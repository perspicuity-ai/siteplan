---
format: perspicuity-work/1
id: sp-project
revision: 1
skill_version: 0.5.0
updated: 2026-09-21
created_at: "2026-09-21T11:56:00-06:00"
updated_at: "2026-09-21T11:56:00-06:00"
record_status: open
work_status: active
---

# Siteplan

The project record: parent of every record in this repository, and the continuing account of what
is true now, what was inherited, what is planned and what was observed. This revision replaces the
template placeholder with the first real basis, selection and plan.

## Current position

Principal and decider: David.

Work owner: Heron (coordinator).

Mode: `Run`. The principal's instruction of 2026-09-21 settles the frame and names three
deliverables in order; this record registers the units that instruction authorises and stops at
the return. No planning stop is needed before the work.

Decision: `selected` — the tool design and plan format in "Selection" below, selected 2026-09-21
by Heron under the principal's delegation of reversible implementation details (AGENTS.md,
Authority). The principal retains acceptance of the return.

Work scope: the first increment of `siteplan` — `python3 -m siteplan new` producing `BRIEF.md`
and `site.json`, `python3 -m siteplan check`, the six kind profiles, `docs/PLAN-FORMAT.md`,
`README.md`, an offline test suite, and real checks in `scripts/check-project.sh`.

Work: revision 1 registers the basis, the selection and the unit plan. No package exists at this
revision: `siteplan/` is absent and `scripts/check-project.sh` is still the template's empty stub.

Outcome: nothing observed yet at this revision. The unit table in Act is an intended result, not a
result, and this record will not report it as one.

Next: Heron picks up U1 (the plan format and its validator) under the pickup plan in Act, then U2
and U3 in order.

Blocked: nothing. Every input U1 needs exists in this repository.

Waiting on: no one. The principal's acceptance of the return is the next move after delivery.

Dependency: none blocking at this revision.

Review due: no timed obligation. R4 and R5 in Review are trigger-based, not dated.

Authority: the principal's instruction of 2026-09-21 (three deliverables: name the coordinator,
register this record, build the tool), within AGENTS.md, Authority — everything inside the project
record's scope is delegated, including reversible implementation details. The principal retains
spending, outbound messages, external agreements and the release word for publication. Nothing in
this increment spends, publishes, deploys, sends, or adds a dependency.

| Stage | began_at | registered_at / exact basis revision | finished_at |
| --- | --- | --- | --- |
| Frame and Decide | 2026-09-21T11:52:00-06:00 | [`CONTEXT.md`](CONTEXT.md) as supplied 2026-09-21; principal's instruction of 2026-09-21 | 2026-09-21T11:56:00-06:00 |
| Act | 2026-09-21T11:56:00-06:00 | revision 1 of this record: unit table, grant and U1 pickup plan | pending |
| Review | 2026-09-21T11:56:00-06:00 | revision 1 of this record: criteria R1–R5 | pending |

## Frame and Decide

### The problem, in the principal's words

From [`CONTEXT.md`](CONTEXT.md) (supplied 2026-09-21): these decisions "are cheap once, at the
start, and expensive later: URL shape and entity model are the two things a site cannot change
without migrations and redirects, and both determine whether a machine can tell what the site is."
Nothing today records them — one of the principal's sites publishes an `Organization` block and no
offering markup, another publishes no structured data at all — "not because anyone decided that,
but because nobody decided anything." The stated purpose is that "the decision is made once, in
writing, before the build."

### Adopted frame

**A plan is a producer/consumer contract between two tools, not a document.** `siteplan` writes the
file; `sitewalk --plan` reads it. That frame decides three things that would otherwise be style
choices: the plan file is the primary artifact and the brief is rendered from the same decisions;
every key is optional because a partial plan must still be usable by a consumer that reads it
later; and the format is versioned because two independently released tools depend on it.

**Reframe considered and rejected.** A broader frame — "generate the site's SEO and AI-visibility
checklist" — would reach more users and would justify a larger catalogue. It is rejected because it
crosses the claim boundary in `CONTEXT.md`: a generated checklist invites the reading that
following it causes an agent to find, understand or recommend the site, and this tool measures
nothing. The adopted frame keeps the deliverable a statement of intent with the basis of each
recommendation visible.

### Fundamental objectives

