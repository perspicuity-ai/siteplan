"""An input that was not supplied is recorded as unstated, and is never filled in.

This is the requirement the product's honesty rests on: the plan must not carry an answer the
principal did not give, and the brief must say which answers are missing and what stating each one
would change.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from siteplan import intent as site_intent
from siteplan import kinds, plan
from siteplan.brief import FLAG_LABELS

from tests.support import make_site, read_brief, read_plan, section, table_rows, temp_dir

BASE_ARGS = ("--kind", "local-business")


class UnstatedStaysUnstated(unittest.TestCase):
    def test_every_intent_flag_is_unstated_when_not_given(self) -> None:
        with temp_dir() as name:
            self.assertEqual(0, make_site(name, *BASE_ARGS)[0])
            brief = read_brief(Path(name))
            rows = table_rows(section(brief, "Inputs"))
        by_label = {row[0]: row[2] for row in rows}
        for flag in site_intent.FLAGS:
            with self.subTest(flag=flag):
                question = site_intent.QUESTIONS[flag].rstrip("?")
                self.assertEqual("**unstated**", by_label[question])
        self.assertEqual("**unstated**", by_label["Site"])
        self.assertEqual("**unstated**", by_label["Name"])

    def test_a_missing_site_and_name_are_not_invented(self) -> None:
        with temp_dir() as name:
            self.assertEqual(0, make_site(name, *BASE_ARGS)[0])
            brief = read_brief(Path(name))
            plan_file = read_plan(Path(name))
        self.assertNotIn("site", plan_file)
        self.assertTrue(brief.startswith("# Untitled site - agent-first design brief"))
        self.assertNotIn("example.com", brief)

    def test_an_unstated_flag_changes_nothing_in_the_plan(self) -> None:
        """The plan is the kind's recommendation, not an answer the principal never gave."""
        with temp_dir() as name:
            self.assertEqual(0, make_site(name, *BASE_ARGS)[0])
            unstated_plan = read_plan(Path(name))
        base = kinds.PROFILES["local-business"]
        expected = plan.build(site_intent.SiteIntent(kind="local-business"), base)
        self.assertEqual(expected, unstated_plan)
        self.assertNotIn("Offer", unstated_plan["offering"]["schema_types"])
        self.assertNotIn("price", unstated_plan["offering"]["fields"])

    def test_stating_a_flag_changes_the_plan(self) -> None:
        with temp_dir() as name:
            self.assertEqual(0, make_site(name, *BASE_ARGS, "--sells")[0])
            selling = read_plan(Path(name))
        self.assertIn("Offer", selling["offering"]["schema_types"])
        self.assertIn("price", selling["offering"]["fields"])

    def test_the_unstated_labels_carry_the_flags_to_state_them(self) -> None:
        with temp_dir() as name:
            self.assertEqual(0, make_site(name, *BASE_ARGS)[0])
            brief = read_brief(Path(name))
            rows = table_rows(section(brief, "What was not stated, and what changes if you state it"))
        listed = {row[0] for row in rows}
        for flag in site_intent.FLAGS:
            with self.subTest(flag=flag):
                self.assertIn(FLAG_LABELS[flag], listed)

    def test_what_would_change_is_computed_not_asserted(self) -> None:
        """Each row must state the same consequence the catalogue produces for that answer."""
        base = kinds.PROFILES["local-business"]
        with temp_dir() as name:
            self.assertEqual(0, make_site(name, *BASE_ARGS)[0])
            brief = read_brief(Path(name))
            rows = table_rows(section(brief, "What was not stated, and what changes if you state it"))
        by_label = {row[0]: (row[1], row[2]) for row in rows}
        for flag in site_intent.FLAGS:
            if flag == "bookings":
                continue  # bookings=no changes nothing and reads as "nothing changes in this plan"
            with self.subTest(flag=flag):
                yes = "; ".join(kinds.changes(base, kinds.with_flag(base, flag, True)))
                no = "; ".join(kinds.changes(base, kinds.with_flag(base, flag, False)))
                self.assertEqual(yes or "nothing changes in this plan", by_label[FLAG_LABELS[flag]][0])
                self.assertEqual(no or "nothing changes in this plan", by_label[FLAG_LABELS[flag]][1])

    def test_all_stated_says_so(self) -> None:
        with temp_dir() as name:
            code, _, _ = make_site(
                name, *BASE_ARGS, "--sells", "--local", "--publishes", "--takes-bookings"
            )
            self.assertEqual(0, code)
            brief = read_brief(Path(name))
        self.assertIn("Every input was stated on the command line or at the prompt.", brief)


class StatedAnswersAreRecorded(unittest.TestCase):
    def test_negatives_are_recorded_as_no(self) -> None:
        with temp_dir() as name:
            code, _, _ = make_site(name, *BASE_ARGS, "--no-sells", "--not-local")
            self.assertEqual(0, code)
            brief = read_brief(Path(name))
            rows = table_rows(section(brief, "Inputs"))
        by_label = {row[0]: row for row in rows}
        self.assertEqual("no", by_label[site_intent.QUESTIONS["sells"].rstrip("?")][2])
        self.assertEqual("no", by_label[site_intent.QUESTIONS["local"].rstrip("?")][2])
        self.assertEqual("--no-sells", by_label[site_intent.QUESTIONS["sells"].rstrip("?")][1])
        self.assertEqual("--not-local", by_label[site_intent.QUESTIONS["local"].rstrip("?")][1])

    def test_a_contradiction_between_kind_and_answer_is_stated(self) -> None:
        with temp_dir() as name:
            self.assertEqual(0, make_site(name, *BASE_ARGS, "--not-local")[0])
            brief = read_brief(Path(name))
            plan_file = read_plan(Path(name))
        self.assertIn("do not fit", brief)
        self.assertNotIn("address", plan_file["identity"]["fields"])
        self.assertIn("local-business", brief)

    def test_no_tension_is_invented_when_the_answers_fit(self) -> None:
        with temp_dir() as name:
            self.assertEqual(0, make_site(name, *BASE_ARGS, "--local", "--sells")[0])
            brief = read_brief(Path(name))
        self.assertNotIn("do not fit", brief)

    def test_a_supplied_address_is_reduced_to_a_domain_and_the_note_says_so(self) -> None:
        with temp_dir() as name:
            code, _, _ = make_site(name, *BASE_ARGS, "--site", "https://example.com/pricing")
            self.assertEqual(0, code)
            brief = read_brief(Path(name))
            plan_file = read_plan(Path(name))
        self.assertEqual("example.com", plan_file["site"])
        self.assertIn("## Notes on the inputs", brief)
        self.assertIn("was recorded as", brief)


if __name__ == "__main__":
    unittest.main()
