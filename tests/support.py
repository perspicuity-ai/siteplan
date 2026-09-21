"""Shared helpers for the tests: run the command line in-process, and read what it wrote."""

from __future__ import annotations

import contextlib
import io
import json
import re
import tempfile
from pathlib import Path

from siteplan import cli

REPO_ROOT = Path(__file__).resolve().parent.parent


def run_cli(*argv: str) -> tuple[int, str, str]:
    """Run the command line in-process and capture its output and exit code."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = cli.main(list(argv))
        except SystemExit as exit_code:  # argparse reports usage errors by exiting
            code = exit_code.code if isinstance(exit_code.code, int) else 2
    return code, out.getvalue(), err.getvalue()


def make_site(directory: Path, *argv: str) -> tuple[int, str, str]:
    return run_cli("new", "--out", str(directory), *argv)


def read_plan(directory: Path) -> dict:
    return json.loads((directory / cli.PLAN_NAME).read_text(encoding="utf-8"))


def read_brief(directory: Path) -> str:
    return (directory / cli.BRIEF_NAME).read_text(encoding="utf-8")


def temp_dir() -> tempfile.TemporaryDirectory:
    return tempfile.TemporaryDirectory(prefix="siteplan-test-")


def section(brief: str, heading: str) -> str:
    """The text of one heading's section, up to the next heading of the same or higher level.

    Accepts ``## Title`` and ``### 1. Title`` alike.
    """
    pattern = re.compile(
        rf"(?m)^(?P<hashes>#{{2,3}}) (?:\d+\. )?{re.escape(heading)}[ \t]*$"
    )
    start = pattern.search(brief)
    if start is None:
        raise AssertionError(f"no section headed {heading!r} in the brief")
    level = len(start.group("hashes"))
    rest = brief[start.end():]
    end = re.search(rf"(?m)^#{{1,{level}}} ", rest)
    return rest[: end.start()] if end else rest


def table_rows(block: str) -> list[list[str]]:
    """The body rows of the first Markdown table in a block, cells stripped."""
    rows: list[list[str]] = []
    for line in block.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if all(set(cell) <= {"-", " "} for cell in cells):
            continue
        rows.append(cells)
    return rows[1:] if rows else []
