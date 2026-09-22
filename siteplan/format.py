"""The plan file format: keys, vocabularies, and validation.

``docs/PLAN-FORMAT.md`` is the authoritative specification. This module implements it. If the two
disagree the document governs the format and this module is the defect.

Two rules shape everything here:

* ``plan_version`` is required, because a file that does not name its format cannot be consumed
  safely. Every other key is optional, so a partial plan is valid.
* Unknown keys are rejected at every level. A key nobody understands is a decision that was not
  made, and a plan that drifts silently from what was agreed is the failure this project exists to
  prevent.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

PLAN_VERSION = 1

#: The kinds the format allows. ``siteplan/kinds.py`` supplies a profile for each; a test keeps
#: the two lists equal.
KINDS: tuple[str, ...] = (
    "content-site",
    "directory",
    "local-business",
    "online-store",
    "personal",
    "saas",
)

#: The machine-readable surfaces a plan may require. Closed on purpose: the consumer has to know
#: what each name means.
SURFACES: tuple[str, ...] = (
    "json-ld",
    "llms.txt",
    "robots.txt",
    "rss.xml",
    "sitemap.xml",
)

CRAWLER_STANCES: tuple[str, ...] = ("closed", "open", "selective")

TRAILING_SLASH: tuple[str, ...] = ("always", "never")

TOP_LEVEL_KEYS: tuple[str, ...] = (
    "plan_version",
    "site",
    "kind",
    "required_surfaces",
    "identity",
    "offering",
    "url_rules",
    "crawler_stance",
    "pages",
)

SECTION_KEYS: tuple[str, ...] = ("schema_types", "fields")
URL_RULE_KEYS: tuple[str, ...] = ("lowercase", "trailing_slash", "max_depth")
PAGE_KEYS: tuple[str, ...] = ("path", "purpose")

#: A Schema.org type name, e.g. ``LocalBusiness`` or ``BlogPosting``.
SCHEMA_TYPE_NAME = re.compile(r"^[A-Z][A-Za-z0-9]*$")
#: A Schema.org property name, e.g. ``name`` or ``openingHoursSpecification``.
FIELD_NAME = re.compile(r"^[a-z][A-Za-z0-9]*$")

#: A bare host name: dot-separated DNS labels, optionally with the root dot. Host names are
#: case-insensitive, so upper case is accepted; a non-ASCII name must be punycode.
_DNS_LABEL = r"[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?"
SITE_NAME = re.compile(rf"^{_DNS_LABEL}(?:\.{_DNS_LABEL})*\.?$")

#: One path segment: ASCII path characters, or a single ``<placeholder>`` segment naming a family
#: of pages. Whitespace, ``?``, ``#`` and non-ASCII characters are not path characters here.
PATH_SEGMENT = r"(?:[A-Za-z0-9\-._~%!$&'()*+,;=:@]+|<[a-z][a-z0-9_-]*>)"
#: A site-relative path: ``/`` alone, or slash-separated non-empty segments. No empty segment, so
#: ``//a`` is invalid; at most one placeholder is enforced separately.
PAGE_PATH = re.compile(rf"^/(?:{PATH_SEGMENT})(?:/{PATH_SEGMENT})*$")
PLACEHOLDER = re.compile(r"<[a-z][a-z0-9_-]*>")


def _show(value: Any) -> str:
    """Render a value for a message without letting it run away."""
    try:
        text = json.dumps(value, ensure_ascii=True)
    except (TypeError, ValueError):  # pragma: no cover - json handles our inputs
        text = repr(value)
    return text if len(text) <= 60 else text[:57] + "..."


def _suggestion(key: str, allowed: tuple[str, ...]) -> str:
    """Name the allowed key a mistyped one was probably meant to be."""
    folded = key.replace("_", "").replace("-", "").lower()
    for candidate in allowed:
        if candidate.replace("_", "").replace("-", "").lower() == folded:
            return f'; did you mean "{candidate}"?'
    return ""


def _unknown_key(key: str, allowed: tuple[str, ...], prefix: str) -> str:
    """One fault naming the offending key's own path, so a reader can find it in the file."""
    where = f"{prefix}.{key}" if prefix else "top level"
    return (
        f'{where}: unknown key "{key}" (allowed: {", ".join(allowed)})'
        f"{_suggestion(key, allowed)}"
    )


def _string_list(
    value: Any,
    where: str,
    allowed: tuple[str, ...] | None = None,
    pattern: re.Pattern[str] | None = None,
    example: str = "",
) -> list[str]:
    """Validate a list of names, returning one problem message per fault."""
    problems: list[str] = []
    if not isinstance(value, list):
        problems.append(f"{where}: expected a list of strings, got {_show(value)}")
        return problems
    if not value:
        problems.append(
            f"{where}: empty list; every key is optional, so omit the key instead of "
            "requiring nothing"
        )
        return problems
    seen: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item:
            problems.append(
                f"{where}[{index}]: expected a non-empty string, got {_show(item)}"
            )
            continue
        if allowed is not None and item not in allowed:
            problems.append(
                f'{where}[{index}]: unknown name "{item}" (allowed: {", ".join(allowed)})'
                f"{_suggestion(item, allowed)}"
            )
        elif pattern is not None and not pattern.fullmatch(item):
            problems.append(
                f'{where}[{index}]: "{item}" is not a Schema.org name'
                + (f" such as {example}" if example else "")
            )
        if item in seen:
            problems.append(f'{where}[{index}]: duplicate "{item}"')
        seen.append(item)
    return problems


