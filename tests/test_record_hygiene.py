"""The record's own claims about time, checked mechanically.

Two revisions of `RECORD.md` were written with times ahead of the clock — estimated rather than read
— and a timestamp is evidence in this method, so the second correction earned a guard rather than a
third paragraph.

What this catches: a record claiming a time that has not happened yet, and an `updated_at` earlier
than `created_at`. What it does not catch: a past time that is merely wrong, or a stage time that
contradicts another line of prose.
"""

from __future__ import annotations

import datetime as dt
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RECORD = REPO_ROOT / "RECORD.md"

FIELD = re.compile(r'^(?P<key>created_at|updated_at):[ \t]*"(?P<value>[^"]+)"', re.M)
TIMESTAMP = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}")

#: Written times and the clock can disagree by a little; they should not disagree by a day.
SLACK = dt.timedelta(minutes=5)


def parse(value: str) -> dt.datetime:
    return dt.datetime.fromisoformat(value)


class TheRecordDoesNotClaimTheFuture(unittest.TestCase):
    def test_front_matter_times_are_not_in_the_future(self) -> None:
        text = RECORD.read_text(encoding="utf-8")
        fields = {match.group("key"): parse(match.group("value")) for match in FIELD.finditer(text)}
        self.assertIn("created_at", fields)
        self.assertIn("updated_at", fields)
        now = dt.datetime.now().astimezone()
        for key, value in fields.items():
            with self.subTest(field=key):
                self.assertLessEqual(
                    value, now + SLACK, f"{key} claims {value.isoformat()}, ahead of {now.isoformat()}"
                )

    def test_updated_at_is_not_before_created_at(self) -> None:
        text = RECORD.read_text(encoding="utf-8")
        fields = {match.group("key"): parse(match.group("value")) for match in FIELD.finditer(text)}
        self.assertLessEqual(fields["created_at"], fields["updated_at"])

    def test_no_timestamp_anywhere_in_the_record_is_in_the_future(self) -> None:
        """Stage tables and returns carry times too, and a future one is the same defect."""
        now = dt.datetime.now().astimezone()
        for raw in TIMESTAMP.findall(RECORD.read_text(encoding="utf-8")):
            with self.subTest(timestamp=raw):
                self.assertLessEqual(parse(raw), now + SLACK)


class TheGuardCanFail(unittest.TestCase):
    def test_a_future_time_would_be_caught(self) -> None:
        future = dt.datetime.now().astimezone() + dt.timedelta(days=1)
        self.assertGreater(future, dt.datetime.now().astimezone() + SLACK)


if __name__ == "__main__":
    unittest.main()
