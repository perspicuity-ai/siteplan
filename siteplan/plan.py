"""The machine-readable plan file: built from a profile, and rendered deterministically.

``docs/PLAN-FORMAT.md`` is the specification. Key order here matches the order the document lists,
because a plan file is read by people too, and a stable order makes two runs diff cleanly.
"""

from __future__ import annotations

import json

from .format import PLAN_VERSION
from .intent import SiteIntent
from .kinds import Profile


def build(intent: SiteIntent, profile: Profile) -> dict:
    """Build the plan document. Keys with nothing to say are omitted rather than defaulted."""
    plan: dict = {"plan_version": PLAN_VERSION}
    if intent.site:
        plan["site"] = intent.site
    plan["kind"] = profile.kind
    plan["required_surfaces"] = list(profile.surface_names)
    plan["identity"] = {
        "schema_types": list(profile.identity_types),
        "fields": list(profile.identity_fields),
    }
    plan["offering"] = {
        "schema_types": list(profile.offering_types),
        "fields": list(profile.offering_fields),
    }
    plan["url_rules"] = {
        "lowercase": profile.urls.lowercase,
        "trailing_slash": profile.urls.trailing_slash,
        "max_depth": profile.urls.max_depth,
    }
    plan["crawler_stance"] = profile.crawler_stance
    plan["pages"] = [
        {"path": path, "purpose": purpose} for path, purpose in profile.pages
    ]
    return plan


def render(plan: dict) -> str:
    """Serialise a plan. Deterministic: same inputs, same bytes, no timestamp."""
    return json.dumps(plan, indent=2, ensure_ascii=True) + "\n"
