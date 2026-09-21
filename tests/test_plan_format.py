"""The plan file format: what check accepts, and what it rejects with which message.

Every rejection asserts on the message, because the point of the check is that a reader can tell
what is wrong with the file rather than only that something is.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from siteplan import format as plan_format
from siteplan import intent as site_intent
from siteplan import kinds, plan

from tests.support import temp_dir

GOOD_PLAN = {
    "plan_version": 1,
    "site": "example.com",
    "kind": "local-business",
    "required_surfaces": ["robots.txt", "sitemap.xml", "json-ld"],
    "identity": {"schema_types": ["LocalBusiness"], "fields": ["name", "address", "telephone"]},
    "offering": {"schema_types": ["Service"], "fields": ["name", "description"]},
    "url_rules": {"lowercase": True, "trailing_slash": "never", "max_depth": 3},
    "crawler_stance": "open",
    "pages": [{"path": "/", "purpose": "what the business is and where it is"}],
}


class AcceptsValidPlans(unittest.TestCase):
    def test_full_plan(self) -> None:
        self.assertEqual([], plan_format.validate(GOOD_PLAN))

    def test_partial_plan(self) -> None:
        """Every key except plan_version is optional, so a partial plan is valid."""
        self.assertEqual([], plan_format.validate({"plan_version": 1}))

    def test_one_key_at_a_time(self) -> None:
        for key, value in GOOD_PLAN.items():
            with self.subTest(key=key):
                self.assertEqual([], plan_format.validate({"plan_version": 1, key: value}))

    def test_every_generated_plan(self) -> None:
        """What siteplan produces must pass siteplan's own check, for every kind."""
        for kind in plan_format.KINDS:
            with self.subTest(kind=kind):
                intent = site_intent.SiteIntent(
                    kind=kind, site="example.com", origin=(("kind", "--kind"),)
                )
                profile = kinds.apply_intent(kinds.PROFILES[kind], intent)
                self.assertEqual([], plan_format.validate(plan.build(intent, profile)))

    def test_summarise_copes_with_a_partial_plan(self) -> None:
        self.assertIn("plan_version 1", plan_format.summarise({"plan_version": 1}))