| # | Objective | Source | Measure, direction, horizon |
| --- | --- | --- | --- |
| O1 | Every new project starts from a brief: the plan file is an input to the build, not a description written afterwards | `CONTEXT.md` §Outcomes 1 | Count of projects whose build is gated on a plan this tool produced; direction up; horizon: the first such project after this increment |
| O2 | The brief is checkable: `sitewalk --plan site.json` reports a built site against the plan it claims to follow | `CONTEXT.md` §Outcomes 2 | A `sitewalk` run against a siteplan-produced file with no shared code; direction: the file is the only coupling; horizon: sitewalk's first run |
| O3 | The claim boundary holds: no output predicts that an agent will find, understand or recommend the site | `CONTEXT.md` §The claim boundary | Every recommendation carries a `published practice` or `our judgement` label, and the brief states the boundary in its own words; checkable by reading any generated brief |
| O4 | Unstated intent is recorded as unstated, never invented | `CONTEXT.md` §What we are deliberately not doing | An input not supplied appears as unstated in the brief, and no recommendation is adjusted for it; checkable by generating with no flags |
| O5 | Deliver this increment: the tool, the format document, the tests and the checks, on the principal's terms | Principal's instruction of 2026-09-21 | `make ci` exits 0, `make records` is clean, `python3 -m unittest discover -s tests -t .` passes offline; horizon: the return of this session |

### Material conditions

| # | Condition | Type | Basis | Affects |
| --- | --- | --- | --- | --- |
| C1 | Python 3.11+, standard library only; a dependency needs a recorded choice | Given | Principal's instruction; `CONTEXT.md` §What we are deliberately not doing | The package layout, the tests, the checks |
| C2 | No crawling and no network from the tool or the tests | Given | `CONTEXT.md` §What we are deliberately not doing; principal's instruction | The kind catalogue must carry its own content; no runtime lookup of schema.org |
| C3 | Runnable as `python3 -m siteplan`; `make ci` runs `scripts/check-project.sh` after `scripts/check_records.sh` | Given | Principal's instruction; `Makefile`, `scripts/ci.sh` | Package at the repository root; the check script becomes the real test runner |
| C4 | `siteplan` owns the plan format and is authoritative; `sitewalk` implements the consumer side and links back | Given | `CONTEXT.md` §The plan file | `docs/PLAN-FORMAT.md` must let a consumer be written without reading this code |
| C5 | The plan file is small: top-level keys only, every key optional, versioned by `plan_version` | Given | `CONTEXT.md` §The plan file; principal's instruction (key list) | The validator's strictness rules; what `check` may reject |
| C6 | The 0.5.0 Perspicuity skill governs the records; the process documents came from a template written against 0.4.0 | Given | `/home/david/.dsh/skills/perspicuity/` (version 0.5.0) read 2026-09-21; principal's instruction | This record's shape (`Run`, `skill_version: 0.5.0`, the work-status list including `in_review`); the template's stale paths are reported, not fixed |
| C7 | Commit locally only: no remote, no push, no publish, no deploy, no spend | Given | Principal's instruction | Commits are local and split into coherent units |
| U1 | Which Schema.org types and properties really exist, and what each published surface's status is | Uncertainty | The catalogue cites published practice from memory; no source is fetched at run time | The catalogue's citations. Resolved by reading the sources named in `docs/PLAN-FORMAT.md` and in the generated brief; a wrong citation is a defect in this increment |
| U2 | Whether `llms.txt` is consumed by any agent, and whether marking up `ReserveAction` or `SearchAction` still has a confirmed consumer | Uncertainty | No evidence available offline; the proposal at `llmstxt.org` carries no standards status | How the brief labels those recommendations. Handling: `llms.txt` is labelled as our judgement with the proposal named; anything without a confirmed consumer is not recommended as a requirement |
| U3 | Whether the six kinds cover the projects the principal will start | Uncertainty | The six come from the principal's instruction, not from an inventory of planned sites | The catalogue's coverage. Reconsideration trigger: the first project whose kind is not among the six |
| A1 | Four intent flags (`sells`, `local`, `publishes`, `takes-bookings`) carry enough of a site's intent to shape the recommendations | Assumption | Our reading of the interviews ahead; unverified | The flag set and the "what changes if you state it" section. Would be challenged if a plan produced here proved wrong at build time in a way traceable to a missing input; the response would be a flag, never a configuration file (`CONTEXT.md` §Success, and what would stop us — scope cap) |
| A2 | A reader of the brief can tell a published claim from a judgement from the label alone | Assumption | Unverified; it is the whole basis of the claim boundary | The label rule in every recommendation. Would be challenged by a reader who could not |

