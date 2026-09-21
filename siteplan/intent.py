"""What the principal said about the site, and how it is collected.

An answer is either stated, asked for interactively, or unstated. There is no fourth state and no
default: anything not supplied is recorded as unstated and no recommendation is adjusted for it.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from urllib.parse import urlsplit

from .format import KINDS

#: The four intent flags, in the order they are asked and rendered.
FLAGS: tuple[str, ...] = ("sells", "local", "publishes", "bookings")

#: The question each flag answers, in the principal's terms.
QUESTIONS: dict[str, str] = {
    "sells": "Does the site sell something directly - a product, a ticket, a paid plan?",
    "local": "Does the business serve a local area, with a place people can visit?",
    "publishes": "Does the site publish content for readers - articles, guides, posts?",
    "bookings": "Can a visitor book a time - an appointment, a table, a slot?",
}


class Cancelled(Exception):
    """The interactive session ended before the questions did."""


@dataclass(frozen=True)
class SiteIntent:
    """The answers, and where each one came from."""

    kind: str
    site: str | None = None
    name: str | None = None
    sells: bool | None = None
    local: bool | None = None
    publishes: bool | None = None
    takes_bookings: bool | None = None
    origin: tuple[tuple[str, str], ...] = field(default=())

    def answer(self, flag: str) -> bool | None:
        return {
            "sells": self.sells,
            "local": self.local,
            "publishes": self.publishes,
            "bookings": self.takes_bookings,
        }[flag]

    def source(self, key: str) -> str:
        """Where a supplied value came from, or that it was never stated."""
        return dict(self.origin).get(key, "not stated")


def normalize_site(raw: str) -> tuple[str, str]:
    """Reduce a supplied address to the bare domain the plan's ``site`` key holds.

    Returns the recorded value and a note describing anything that was dropped, so the brief can
    say what it did with what it was given rather than silently rewriting it.
    """
    supplied = raw.strip()
    if not supplied:
        return "", ""
    candidate = supplied if "://" in supplied else "//" + supplied
    parts = urlsplit(candidate)
    host = (parts.netloc or parts.path.split("/")[0]).rstrip(".").lower()
    dropped: list[str] = []
    if "://" in supplied:
        dropped.append("the scheme")
    if parts.path.strip("/"):
        dropped.append("the path")
    if parts.query:
        dropped.append("the query")
    if parts.fragment:
        dropped.append("the fragment")
    if not dropped:
        return host, ""
    return (
        host,
        f'"{supplied}" was recorded as "{host}": the plan\'s site is a bare domain, so '
        + " and ".join(dropped)
        + (" were" if len(dropped) > 1 else " was")
        + " dropped.",
    )


def _prompt(question: str) -> str:
    try:
        return input(question).strip()
    except EOFError:
        raise Cancelled(
            "input ended before the questions did; nothing was written. Supply the answers as "
            "flags, or run --interactive with a terminal attached."
        ) from None


def _ask_yes_no(question: str) -> bool | None:
    while True:
        answer = _prompt(f"{question} [y/n, Enter leaves it unstated] ").lower()
        if answer == "":
            return None
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print('Please answer "y", "n", or press Enter to leave it unstated.')


def _ask_kind() -> str:
    print("Which kind of site is this?")
    for index, kind in enumerate(KINDS, start=1):
        print(f"  {index}. {kind}")
    while True:
        answer = _prompt("Number or name: ").lower()
        if answer in KINDS:
            return answer
        if answer.isdigit() and 1 <= int(answer) <= len(KINDS):
            return KINDS[int(answer) - 1]
        if answer == "":
            raise Cancelled(
                "a kind is required: it selects the recommendations, and inventing one would "
                "invent the plan. Nothing was written."
            )
        print("Please give one of the numbers or names above.")


def ask(intent: SiteIntent) -> SiteIntent:
    """Fill in the answers that were not supplied. Supplied answers are not asked again."""
    print("Press Enter to leave an answer unstated; the brief will say so rather than guess.")
    origin = dict(intent.origin)
    site, name, kind = intent.site, intent.name, intent.kind

    if kind == "":
        kind = _ask_kind()
        origin["kind"] = "asked interactively"
    if site is None:
        answer = _prompt("Site domain, for example example.com (Enter leaves it unstated): ")
        if answer:
            site, note = normalize_site(answer)
            origin["site"] = "asked interactively"
            if note:
                print(f"note: {note}")
    if name is None:
        answer = _prompt("Site or business name (Enter leaves it unstated): ")
        if answer:
            name = answer
            origin["name"] = "asked interactively"

    answers: dict[str, bool | None] = {}
    for flag in FLAGS:
        supplied = intent.answer(flag)
        if supplied is not None:
            answers[flag] = supplied
            continue
        answers[flag] = _ask_yes_no(QUESTIONS[flag])
        if answers[flag] is not None:
            origin[flag] = "asked interactively"

    print()
    return SiteIntent(
        kind=kind,
        site=site,
        name=name,
        sells=answers["sells"],
        local=answers["local"],
        publishes=answers["publishes"],
        takes_bookings=answers["bookings"],
        origin=tuple(sorted(origin.items())),
    )