def _validate_section(name: str, value: Any) -> list[str]:
    """Validate ``identity`` or ``offering``: an object of ``schema_types`` and ``fields``."""
    if not isinstance(value, dict):
        return [f"{name}: expected an object, got {_show(value)}"]
    problems: list[str] = []
    for key in value:
        if key not in SECTION_KEYS:
            problems.append(_unknown_key(key, SECTION_KEYS, name))
    known = [key for key in SECTION_KEYS if key in value]
    if not known:
        problems.append(
            f"{name}: no recognized keys; give schema_types or fields, or omit the key"
        )
    if "schema_types" in value:
        problems.extend(
            _string_list(
                value["schema_types"],
                f"{name}.schema_types",
                pattern=SCHEMA_TYPE_NAME,
                example='"LocalBusiness"',
            )
        )
    if "fields" in value:
        problems.extend(
            _string_list(
                value["fields"],
                f"{name}.fields",
                pattern=FIELD_NAME,
                example='"telephone" or "openingHoursSpecification"',
            )
        )
    return problems


def _validate_url_rules(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return [f"url_rules: expected an object, got {_show(value)}"]
    problems: list[str] = []
    for key in value:
        if key not in URL_RULE_KEYS:
            problems.append(_unknown_key(key, URL_RULE_KEYS, "url_rules"))
    if not any(key in value for key in URL_RULE_KEYS):
        problems.append(
            "url_rules: no recognized keys; give lowercase, trailing_slash or max_depth, "
            "or omit the key"
        )
    if "lowercase" in value and not isinstance(value["lowercase"], bool):
        problems.append(
            f"url_rules.lowercase: expected true or false, got {_show(value['lowercase'])}"
        )
    if "trailing_slash" in value and value["trailing_slash"] not in TRAILING_SLASH:
        problems.append(
            "url_rules.trailing_slash: expected "
            + " or ".join(f'"{item}"' for item in TRAILING_SLASH)
            + f", got {_show(value['trailing_slash'])}"
        )
    if "max_depth" in value:
        depth = value["max_depth"]
        if isinstance(depth, bool) or not isinstance(depth, int) or depth < 1:
            problems.append(
                f"url_rules.max_depth: expected a positive integer, got {_show(depth)}; "
                '"/" is depth 0 and "/a/b" is depth 2'
            )
    return problems


def _depth(path: str) -> int:
    """The path depth: ``/`` is 0, ``/a`` is 1, ``/a/b`` is 2. A placeholder is one segment."""
    return len([segment for segment in path.split("/") if segment])


def _validate_pages(value: Any, max_depth: int | None = None) -> list[str]:
    if not isinstance(value, list):
        return [f"pages: expected a list of page objects, got {_show(value)}"]
    if not value:
        return [
            "pages: empty list; every key is optional, so omit the key instead of planning "
            "no pages"
        ]
    problems: list[str] = []
    seen: list[str] = []
    for index, page in enumerate(value):
        where = f"pages[{index}]"
        if not isinstance(page, dict):
            problems.append(f"{where}: expected an object with path and purpose, got {_show(page)}")
            continue
        for key in page:
            if key not in PAGE_KEYS:
                problems.append(_unknown_key(key, PAGE_KEYS, where))
        for key in PAGE_KEYS:
            if key not in page:
                problems.append(f"{where}.{key}: required")
        path = page.get("path")
        if isinstance(path, str):
            if path != "/" and not PAGE_PATH.fullmatch(path):
                problems.append(
                    f'{where}.path: expected "/" or slash-separated ASCII segments beginning '
                    f'with "/", got {_show(path)}'
                )
            elif len(PLACEHOLDER.findall(path)) > 1:
                problems.append(
                    f'{where}.path: at most one <placeholder> segment per path, got '
                    f"{_show(path)}"
                )
            elif path in seen:
                problems.append(f'{where}.path: duplicate path "{path}"')
            else:
                seen.append(path)
                if max_depth is not None and _depth(path) > max_depth:
                    problems.append(
                        f"{where}.path: depth {_depth(path)} exceeds url_rules.max_depth "
                        f"{max_depth}; a page may not be deeper than the plan's own URL rules"
                    )
        elif path is not None:
            problems.append(f"{where}.path: expected a string, got {_show(path)}")
        purpose = page.get("purpose")
        if purpose is not None and (not isinstance(purpose, str) or not purpose.strip()):
            problems.append(
                f"{where}.purpose: expected a non-empty string, got {_show(purpose)}"
            )
    return problems


def validate(data: Any) -> list[str]:
    """Validate a parsed plan. Returns one message per fault; an empty list means valid."""
    if not isinstance(data, dict):
        return [f"the plan must be a JSON object at the top level, got {_show(data)}"]

    problems: list[str] = []
    for key in data:
        if key not in TOP_LEVEL_KEYS:
            problems.append(_unknown_key(key, TOP_LEVEL_KEYS, ""))

    if "plan_version" not in data:
        problems.append(
            "plan_version: required; it names the format this file follows, and it is the only "
            "required key"
        )
    else:
        version = data["plan_version"]
        if isinstance(version, bool) or not isinstance(version, int):
            problems.append(
                f"plan_version: expected the integer {PLAN_VERSION}, got {_show(version)}"
            )
        elif version != PLAN_VERSION:
            problems.append(
                f"plan_version: expected {PLAN_VERSION}, got {version}; this checker implements "
                f"plan_version {PLAN_VERSION} only"
            )

    if "site" in data:
        site = data["site"]
        if not isinstance(site, str) or not site:
            problems.append(f"site: expected a non-empty string, got {_show(site)}")
        elif not SITE_NAME.fullmatch(site):
            problems.append(
                f'site: expected a bare domain such as "example.com" (dot-separated host labels, '
                f"no scheme, no path, no port, no whitespace), got {_show(site)}"
            )

    if "kind" in data:
        kind = data["kind"]
        if not isinstance(kind, str) or kind not in KINDS:
            problems.append(
                f"kind: expected one of {', '.join(KINDS)}; got {_show(kind)}"
                f"{_suggestion(str(kind), KINDS)}"
            )

    if "required_surfaces" in data:
        problems.extend(
            _string_list(data["required_surfaces"], "required_surfaces", allowed=SURFACES)
        )

    for section in ("identity", "offering"):
        if section in data:
            problems.extend(_validate_section(section, data[section]))

    max_depth: int | None = None
    if "url_rules" in data:
        problems.extend(_validate_url_rules(data["url_rules"]))
        rules = data["url_rules"]
        if isinstance(rules, dict):
            depth = rules.get("max_depth")
            if isinstance(depth, int) and not isinstance(depth, bool) and depth >= 1:
                max_depth = depth

    if "crawler_stance" in data:
        stance = data["crawler_stance"]
        if not isinstance(stance, str) or stance not in CRAWLER_STANCES:
            problems.append(
                f"crawler_stance: expected one of {', '.join(CRAWLER_STANCES)}; "
                f"got {_show(stance)}"
            )

    if "pages" in data:
        problems.extend(_validate_pages(data["pages"], max_depth))

    return problems


class RepeatedKey(Exception):
    """A JSON object in the plan repeated a key, which the format forbids."""

    def __init__(self, keys: list[str]) -> None:
        super().__init__(", ".join(keys))
        self.keys = keys


def _object_without_repeated_keys(pairs: list[tuple[str, Any]]) -> dict:
    """Build one JSON object, refusing a repeated key.

    JSON leaves a repeated key to the implementation — one parser keeps the last value, another the
    first — so two compliant readers could take different plans from the same bytes with no fault on
    either side. The format closes that by making the file invalid, which is why this hook exists
    rather than a plain ``json.loads``.
    """
    seen: dict[str, Any] = {}
    repeated: list[str] = []
    for key, value in pairs:
        if key in seen and key not in repeated:
            repeated.append(key)
        seen[key] = value
    if repeated:
        raise RepeatedKey(repeated)
    return seen


def read_plan(path: str | Path) -> tuple[Any, list[str]]:
    """Read and parse a plan file. Returns ``(data, problems)``; data is None when unreadable."""
    file = Path(path)
    try:
        text = file.read_text(encoding="utf-8")
    except OSError as error:
        return None, [f"cannot read {file}: {error.strerror or error}"]
    try:
        return json.loads(text, object_pairs_hook=_object_without_repeated_keys), []
    except RepeatedKey as error:
        names = ", ".join(f'"{key}"' for key in error.keys)
        return None, [
            f"{file}: repeated key {names} in one JSON object; the format forbids it because two "
            f"readers would otherwise take different plans from the same bytes"
        ]
    except json.JSONDecodeError as error:
        return None, [f"{file}: not valid JSON: {error.msg} (line {error.lineno}, column {error.colno})"]


def summarise(data: Any) -> str:
    """A one-line description of a valid plan, for the check command."""
    parts: list[str] = []
    if isinstance(data, dict):
        parts.append(f"plan_version {data['plan_version']}")
        if "site" in data:
            parts.append(f"site {data['site']}")
        if "kind" in data:
            parts.append(f"kind {data['kind']}")
        for key, label in (
            ("required_surfaces", "surface"),
            ("pages", "page"),
        ):
            if key in data:
                count = len(data[key])
                parts.append(f"{count} {label}{'' if count == 1 else 's'}")
        for key in ("identity", "offering"):
            if key in data and "schema_types" in data[key]:
                parts.append(f"{key} {'/'.join(data[key]['schema_types'])}")
        if "crawler_stance" in data:
            parts.append(f"crawlers {data['crawler_stance']}")
    return ", ".join(parts)
