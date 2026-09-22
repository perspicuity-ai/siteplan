"""The label discipline: a `published practice` claim must name the source it rests on.

This is the check that makes the labels mean something. Without it, a recommendation can be written
with a practice label and no source, and nothing fails — which is how the catalogue's citations went
wrong the first time (four materially wrong claims out of fifteen checked, found by a fact-check
rather than by the suite).

What it catches: a new or edited `published practice` claim that names no source in `SOURCES`, or a
surface whose basis text names none. What it does not catch: whether the named source says what the
claim says. That is what the audit in `docs/CITATIONS.md` is for, and no mechanical check can do it.
"""

from __future__ import annotations

import unittest

from siteplan import kinds

SOURCE_KEYS = tuple(name for name, _ in kinds.SOURCES)


def named_sources(text: str) -> list[str]:
    """The source keys a piece of text names, by exact key."""
    return [key for key in SOURCE_KEYS if key in text]


class PracticeClaimsNameTheirSource(unittest.TestCase):
    def test_every_surface_basis_names_its_source(self) -> None:
        for surface, (basis, why) in kinds.SURFACE_BASIS.items():
            with self.subTest(surface=surface):
                self.assertTrue(why.strip())
                if basis == kinds.BASIS_PRACTICE:
                    self.assertTrue(
                        named_sources(why),
                        f"{surface}: labelled published practice but names no source in SOURCES",
                    )

    def test_every_practice_advice_names_its_source(self) -> None:
        for kind, profile in kinds.PROFILES.items():
            for item in kinds.advice_for(profile):
                with self.subTest(kind=kind, group=item.group):
                    self.assertTrue(item.why.strip(), f"{kind}.{item.group}: no reason given")
                    if item.basis == kinds.BASIS_PRACTICE:
                        self.assertTrue(
                            named_sources(item.why),
                            f"{kind}.{item.group}: labelled published practice but names no "
                            f"source in SOURCES: {item.why[:80]}...",
                        )

    def test_every_source_has_a_usable_identifier(self) -> None:
        for name, where in kinds.SOURCES:
            with self.subTest(source=name):
                self.assertTrue(name.strip())
                self.assertIn("http", where, "a source must be identifiable, not just described")

    def test_the_labels_are_only_the_two_that_exist(self) -> None:
        labels = {basis for basis, _ in kinds.SURFACE_BASIS.values()}
        for profile in kinds.PROFILES.values():
            labels.update(item.basis for item in kinds.advice_for(profile))
        self.assertEqual({kinds.BASIS_PRACTICE, kinds.BASIS_JUDGEMENT}, labels)

    def test_a_judgement_does_not_dress_itself_as_a_source(self) -> None:
        """A judgement may name a source for a fact inside it, but not as its basis."""
        for kind, profile in kinds.PROFILES.items():
            for item in kinds.advice_for(profile):
                if item.basis != kinds.BASIS_JUDGEMENT:
                    continue
                with self.subTest(kind=kind, group=item.group):
                    head = item.why.split(". ")[0]
                    self.assertNotIn(
                        "is the published pattern",
                        head,
                        f"{kind}.{item.group}: a judgement leads with a published-pattern claim",
                    )


class TheCatalogueIsFullyLabelled(unittest.TestCase):
    """Every rendered recommendation group has exactly one advice item: the briefs depend on it."""

    GROUPS = ("identity_types", "identity_fields", "offering_types", "offering_fields",
              "urls", "crawler", "pages")

    def test_each_group_has_exactly_one_item(self) -> None:
        for kind, profile in kinds.PROFILES.items():
            items = kinds.advice_for(profile)
            for group in self.GROUPS:
                with self.subTest(kind=kind, group=group):
                    self.assertEqual(
                        1, len([item for item in items if item.group == group])
                    )


if __name__ == "__main__":
    unittest.main()
