"""Generating a brief and a plan: every kind, the labels, and the claim boundary.

The brief and the plan are rendered from one profile, so these tests check that they agree and that
what the brief claims about itself is true of what it contains.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from siteplan import cli
from siteplan import format as plan_format
from siteplan import kinds

from tests.support import make_site, read_brief, read_plan, section, table_rows, temp_dir

KIND_ARGS = ("--site", "example.com", "--name", "Example Site")


class EveryKindGenerates(unittest.TestCase):
    def test_all_kinds_generate_a_brief_and_a_plan(self) -> None:
        for kind in plan_format.KINDS:
            with self.subTest(kind=kind), temp_dir() as name:
                code, out, err = make_site(name, *KIND_ARGS, "--kind", kind)
                self.assertEqual(0, code, err)
                brief = read_brief(Path(name))
                plan = read_plan(Path(name))
                self.assertIn(f"`{kind}`", brief)
                self.assertEqual(kind, plan["kind"])
                self.assertEqual([], plan_format.validate(plan))
                self.assertIn("wrote", out)

    def test_plan_carries_every_decision(self) -> None:
        for kind in plan_format.KINDS:
            with self.subTest(kind=kind), temp_dir() as name:
                self.assertEqual(0, make_site(name, *KIND_ARGS, "--kind", kind)[0])
                plan = read_plan(Path(name))
                self.assertIn("required_surfaces", plan)
                self.assertTrue(plan["required_surfaces"])
                self.assertTrue(plan["identity"]["schema_types"])
                self.assertTrue(plan["identity"]["fields"])
                self.assertTrue(plan["offering"]["schema_types"])
                self.assertTrue(plan["offering"]["fields"])
                self.assertIn(plan["crawler_stance"], plan_format.CRAWLER_STANCES)
                self.assertTrue(plan["pages"])
                for page in plan["pages"]:
                    self.assertTrue(page["path"].startswith("/"))
                    self.assertTrue(page["purpose"])


class BriefAgreesWithPlan(unittest.TestCase):
    def test_plan_values_appear_in_the_brief(self) -> None:
        for kind in plan_format.KINDS:
            with self.subTest(kind=kind), temp_dir() as name:
                self.assertEqual(0, make_site(name, *KIND_ARGS, "--kind", kind)[0])
                brief = read_brief(Path(name))
                plan = read_plan(Path(name))
                for schema_type in plan["identity"]["schema_types"]:
                    self.assertIn(f"`{schema_type}`", brief)
                for schema_type in plan["offering"]["schema_types"]:
                    self.assertIn(f"`{schema_type}`", brief)
                for field in plan["identity"]["fields"] + plan["offering"]["fields"]:
                    self.assertIn(f"`{field}`", brief)
                for path in (page["path"] for page in plan["pages"]):
                    self.assertIn(f"`{path}`", brief)

    def test_surfaces_table_matches_required_surfaces(self) -> None:
        for kind in plan_format.KINDS:
            with self.subTest(kind=kind), temp_dir() as name:
                self.assertEqual(0, make_site(name, *KIND_ARGS, "--kind", kind)[0])
                brief = read_brief(Path(name))
                plan = read_plan(Path(name))
                rows = table_rows(section(brief, "Machine-readable surfaces"))
                listed = [row[0].strip("`") for row in rows]
                self.assertEqual(plan["required_surfaces"], listed)

    def test_every_surface_row_carries_a_basis(self) -> None:
        with temp_dir() as name:
            self.assertEqual(0, make_site(name, *KIND_ARGS, "--kind", "online-store")[0])
            rows = table_rows(
                section(read_brief(Path(name)), "Machine-readable surfaces")
            )
        self.assertTrue(rows)
        for row in rows:
            self.assertIn(row[1], {kinds.BASIS_PRACTICE, kinds.BASIS_JUDGEMENT})


class BriefStatesItsBasis(unittest.TestCase):
    def test_both_labels_appear_for_every_kind(self) -> None:
        for kind in plan_format.KINDS:
            with self.subTest(kind=kind), temp_dir() as name:
                self.assertEqual(0, make_site(name, *KIND_ARGS, "--kind", kind)[0])
                brief = read_brief(Path(name))
                self.assertIn("**published practice**", brief)
                self.assertIn("**our judgement**", brief)
                self.assertIn("published practice", brief)
                self.assertIn("our judgement", brief)

    def test_each_recommendation_carries_one_basis(self) -> None:
        with temp_dir() as name:
            self.assertEqual(0, make_site(name, *KIND_ARGS, "--kind", "saas")[0])
            brief = read_brief(Path(name))
        basis_lines = [line for line in brief.splitlines() if line.strip().startswith("Basis: ")]
        self.assertGreaterEqual(len(basis_lines), 6)
        for line in basis_lines:
            self.assertTrue(
                line.startswith(f"  Basis: {kinds.BASIS_PRACTICE}.")
                or line.startswith(f"  Basis: {kinds.BASIS_JUDGEMENT}."),
                line,
            )

    def test_the_two_labels_are_explained(self) -> None:
        with temp_dir() as name:
            self.assertEqual(0, make_site(name, *KIND_ARGS, "--kind", "content-site")[0])
            brief = read_brief(Path(name))
        self.assertIn("You can check it", brief)
        self.assertIn("entitled to discount it", brief)

    def test_published_practice_claims_name_their_source(self) -> None:
        with temp_dir() as name:
            self.assertEqual(0, make_site(name, *KIND_ARGS, "--kind", "directory")[0])
            brief = read_brief(Path(name))
        self.assertIn("## Sources for the published-practice claims", brief)
        self.assertIn("RFC 9309", brief)
        self.assertIn("sitemaps.org", brief)
        self.assertIn("https://schema.org/", brief)


class BriefKeepsTheClaimBoundary(unittest.TestCase):
    def test_the_boundary_is_stated_in_the_briefs_own_words(self) -> None:
        with temp_dir() as name:
            self.assertEqual(0, make_site(name, *KIND_ARGS, "--kind", "local-business")[0])
            brief = read_brief(Path(name))
        self.assertIn(
            "does not predict whether an agent will find, understand or\nrecommend the site", brief
        )
        self.assertIn("Neither is evidence of success", brief)
        self.assertIn("## What this brief does not claim", brief)
        self.assertIn("measured nothing about any live site", brief)

    def test_no_kind_promises_discovery(self) -> None:
        forbidden = (
            "will be found",
            "guarantees",
            "will rank",
            "improves your ranking",
            "agents will recommend",
        )
        for kind in plan_format.KINDS:
            with self.subTest(kind=kind), temp_dir() as name:
                self.assertEqual(0, make_site(name, *KIND_ARGS, "--kind", kind)[0])
                brief = read_brief(Path(name))
                for phrase in forbidden:
                    self.assertNotIn(phrase, brief)


class OutputIsDeterministic(unittest.TestCase):
    def test_two_runs_with_the_same_inputs_are_byte_identical(self) -> None:
        inputs = ("--site", "example.com", "--kind", "saas", "--sells", "--local")
        with temp_dir() as name:
            for _ in range(2):
                self.assertEqual(0, make_site(name, *inputs, "--force")[0])
            first = (
                read_brief(Path(name)),
                read_plan(Path(name)),
            )
        with temp_dir() as name:
            self.assertEqual(0, make_site(name, *inputs)[0])
            second = (
                read_brief(Path(name)),
                read_plan(Path(name)),
            )
        self.assertEqual(first, second)

    def test_plan_key_order_is_the_documented_order(self) -> None:
        with temp_dir() as name:
            self.assertEqual(0, make_site(name, *KIND_ARGS, "--kind", "personal")[0])
            plan = read_plan(Path(name))
        self.assertEqual(
            [
                "plan_version",
                "site",
                "kind",
                "required_surfaces",
                "identity",
                "offering",
                "url_rules",
                "crawler_stance",
                "pages",
            ],
            list(plan),
        )


class ExistingFilesAreProtected(unittest.TestCase):
    def test_refuses_to_overwrite_without_force(self) -> None:
        with temp_dir() as name:
            self.assertEqual(0, make_site(name, *KIND_ARGS, "--kind", "personal")[0])
            before = read_brief(Path(name))
            code, _, err = make_site(name, *KIND_ARGS, "--kind", "saas")
            self.assertEqual(2, code)
            self.assertIn("refusing to overwrite", err)
            self.assertEqual(before, read_brief(Path(name)))

    def test_force_replaces_them(self) -> None:
        with temp_dir() as name:
            self.assertEqual(0, make_site(name, *KIND_ARGS, "--kind", "personal")[0])
            self.assertEqual(0, make_site(name, *KIND_ARGS, "--kind", "saas", "--force")[0])
            self.assertEqual("saas", read_plan(Path(name))["kind"])


class PackageSelfCheck(unittest.TestCase):
    def test_generated_plan_is_json_serialisable_and_valid(self) -> None:
        with temp_dir() as name:
            self.assertEqual(0, make_site(name, *KIND_ARGS, "--kind", "content-site")[0])
            text = (Path(name) / cli.PLAN_NAME).read_text(encoding="utf-8")
        self.assertEqual([], plan_format.validate(json.loads(text)))
        self.assertTrue(text.endswith("\n"))


if __name__ == "__main__":
    unittest.main()