### Alternatives and consequences

Each row is a choice point where a credible alternative existed. The selected option and the reason
are in the last column; the rejected options are named so a later reader does not relitigate them.

| # | Choice point | Alternatives considered | Selected, and the decisive reason |
| --- | --- | --- | --- |
| D1 | Where the per-kind recommendations live | (a) a catalogue in the package's code; (b) a JSON data file loaded at run time; (c) ask a model at run time | **(a)**. (b) needs a second format, a loader and a validator for the loader, and a data file can be edited into an invalid state silently; (c) is a dependency, non-deterministic, and would put an unlabelled judgement behind an authoritative-looking brief. Code is typed, testable and diffable |
| D2 | How the tool is driven | (a) flags with an optional interactive mode; (b) one `--spec input.json`; (c) interactive questions only; (d) a library with no CLI | **(a)**. (b) adds a second format to learn and is a configuration file by another name, which the scope cap forbids; (c) cannot run in a test or a script; (d) has no user surface |
| D3 | One artifact or two | (a) `BRIEF.md` for humans plus `site.json` for machines; (b) JSON only, rendered on demand; (c) the plan embedded in the brief as a fenced block | **(a)**. The brief is the thing a human reads in the repository; a brief that needs a command run to be read is the "written once and never read" failure in `CONTEXT.md`. (c) makes one file serve two parsers and lets the two halves drift when one is edited |
| D4 | Validation strictness | (a) closed vocabularies for kinds and surfaces, Schema.org-shaped but open field names, unknown keys rejected at every level; (b) permissive: ignore unknown keys; (c) fully closed vocabularies including field names | **(a)**. A plan that drifts silently is the failure `CONTEXT.md` names; a rejected plan is visible. (c) would reject legitimate Schema.org properties the catalogue does not emit — for example `servesCuisine`, `hasMenu` — and rejecting a valid plan is a worse failure than accepting an unusual one |
| D5 | Is `plan_version` optional like every other key | (a) required; (b) optional, treated as 1 when absent; (c) optional, with a warning when absent | **(a)**. A file that does not name its format cannot be safely consumed, and (b) is an invented default. Recorded as an interpretation of the principal's "every key optional": the version marker is the format's identity, the plan's content is optional. Flagged for the principal in the report |
| D6 | Unstated inputs in the plan file | (a) the plan carries only design decisions; unstated inputs appear only in the brief; (b) add an `inputs` key to the plan | **(a)**. The key list is fixed by the principal and consumed by another tool; interview answers are not design decisions. The brief records what was and was not stated |
| D7 | Whether a generated file carries a timestamp | (a) no timestamp; (b) a generated-at date | **(a)**. Provenance is the commit, and deterministic output lets the tests compare bytes and lets a rerun with unchanged inputs be a no-op. A wall-clock stamp also makes every regeneration a diff |
| D8 | Which kind profiles to ship | (a) the six the principal named; (b) one universal profile for every site; (c) a larger set including restaurants, marketplaces and docs sites | **(a)**. (b) destroys the product's reason to exist; (c) multiplies the citations each profile owes without a user yet. Reconsideration trigger: the first project whose kind is not one of the six |
| D9 | Where the basis of a recommendation is stored | (a) a label and a reason beside each recommendation in the catalogue, rendered into the brief; (b) a general statement at the top of the brief | **(a)**. `CONTEXT.md` requires the basis per recommendation: "where a recommendation rests on published practice it says so; where it is our judgement it says that instead" |

**The decisive tradeoff.** Coverage against claim discipline. A larger catalogue, more kinds and
more recommended surfaces would be more useful and would look more authoritative — and every added
recommendation needs either a citable source or an explicit `our judgement` label, so breadth is
bought with either research this increment cannot do offline or a weaker boundary. The selected
design keeps the catalogue to the six named kinds, labels every item, and invents nothing about a
site it was not told. What would warrant reconsideration: the first project whose build is gated on
a plan and whose kind is not covered, or a `sitewalk` run that cannot consume a plan produced here.

