"""The conformance fixtures, run against the validator.

``docs/fixtures/plan-conformance.json`` is published with the format so another repository can test
its consumer against it. Running the same cases here is what stops the fixtures from drifting away
from the behaviour they claim to describe.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from siteplan import format as plan_format

FIXTURES = Path(__file__).resolve().parent.parent / "docs" / "fixtures" / "plan-conformance.json"


def load() -> dict:
    return json.loads(FIXTURES.read_text(encoding="utf-8"))


class FixtureFileShape(unittest.TestCase):
    def test_the_file_parses_and_names_the_format(self) -> None:
        document = load()
        self.assertEqual("siteplan-plan-conformance/1", document["format"])
        self.assertEqual(plan_format.PLAN_VERSION, document["plan_version"])
        self.assertGreaterEqual(len(document["cases"]), 20)

    def test_every_case_is_well_formed(self) -> None:
        names = set()
        for case in load()["cases"]:
            with self.subTest(case=case.get("name")):
                self.assertTrue(case["name"])
                self.assertNotIn(case["name"], names)
                names.add(case["name"])
                self.assertTrue(case["covers"], "a case says what it establishes")
                self.assertIn("plan", case)
                self.assertIsInstance(case["valid"], bool)
                if not case["valid"]:
                    self.assertIn("invalid_keys", case)
                    self.assertTrue(case["expect"], "an invalid case pins the producer's message")
                else:
                    self.assertNotIn("expect", case)

    def test_both_kinds_of_case_are_covered(self) -> None:
        cases = load()["cases"]
        self.assertGreaterEqual(len([case for case in cases if case["valid"]]), 5)
        self.assertGreaterEqual(len([case for case in cases if not case["valid"]]), 10)


class FixturesMatchTheValidator(unittest.TestCase):
    def test_every_case(self) -> None:
        for case in load()["cases"]:
            with self.subTest(case=case["name"]):
                problems = plan_format.validate(case["plan"])
                if case["valid"]:
                    self.assertEqual(
                        [], problems, f"{case['name']}: expected no fault, got {problems}"
                    )
                    continue
                self.assertTrue(problems, f"{case['name']}: expected a fault, got none")
                joined = " | ".join(problems)
                for key in case["invalid_keys"]:
                    self.assertIn(
                        key,
                        joined,
                        f"{case['name']}: no fault names {key!r}; faults were {problems}",
                    )
                self.assertIn(
                    case["expect"],
                    joined,
                    f"{case['name']}: expected a fault containing {case['expect']!r}, "
                    f"got {problems}",
                )

    def test_an_unknown_version_is_the_producer_s_own_fault(self) -> None:
        """The fixtures carry version cases, so the validator cannot silently accept a newer file."""
        cases = {case["name"]: case for case in load()["cases"]}
        self.assertIn("unknown-version", cases)
        self.assertFalse(cases["unknown-version"]["valid"])


class DocumentCoversTheImplementation(unittest.TestCase):
    """A drift alarm between the document and the code, not a statement about which one is right.

    The document is authoritative; if this fails, a person decides which side is wrong and changes
    the other. It exists so that a key or a vocabulary value cannot be added to the code and left
    undocumented, which is how an "authoritative" document quietly stops being one.
    """

    def setUp(self) -> None:
        self.document = (
            Path(__file__).resolve().parent.parent / "docs" / "PLAN-FORMAT.md"
        ).read_text(encoding="utf-8")

    def test_every_top_level_key_is_named(self) -> None:
        for key in plan_format.TOP_LEVEL_KEYS:
            with self.subTest(key=key):
                self.assertIn(f"`{key}`", self.document)

    def test_every_closed_vocabulary_value_is_named(self) -> None:
        for value in (
            plan_format.KINDS + plan_format.SURFACES + plan_format.CRAWLER_STANCES
            + plan_format.TRAILING_SLASH
        ):
            with self.subTest(value=value):
                self.assertIn(f"`{value}`", self.document)

    def test_the_nested_keys_are_named(self) -> None:
        for key in plan_format.SECTION_KEYS + plan_format.URL_RULE_KEYS + plan_format.PAGE_KEYS:
            with self.subTest(key=key):
                self.assertIn(f"`{key}`", self.document)

    def test_the_versioning_rules_and_change_log_are_present(self) -> None:
        self.assertIn("## Versioning", self.document)
        self.assertIn("## Change log", self.document)
        self.assertIn("Conformance fixtures", self.document)
        for rule in (
            "Additive optional keys keep `plan_version`",
            "requires a\n   `plan_version` bump",
            "A consumer must not guess",
            "must never present an unchecked\n   key as met",
        ):
            with self.subTest(rule=rule):
                self.assertIn(rule, self.document)


if __name__ == "__main__":
    unittest.main()