class RejectsMalformedPlans(unittest.TestCase):
    def assert_rejected(self, document: object, expected: str) -> list[str]:
        problems = plan_format.validate(document)
        self.assertTrue(problems, f"expected a problem, got none for {document!r}")
        joined = " | ".join(problems)
        self.assertIn(expected, joined)
        return problems

    def test_top_level_must_be_an_object(self) -> None:
        self.assert_rejected([{"plan_version": 1}], "must be a JSON object")

    def test_plan_version_required(self) -> None:
        self.assert_rejected({"site": "example.com"}, "plan_version: required")

    def test_plan_version_must_be_the_supported_integer(self) -> None:
        self.assert_rejected({"plan_version": 2}, "expected 1, got 2")
        self.assert_rejected({"plan_version": "1"}, "expected the integer 1")
        self.assert_rejected({"plan_version": True}, "expected the integer 1")

    def test_unknown_top_level_key(self) -> None:
        self.assert_rejected({"plan_version": 1, "sites": "example.com"}, 'unknown key "sites"')

    def test_a_mistyped_key_is_suggested(self) -> None:
        """A near miss on case or separators gets the right key named in the message."""
        problems = self.assert_rejected(
            {"plan_version": 1, "Site": "example.com"}, 'unknown key "Site"'
        )
        self.assertTrue(any('did you mean "site"' in problem for problem in problems))

    def test_unknown_kind(self) -> None:
        self.assert_rejected({"plan_version": 1, "kind": "shop"}, "kind: expected one of")

    def test_unknown_surface(self) -> None:
        self.assert_rejected(
            {"plan_version": 1, "required_surfaces": ["robots.txt", "humans.txt"]},
            'unknown name "humans.txt"',
        )

    def test_surfaces_must_be_a_list(self) -> None:
        self.assert_rejected(
            {"plan_version": 1, "required_surfaces": "robots.txt"}, "expected a list of strings"
        )

    def test_empty_surfaces_rejected(self) -> None:
        self.assert_rejected({"plan_version": 1, "required_surfaces": []}, "empty list")

    def test_duplicate_surface(self) -> None:
        self.assert_rejected(
            {"plan_version": 1, "required_surfaces": ["robots.txt", "robots.txt"]},
            "duplicate",
        )

    def test_site_must_be_a_bare_domain(self) -> None:
        self.assert_rejected(
            {"plan_version": 1, "site": "https://example.com/path"}, "bare domain"
        )
        self.assert_rejected({"plan_version": 1, "site": ""}, "non-empty string")

    def test_identity_must_be_an_object(self) -> None:
        self.assert_rejected({"plan_version": 1, "identity": ["LocalBusiness"]}, "expected an object")

    def test_identity_unknown_key(self) -> None:
        problems = self.assert_rejected(
            {"plan_version": 1, "identity": {"schemaTypes": ["LocalBusiness"]}},
            'unknown key "schemaTypes"',
        )
        self.assertTrue(any('did you mean "schema_types"' in problem for problem in problems))

    def test_identity_must_carry_something(self) -> None:
        self.assert_rejected({"plan_version": 1, "identity": {}}, "no recognized keys")

    def test_schema_types_must_be_a_list_of_type_names(self) -> None:
        self.assert_rejected(
            {"plan_version": 1, "identity": {"schema_types": "LocalBusiness"}},
            "expected a list of strings",
        )
        self.assert_rejected(
            {"plan_version": 1, "identity": {"schema_types": ["local business"]}},
            "is not a Schema.org name",
        )

    def test_fields_must_be_schema_org_property_names(self) -> None:
        self.assert_rejected(
            {"plan_version": 1, "offering": {"fields": ["opening hours"]}},
            "is not a Schema.org name",
        )
        self.assert_rejected(
            {"plan_version": 1, "offering": {"fields": []}}, "empty list"
        )

    def test_url_rules_shape(self) -> None:
        self.assert_rejected({"plan_version": 1, "url_rules": []}, "url_rules: expected an object")
        self.assert_rejected({"plan_version": 1, "url_rules": {}}, "no recognized keys")
        self.assert_rejected(
            {"plan_version": 1, "url_rules": {"trailing_slash": "sometimes"}},
            'expected "always" or "never"',
        )
        self.assert_rejected(
            {"plan_version": 1, "url_rules": {"max_depth": 0}}, "positive integer"
        )
        self.assert_rejected(
            {"plan_version": 1, "url_rules": {"lowercase": "yes"}}, "expected true or false"
        )

    def test_crawler_stance_vocabulary(self) -> None:
        self.assert_rejected(
            {"plan_version": 1, "crawler_stance": "sometimes"}, "crawler_stance: expected one of"
        )

    def test_pages_shape(self) -> None:
        self.assert_rejected({"plan_version": 1, "pages": {}}, "expected a list of page objects")
        self.assert_rejected({"plan_version": 1, "pages": []}, "empty list")
        self.assert_rejected(
            {"plan_version": 1, "pages": [{"path": "/"}]}, "pages[0].purpose: required"
        )
        self.assert_rejected(
            {"plan_version": 1, "pages": [{"purpose": "x"}]}, "pages[0].path: required"
        )
        self.assert_rejected(
            {"plan_version": 1, "pages": [{"path": "about", "purpose": "x"}]},
            'slash-separated ASCII segments beginning with "/"',
        )
        self.assert_rejected(
            {"plan_version": 1, "pages": [{"path": "/a", "purpose": "x", "title": "y"}]},
            'unknown key "title"',
        )
        self.assert_rejected(
            {
                "plan_version": 1,
                "pages": [
                    {"path": "/a", "purpose": "x"},
                    {"path": "/a", "purpose": "y"},
                ],
            },
            "duplicate path",
        )


class ReadsFiles(unittest.TestCase):
    def test_missing_file(self) -> None:
        with temp_dir() as name:
            data, problems = plan_format.read_plan(Path(name) / "nope.json")
        self.assertIsNone(data)
        self.assertIn("cannot read", problems[0])

    def test_invalid_json(self) -> None:
        with temp_dir() as name:
            path = Path(name) / "site.json"
            path.write_text("{not json", encoding="utf-8")
            data, problems = plan_format.read_plan(path)
        self.assertIsNone(data)
        self.assertIn("not valid JSON", problems[0])

    def test_good_file(self) -> None:
        with temp_dir() as name:
            path = Path(name) / "site.json"
            path.write_text(json.dumps(GOOD_PLAN), encoding="utf-8")
            data, problems = plan_format.read_plan(path)
        self.assertEqual([], problems)
        self.assertEqual([], plan_format.validate(data))


class VocabulariesAgree(unittest.TestCase):
    def test_every_allowed_kind_has_a_profile(self) -> None:
        self.assertEqual(set(plan_format.KINDS), set(kinds.PROFILES))

    def test_every_profile_surface_is_an_allowed_surface(self) -> None:
        for kind, profile in kinds.PROFILES.items():
            with self.subTest(kind=kind):
                for surface in profile.surface_names:
                    self.assertIn(surface, plan_format.SURFACES)

    def test_every_surface_has_a_basis(self) -> None:
        self.assertEqual(set(plan_format.SURFACES), set(kinds.SURFACE_BASIS))

    def test_profiles_use_allowed_stances_and_slash_conventions(self) -> None:
        for kind, profile in kinds.PROFILES.items():
            with self.subTest(kind=kind):
                self.assertIn(profile.crawler_stance, plan_format.CRAWLER_STANCES)
                self.assertIn(profile.urls.trailing_slash, plan_format.TRAILING_SLASH)
                self.assertGreater(profile.urls.max_depth, 0)


if __name__ == "__main__":
    unittest.main()