### Selection

`selected_at` 2026-09-21T11:56:00-06:00. Selected by Heron, work owner, under the principal's
delegation of reversible implementation details (AGENTS.md, Authority); basis: revision 1 of this
record. The principal remains the decider for the increment as a whole and accepts or rejects the
return; the choices above are reversible implementation details, recorded so the rejected
alternatives are not relitigated.

The choice: build `siteplan` as a standard-library Python package under `siteplan/`, runnable as
`python3 -m siteplan`, with `new` (flags or `--interactive`) writing `BRIEF.md` and `site.json`,
`check` validating a plan file against `docs/PLAN-FORMAT.md`, a per-kind catalogue carrying one
labelled basis per recommendation, and an offline test suite wired into `make ci` through
`scripts/check-project.sh`.

### Decision index

| Record | Owner | State | Depends on |
| --- | --- | --- | --- |
| `sp-project` (this record) | Heron | selected, active | — |
| A sub-record per kind profile | — | deliberately not split in this increment: one intention, one release, and the profiles are the content of the selection above | the first consumer of the plan file |
| The process-document record `AGENTS.md` asks for | — | not filed in this increment; see "Deviations and fences" | the principal's decision on the template's 0.4.0 conventions |

## Act

Grant, registered with revision 1 and before any code: **Heron** is granted U1–U3. Included: the
package, `docs/PLAN-FORMAT.md`, the tests, the real checks in `scripts/check-project.sh`, and local
commits. Excluded: any network use, any new dependency, any deployment or publication, any spend,
any outbound message, any edit to `CONTEXT.md` or to the template's process documents, and any
recommendation that cannot be given a basis label. Stop condition: the increment is returned for
acceptance, or a unit needs something outside this grant.

| # | State | Result | Inputs / dependencies | Owner, timing | Done when | Actual evidence |
| --- | --- | --- | --- | --- | --- | --- |
| U1 | picked up | The plan format and its validator: `docs/PLAN-FORMAT.md` plus `siteplan check` | The principal's key list; `CONTEXT.md` §The plan file | Heron, this session | The criteria in the U1 pickup plan below | Pending |
| U2 | planned | The kind catalogue and the brief: `siteplan new`, producing `BRIEF.md` and `site.json` for all six kinds, by flags or `--interactive` | U1 | Heron, this session | Every kind generates; unstated inputs appear as unstated; every recommendation carries a basis label | Pending |
| U3 | planned | Project surfaces: `README.md`, real `scripts/check-project.sh`, `make ci` exiting 0, `make records` clean, coherent local commits | U1, U2 | Heron, this session | `make ci` exits 0 at the delivered commit; the record carries the evidence | Pending |

### Pickup plan, U1 (registered before implementation)

Route: (1) write `docs/PLAN-FORMAT.md` as the specification — the eleven keys, the one required
key, the nested shapes, the closed vocabularies, the exit codes and the authority of the document;
(2) implement `siteplan/format.py` against that document; (3) implement `siteplan check FILE`, one
message per fault, non-zero exit on any fault; (4) write the tests for the accepted case and each
malformed class; (5) run `python3 -m unittest discover -s tests -t .` from the repository root,
with no network.

Acceptance criteria, registered before the work:

1. `docs/PLAN-FORMAT.md` names every key, states which are required, defines the nested shapes and
   the closed vocabularies, and states that this project owns the format.
2. `python3 -m siteplan check FILE` exits 0 on a plan the document calls valid — including a plan
   whose only key is `plan_version` — and prints a one-line summary.
3. It exits non-zero, with a message naming the offending key, for every malformed class: unknown
   top-level key, missing or wrong `plan_version`, unknown kind, unknown surface, wrong type for a
   nested object, unknown key inside a nested object, empty list where a list is meaningful,
   malformed page entry, malformed Schema.org name, unreadable file and invalid JSON.
4. The tests run with no network access, and the package imports no network module.
5. `siteplan` is byte-compiled by `scripts/check-project.sh`, which runs the tests; `make ci` exits
   0.

Not in U1: the brief renderer and the kind catalogue (U2); `README.md` and the check script's final
form (U3).

