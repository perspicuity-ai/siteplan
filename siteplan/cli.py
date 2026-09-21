"""The command line: ``siteplan new`` and ``siteplan check``.

Exit codes, which the format document and the README both state:

* ``0`` - success.
* ``1`` - a plan file that does not follow the format.
* ``2`` - a usage error, a refused overwrite, or an interactive session that ended early.
* ``3`` - siteplan produced a plan that fails its own check; that is a defect here, not in the
  input, and it is reported as one.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__, brief
from . import format as plan_format
from . import intent as site_intent
from . import kinds, plan

BRIEF_NAME = "BRIEF.md"
PLAN_NAME = "site.json"

#: dest, positive flag, negative flag, one-line meaning. The order is the order they are asked.
INTENT_FLAGS: tuple[tuple[str, str, str, str], ...] = (
    ("sells", "--sells", "--no-sells", "the site sells something directly"),
    ("local", "--local", "--not-local", "the business serves a local area"),
    ("publishes", "--publishes", "--no-publishes", "the site publishes content for readers"),
    (
        "bookings",
        "--takes-bookings",
        "--no-takes-bookings",
        "a visitor can book an appointment, table or slot",
    ),
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="siteplan",
        description=(
            "Turn a site's intent into an agent-first design brief. Writes BRIEF.md for a reader "
            "and site.json for a consumer such as 'sitewalk --plan'."
        ),
        epilog=(
            "Standard library only. No network, no crawling, no code generation, no templates. "
            "The plan file format is specified in docs/PLAN-FORMAT.md."
        ),
    )
    parser.add_argument("--version", action="version", version=f"siteplan {__version__}")
    subcommands = parser.add_subparsers(dest="command", required=True, metavar="{new,check}")

    new = subcommands.add_parser(
        "new",
        help="write BRIEF.md and site.json for a site",
        description=(
            "Write a design brief and a plan file. Supply the inputs as flags, or use "
            "--interactive. Anything not supplied is recorded as unstated, never invented."
        ),
    )
    new.add_argument("--site", metavar="DOMAIN", help="the site's domain, for example example.com")
    new.add_argument("--name", metavar="NAME", help="what the site or the business is called")
    new.add_argument(
        "--kind",
        choices=plan_format.KINDS,
        metavar="KIND",
        help="the kind of site, which selects the recommendations: "
        + ", ".join(plan_format.KINDS),
    )
    new.add_argument(
        "--out", metavar="DIR", default=".", help="directory to write into (default: .)"
    )
    new.add_argument(
        "--interactive",
        action="store_true",
        help="ask for the answers the flags did not supply",
    )
    new.add_argument(
        "--force",
        action="store_true",
        help=f"overwrite {BRIEF_NAME} and {PLAN_NAME} if they already exist",
    )
    answers = new.add_argument_group("intent flags", "each pair states the answer; neither states nothing")
    for dest, positive, negative, meaning in INTENT_FLAGS:
        answers.add_argument(
            positive, dest=f"{dest}_yes", action="store_true", help=meaning
        )
        answers.add_argument(
            negative, dest=f"{dest}_no", action="store_true", help=f"not: {meaning}"
        )

    check = subcommands.add_parser(
        "check",
        help="validate a plan file against docs/PLAN-FORMAT.md",
        description=(
            "Report every fault in a plan file. Exits 0 when the file follows the format, 1 when "
            "it does not. A file that passes is a well-formed plan; it is not evidence that the "
            "plan is good or that a site following it will succeed."
        ),
    )
    check.add_argument("path", metavar="FILE", help="the plan file to check, for example site.json")
    return parser


def _intent_from_args(args: argparse.Namespace, parser: argparse.ArgumentParser) -> site_intent.SiteIntent:
    """Collect the answers the command line supplied, and nothing else."""
    origin: dict[str, str] = {}
    answers: dict[str, bool | None] = {}
    for dest, positive, negative, _ in INTENT_FLAGS:
        yes = getattr(args, f"{dest}_yes")
        no = getattr(args, f"{dest}_no")
        if yes and no:
            parser.error(f"{positive} and {negative} contradict each other; give one or neither")
        answers[dest] = True if yes else (False if no else None)
        if yes:
            origin[dest] = positive
        elif no:
            origin[dest] = negative

    site: str | None = None
    if args.site is not None:
        site, _ = site_intent.normalize_site(args.site)
        if not site:
            parser.error("--site needs a domain, for example --site example.com")
        origin["site"] = "--site"
    if args.name is not None:
        origin["name"] = "--name"
    if args.kind:
        origin["kind"] = "--kind"

    return site_intent.SiteIntent(
        kind=args.kind or "",
        site=site,
        name=args.name,
        sells=answers["sells"],
        local=answers["local"],
        publishes=answers["publishes"],
        takes_bookings=answers["bookings"],
        origin=tuple(sorted(origin.items())),
    )


def _new(args: argparse.Namespace, parser: argparse.ArgumentParser) -> int:
    intent = _intent_from_args(args, parser)

    notes: list[str] = []
    if args.site is not None:
        _, note = site_intent.normalize_site(args.site)
        if note:
            notes.append(note)

    if args.interactive:
        try:
            intent = site_intent.ask(intent)
        except site_intent.Cancelled as error:
            print(f"error: {error}", file=sys.stderr)
            return 2

    if not intent.kind:
        parser.error(
            "--kind is required unless --interactive is used: the kind selects the "
            "recommendations, and guessing one would invent the plan. Choose from: "
            + ", ".join(plan_format.KINDS)
        )

    base = kinds.PROFILES[intent.kind]
    profile = kinds.apply_intent(base, intent)
    document = plan.build(intent, profile)

    faults = plan_format.validate(document)
    if faults:
        print("error: siteplan produced a plan that fails its own check.", file=sys.stderr)
        for fault in faults:
            print(f"  {fault}", file=sys.stderr)
        print("This is a defect in the kind catalogue, not in your input.", file=sys.stderr)
        return 3

    output_dir = Path(args.out)
    targets = [
        (output_dir / BRIEF_NAME, brief.render(intent, base, profile, tuple(notes))),
        (output_dir / PLAN_NAME, plan.render(document)),
    ]
    existing = [path for path, _ in targets if path.exists()]
    if existing and not args.force:
        print(
            "error: refusing to overwrite "
            + ", ".join(str(path) for path in existing)
            + "; pass --force to replace them",
            file=sys.stderr,
        )
        return 2
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        for path, text in targets:
            path.write_text(text, encoding="utf-8")
    except OSError as error:
        print(f"error: cannot write {error.filename or output_dir}: {error.strerror or error}", file=sys.stderr)
        return 2

    unstated = [flag for flag in site_intent.FLAGS if intent.answer(flag) is None]
    print(f"wrote {BRIEF_NAME} and {PLAN_NAME} in {output_dir}")
    print(
        f"kind: {profile.kind}; {len(profile.surfaces)} required surfaces; "
        f"{len(profile.pages)} pages; crawler stance: {profile.crawler_stance}"
    )
    if unstated:
        print(
            "unstated: "
            + ", ".join(unstated)
            + " - the brief says what stating each answer would change"
        )
    else:
        print("unstated: nothing; every intent flag was stated")
    return 0


def _check(args: argparse.Namespace) -> int:
    data, faults = plan_format.read_plan(args.path)
    if not faults:
        faults = plan_format.validate(data)
    if faults:
        count = len(faults)
        print(f"{args.path}: {count} problem{'' if count == 1 else 's'}", file=sys.stderr)
        for fault in faults:
            print(f"  {fault}", file=sys.stderr)
        return 1
    print(f"{args.path}: ok ({plan_format.summarise(data)})")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "new":
        return _new(args, parser)
    return _check(args)