### Provisional pickup notes for U2 and U3

Registered now as scope, to be confirmed at their own pickup under the 0.5.0 rule that a later
pickup plan depends on what the earlier unit found. U2: the catalogue is data in
`siteplan/kinds.py`, one frozen profile per kind, each carrying its labelled recommendations; the
brief renders those recommendations and the plan is built from the same profile, so the two cannot
disagree; the "what changes if you state it" section is computed by applying each unstated flag in
isolation and diffing the profile, not written by hand. U3: `scripts/check-project.sh` byte-compiles
the package and runs the unit tests; `README.md` states what the tool does, how to run it and what
it does not do.

## Review

| # | Criterion | Evidence source | Owner, window or trigger | Finding | Response |
| --- | --- | --- | --- | --- | --- |
| R1 | Delivery: `make ci` exits 0 and `make records` reports no mechanical issue, at the delivered commit | `make ci` output; the commit hash | Heron, at the return | Pending | — |
| R2 | Delivery: all six kinds generate a brief and a plan, and `check` accepts every generated plan | `python3 -m unittest discover -s tests -t .` | Heron, at the return | Pending | — |
| R3 | Delivery: unstated intent appears as unstated; every recommendation carries `published practice` or `our judgement`; the brief states the claim boundary in its own words | Assertions over generated files in the test suite | Heron, at the return | Pending | — |
| R4 | Benefit, later: a new project's build is gated on a plan this tool produced | Repository evidence of the first gated build | David — trigger: the first project that uses a plan; no date | Pending | — |
| R5 | Benefit, later: `sitewalk --plan site.json` consumes a siteplan-produced file unchanged, with no shared code | The first `sitewalk` run against a plan file | The sitewalk owner (unnamed until that project is staffed) — trigger: sitewalk's first run against a plan file | Pending | — |

R1–R3 are delivery acceptance: they can be settled at the return by a mechanical check. R4 and R5
are observations about the world and cannot be settled here; they are recorded so the increment is
not mistaken for evidence that the outcome was achieved. Delivery is not benefit.

## Deviations and fences

- **The template's first task is not this session's task.** `AGENTS.md` §Your first task and
  `docs/KICKOFF.md` direct the first worker to revise `AGENTS.md`, `CONTEXT.md` and
  `docs/RECORDS.md` and to file `docs/records/<date>-process-record-conventions.md`, with feature
  work waiting on acceptance. The principal's instruction of 2026-09-21 scoped this session
  differently — name, record, tool — and directed that template disagreements be reported instead
  of fixed. Both the revision pass and that record are therefore not filed here.
- **Template defects found and reported, not fixed** (detail in the return, not in this record):
  the skill path `/home/david/.codex/skills/perspicuity/SKILL.md` is stale beside the installed
  0.5.0 skill; the process documents describe the 0.4.0 record shape with no mode in
  `Current position`; `scripts/check_records.sh` looks for the checker at a path that currently
  resolves, but only through a symlink nothing documents; `AGENTS.md`'s standing constraints are
  still the template's placeholder; and `docs/RECORDS.md` lists a project code `sp` for "this
  template" that is now this project's code.
- **Deliberately absent from this increment:** code generation, scaffolding, site templates,
  crawling, any network call, any dependency, any configuration file, accounts and external APIs.
  `CONTEXT.md` §What we are deliberately not doing is the fence, and the tests check the network
  part mechanically.
- **`docs/ARCHITECTURE.md` remains the template placeholder.** The tool's design decisions are in
  this record. Filling a second document with the same decisions would create the drift the corpus
  rule exists to prevent; the next increment should either make that file the settled-technical
  view or delete it.

## Changes

Revision 1, 2026-09-21T11:56:00-06:00. Created: replaced the template placeholder with the project
record — frame, objectives, material conditions, alternatives, selection, grant, unit plan, U1
pickup plan and review criteria. Source: [`CONTEXT.md`](CONTEXT.md) as supplied 2026-09-21; the
principal's instruction of 2026-09-21; [`docs/ACTORS.md`](docs/ACTORS.md) naming Heron (commit
`1ea70a1`). Reason: the corpus rule requires the basis, the choice and the review criteria to exist
before the work that depends on them. Affects: U1–U3.
