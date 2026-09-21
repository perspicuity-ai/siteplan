---
format: perspicuity-work/1
id: sp-project
revision: 5
skill_version: 0.5.0
updated: 2026-09-21
created_at: "2026-09-21T11:56:00-06:00"
updated_at: "2026-09-21T13:33:00-06:00"
record_status: open
work_status: submitted
---

# Siteplan

The project record: the parent of every record in this repository, and the continuing account of
the basis, the plan and the result. Revision 2 is the Statement of Work; revision 3 records the
principal's selection and the grant of U1; this revision returns U1 for acceptance.

**U1 is delivered and awaits acceptance. U2–U4 are not granted.** Nothing in the draft package is
ratified by this return; U2 and U3 judge it.

## Current position

Principal and decider: David.

Work owner: Heron (coordinator).

Mode: `Run`, unchanged since the principal's ratification of 2026-09-21, which arrived before
13:22:07 and was registered at 13:23:14: U1 was granted, and the run carried that unit to its
return. `Plan` was the mode between 12:20 and the ratification, when the deliverable was the
Statement of Work; revisions 2 and 3 hold that basis. U2 may use the plan already registered rather
than re-planning, but it may not start without its own grant.

Decision: `selected` — course A1, the format-first two-file tool, at basis revision 2 of this
record. Selected by David on 2026-09-21; the selection, the answers he gave with it and the grant
he registered are in "Selection" and "Answers to the open questions". Recommendation and selection
are separate entries below, as the method requires.

Work scope: U1 — delivered at `757eef3` and `7db7c03`, and now awaiting the principal's acceptance.
The scope for the next run is U2, the citation audit, which is not granted.

Work: revision 3 registered the grant at 13:23:14. U1 was carried out between then and 13:28:49,
when the return was committed: `docs/PLAN-FORMAT.md` frozen as `plan_version` 1; 45 conformance
fixtures published;
`siteplan check` and its tests brought to the document, which exposed six defects in the draft;
`scripts/check-project.sh` replaced with the real checks. The return, with its evidence and the gaps
it leaves, is in Act.

Outcome: U1's delivery is complete — `make ci` exits 0 through real checks at the delivered
revision — and no benefit is observed. No project has used a plan; no consumer has read one; the
format's implementability is an assessor's reading, not an implementation.

Next: David accepts U1 or returns it with findings, and separately grants or refuses U2. A pending
move outside this run: the freeze notice goes to Moss, who owns `sitewalk`, and it must travel
through the principal, because a worker here cannot message another repository's session.

Blocked: nothing in the U1 return. U2 cannot start until its grant is registered.

Waiting on: David — acceptance of U1, and the grant of U2.

Dependency: David's acceptance of U1, and his grant for U2. Owner David; resolving step: his reply
to this record.

Review due: no timed obligation. R5–R7 are trigger-based and are stated in Review.

Authority: U1's grant, registered at revision 3 and now complete. No authority is held for U2, U3 or
U4; for any change to the format (versioning rule 5 makes a consumer-breaking change the principal's
decision); or for contacting another repository. The principal retains spending, outbound messages,
external agreements, the release word, and the selection of courses and units.

| Stage | began_at | registered_at / exact basis revision | finished_at |
| --- | --- | --- | --- |
| Frame and Decide | 2026-09-21T11:52:23-06:00 | [`CONTEXT.md`](CONTEXT.md) as supplied 2026-09-21; principal's instructions and answers of 2026-09-21 | 2026-09-21T13:23:14-06:00 |
| Act | 2026-09-21T13:23:14-06:00 | revision 3 of this record: U1 granted, pickup immediately after | 2026-09-21T13:28:49-06:00 |
| Review | 2026-09-21T13:28:49-06:00 | criteria R1–R8, registered at revision 2 before the work | pending — U1 awaits acceptance |

## Frame and Decide

### The problem, in the principal's words

From [`CONTEXT.md`](CONTEXT.md) (supplied 2026-09-21): the decisions "are cheap once, at the start,
and expensive later: URL shape and entity model are the two things a site cannot change without
migrations and redirects, and both determine whether a machine can tell what the site is." Nothing
today records them; two of the principal's sites publish no offering markup, or no structured data
at all, "not because anyone decided that, but because nobody decided anything." The purpose is that
"the decision is made once, in writing, before the build."

The underlying problem is not "there is no generator". It is that a site's intent is never written
down in a form a later check can hold it to, so the site drifts from whatever was intended and
nobody can tell. A generator is one means; a written checklist is another. Both are on the table
below.

### Adopted frame

**A plan is a producer/consumer contract between two tools, and a brief is a statement of intent.**
`siteplan` writes the file, `sitewalk --plan` reads it, and the file is the only coupling. That
frame decides three things that would otherwise be taste: the plan file is a first-class artifact
with its own specification; the brief and the plan are rendered from the same decisions; and every
recommendation carries a label saying whether it rests on published practice or on our judgement.

**Reframe considered and rejected.** "Make the tool produce a site, or at least a template, so the
plan is followed by construction." Rejected: `CONTEXT.md` fences it (no code generation, no
scaffolding), and it would make the tool responsible for the drift it exists to detect.

### Fundamental objectives

| # | Objective | Source | Measure, direction and horizon |
| --- | --- | --- | --- |
| O1 | Every new project starts from a brief: the plan is an input to the build, not a description written afterwards | `CONTEXT.md` §Outcomes 1 | A plan file committed in a project before its first build commit; direction up; horizon: the first project started after ratification |
| O2 | The brief is checkable: `sitewalk --plan site.json` reports a built site against the plan it claims to follow | `CONTEXT.md` §Outcomes 2 | A `sitewalk` run against a siteplan-produced file with no shared code; horizon: sitewalk's first run |
| O3 | The claim boundary holds: no output predicts that an agent will find, understand or recommend the site | `CONTEXT.md` §The claim boundary | Every recommendation carries one label, and the label matches a source that was read or says `our judgement`; checkable by reading any generated brief |
| O4 | Unstated intent is recorded as unstated, never invented | `CONTEXT.md` §What we are deliberately not doing | An input not supplied appears as unstated, and no recommendation is adjusted for it; checkable by generating with no flags |
| O5 | The format survives its consumer: a change here does not silently break `sitewalk` | `CONTEXT.md` §The plan file | Zero unversioned breaking changes; measure: the change log in `docs/PLAN-FORMAT.md` against `plan_version`; horizon: sitewalk's first two releases |
| O6 | The increment the principal ratifies is delivered on the terms he ratifies | principal's instruction of 2026-09-21 | Units U1–U4 accepted against R1–R4; horizon: this increment |

O5 is new at this revision: revision 1 treated the format as one decision among nine, and the
coupling it creates is material enough to carry an objective of its own.

### Material conditions

| # | Condition | Type | Basis | Affects |
| --- | --- | --- | --- | --- |
| C1 | Python 3.11+, standard library only; a dependency needs a recorded choice | Given | Principal's instruction; `CONTEXT.md` §What we are deliberately not doing | Layout, tests, checks; U1, U3, U4 |
| C2 | The tool fetches nothing: no crawling, no network at run time | Given | `CONTEXT.md` ibid.; principal's instruction | The catalogue must carry its own text; U3; and see OQ2, which is about workers reading sources, not about the tool |
| C3 | Runnable as `python3 -m siteplan`; `make ci` runs `scripts/check-project.sh` after `scripts/check_records.sh` | Given | Principal's instruction; `Makefile`, `scripts/ci.sh` | Package layout; U3, U4 |
| C4 | `siteplan` owns the plan format and is authoritative; `sitewalk` implements the consumer side and links back | Given | `CONTEXT.md` §The plan file | U1; the stability rules under "Recommendation" |
| C5 | The plan file is small: top-level keys only, every key optional, versioned by `plan_version` | Given | `CONTEXT.md` §The plan file; principal's instruction (key list) | U1; see OQ3, which asks how literally to read "every key optional" |
| C6 | Records follow Perspicuity 0.5.0; the template's process documents were written against 0.4.0 | Given | The installed skill at `/home/david/.dsh/skills/perspicuity/` (0.5.0), read 2026-09-21; principal's instruction | This record's shape; the deviations reported at the end |
| C7 | Commit locally only: no remote, no push, no publish, no deploy, no spend | Given | Principal's instruction | All units |
| C8 | A draft `siteplan/` package and `tests/` suite exist uncommitted, written ahead of this plan and reviewed by nobody | Given | The working tree, measured 2026-09-21 before 12:09:46 | U1, U3, U4: they judge it. Its measurements are usable; its decisions are not ratified |
| C9 | A 15-item fact-check of the catalogue's citations was run on 2026-09-21 against primary sources; it found four claims materially wrong or too strong in the tree, and two needing qualification. None is corrected | Given | The delegated fact-check of 2026-09-21, sources fetched live; the defects are listed in Act | U2, and O3: a catalogue whose citations are wrong cannot carry evidence labels |
| U1 | Whether the remaining catalogue claims hold up: the checked sample was chosen by me, not at random | Uncertainty | Only the checked items are verified | U2's estimate and O3. Resolved by: auditing the remaining labelled claims and recording the date each source was read |
| U2 | Whether any consumer reads `llms.txt`. The proposal claims platform adoption; Google's documentation says such files are not needed for Search and do not affect visibility | Uncertainty | Two conflicting claims, and no measurement either way | Whether `llms.txt` is recommended as a requirement or as a labelled bet; OQ8. Resolved by: evidence of a consumer, or by demoting it to a stated judgement. Unresolved at revision 3; U2 carries it |
| U3 | Whether the six kinds cover the projects the principal will start | Uncertainty | The six come from the principal's instruction, not from an inventory of planned sites | U3's scope; OQ8 |
| U4 | When `sitewalk` will exist, and who owns it, so that the format is exercised by a real consumer | Uncertainty | Resolved at revision 3: `sitewalk` exists, is owned by Moss, and is at its own ratified SOW stage (OQ6) | O2, O5, R6. Now a dependency to coordinate, not an unknown: R6's owner is Moss |
| U5 | Whether anyone reads the brief. This is the objective the tool exists for and the one no artifact can demonstrate | Uncertainty | No project has run this tool | O1, R5, R7. Resolved only by the first project that uses a plan, and by what it does next |
| A1 | Four intent flags (`sells`, `local`, `publishes`, `takes-bookings`) carry enough of a site's intent to shape the recommendations | Assumption | Our reading; unverified | U3's flag set. Challenged by a plan that proves wrong at build time in a way traceable to a missing input; the response would be a flag, never a configuration file (`CONTEXT.md` scope cap) |
| A2 | A reader can tell a published claim from a judgement from the label alone | Assumption | Unverified; it is the whole basis of the claim boundary | O3. Challenged by a reader who could not. Cheap test: ask one reader of a generated brief |
| A3 | The principal wants a machine-readable plan file, not only a written brief | Assumption | Inferred from `CONTEXT.md` §Outcomes 2 and the key list in the principal's instruction | O2 and course A1 itself. Directly challenged by OQ1: course A2 would satisfy O1 without it |

### Alternatives

Five complete courses. A1 is what the existing draft represents; A5 is not building a tool at all.

**A1 — Two-file tool, format first.** `siteplan new` writes `BRIEF.md` (labelled recommendations)
and `site.json` (the plan a consumer reads); `siteplan check` validates a plan against
`docs/PLAN-FORMAT.md`; six kind profiles supply the recommendations. Order of work: format document
and fixtures, then the catalogue audit, then the generator, then the project surfaces. Delivers
O1–O6.

**A2 — A written checklist in the project template, no tool.** One file added to the
`project-setup` template: a design checklist a worker fills in by hand for each new project —
which Schema.org types, which surfaces, what URL shape, what crawler stance. No code, no format, no
consumer. It delivers O1 weakly (a human writes it), fails O2 and O5 outright, and O3 and O4 rest
on the template staying disciplined. Its advantage is that it costs an afternoon and can be tried
on the next project immediately.

**A3 — Brief-only generator, no plan file.** `siteplan new` writes only `BRIEF.md`; no `check`, no
format, no coupling to `sitewalk`. Delivers O1, O3 (labels are rendered) and O4. Fails O2 and O5 —
there is nothing for a consumer to read — and drops the machine-readable half of the product.

**A4 — Format and validator only; briefs written by hand.** `docs/PLAN-FORMAT.md`,
`siteplan check`, and conformance fixtures; no generator. A consumer could be built immediately
against a frozen format, and the format is exercised by hand-written plans. Delivers O2 and O5;
delivers O1 poorly (a hand-written plan per project is the status quo that failed) and O3 not at
all (nothing enforces the label discipline).

**A5 — Do not build it; close the project.** Keep the record, delete the draft, and revisit only if
a project needs a brief. Honest if the real problem is that nobody wanted a plan; it delivers
nothing and costs nothing further. `CONTEXT.md`'s failure test — "if the brief is written once and
never read ... the honest outcome is to delete the tool" — is an argument for building it only if
the first use is likely to be read.

### Consequences

Each cell: whether the course serves the objective, with `E` where the basis is evidence gathered
this session and `J` where it is judgement. `?` marks a gap that could change the choice.

| Objective | A1 two-file tool | A2 template checklist | A3 brief only | A4 format only | A5 stop |
| --- | --- | --- | --- | --- | --- |
| O1 brief before the build | serves (J) | serves weakly (J): a hand-filled file is skipped when busy | serves (J) | fails (J): the status quo | fails by construction |
| O2 checkable by sitewalk | serves (E): the draft validates 60 generated plans, and a consumer has a file to read | fails (J): nothing machine-readable | fails (J) | serves (E): that is all it does | fails |
| O3 label discipline | serves (E): two labels, one per recommendation, checked by test — but C9 shows four claims are wrong (E) | weak (J): nothing enforces it | serves partially (E): no plan to check against | fails (J) | n/a |
| O4 unstated stays unstated | serves (E): implemented and tested, with the unstated table computed by diffing | weak (J): a human may fill gaps | serves (E) | n/a | n/a |
| O5 format survives its consumer | serves (J): stability rules exist, unexercised until sitewalk runs (?) | n/a | n/a | serves (J) | n/a |
| O6 on the principal's terms | (?) depends on OQ1–OQ4 | cheap (E): one afternoon | cheap (J) | moderate (J) | zero (E) |
| Cost to acceptance | 3.5–4.5 sessions (J, weak basis — see the estimates) | under 1 session (J) | 1–1.5 sessions (J) | 1 session (J) | 0 |

**Material gaps, left visible.** (a) No evidence that any consumer reads `llms.txt`; the two
sources conflict (U2). (b) No evidence about whether a brief is read, which is O1 itself (U5).
(c) The estimate basis is one short drafting session plus one fact-check, which is thin: the draft
was written quickly and reviewed by nobody (C8). (d) The right size of the citation audit is
unknown because the checked sample was not random (U1). (e) Whether `sitewalk` will exist in time
to exercise the format is unknown (U4).

**The decisive tradeoff.** A1 accepts a permanent coupling — a format owned here and consumed in
another repository — and a citation burden: every recommendation must be checkable or labelled as
judgement, which C9 shows is real work. A2 and A3 are much cheaper and would answer the smaller
question ("does anyone want a brief?") faster. They are rejected as the *first* increment because
`CONTEXT.md`'s second outcome is the checkable half, and because the principal has already
specified the plan file's keys — but the comparison above is deliberately close enough that he
could rationally choose A2 as a trial. What would warrant reconsidering A1: no project starting
from a brief within one horizon of ratification (R5), or a consumer that cannot be written from
the format document alone (R1).

### Recommendation

**Course A1, with the citation audit ahead of the generator.** Concretely: specify and freeze the
format with its fixtures (U1); audit every labelled claim in the catalogue, correcting or demoting
what does not hold (U2); complete and correct the generator against the audited catalogue (U3);
then the project surfaces and real checks (U4).

The reason is the order of trust. The plan file is the artifact another repository must implement
against, so it should be the thing settled first; and the brief's only claim to value is that its
labels mean something, which C9 has already shown they do not yet. Building the generator first
would scale a catalogue whose evidence is unverified — which is what the uncommitted draft did.

The tradeoff this accepts: the visible artifact lags. The principal sees no tool until U3, because
the first two units produce a document and an audit rather than software. The compensating gain is
that the generator is then built once, against a format that is already the contract and a
catalogue that has been checked.

**David ratifies. Heron does not select.** If he prefers A2 as a cheap trial, the measurements of
the draft stay valid and U1–U4 are replaced by a one-file change in the template repository — which
would require amending this record.

### Selection

`selected_at` 2026-09-21, before 13:22:07 — the exact arrival was not observed; registered at 13:23:14 in commit `3d436a6`. Decider: David, the principal. Basis: revision 2 of this
record — the frame, objectives O1–O6, conditions C1–C9, the five courses and the comparison above.

**Course A1 is selected**, as recommended, with two qualifications the principal added: v1 ships
only the kinds whose citations pass the audit (OQ8), and the CLI contract is fixed as exit 0 clean,
1 for findings or an invalid plan, 2 for a usage error, with no `--force` (OQ5). U1 is granted; U2,
U3 and U4 are not, and each comes back for its own grant at pickup.

The reason recorded for the selection is the one recommended: the format is the artifact another
repository must implement against, and the brief's value rests on labels that the fact-check has
already shown cannot yet be trusted, so the format is settled and the catalogue audited before the
generator is completed. The tradeoff accepted is the same one: no visible tool until U3.

Two consequences follow that this record must carry, because they were not in the recommendation:

1. **The format's kind vocabulary and the generator's coverage are different questions.** The
   format defines the closed set of kind names a plan may carry; the generator offers a profile for
   a kind. OQ8 reduces the second, not the first: a kind whose profile fails the audit stops being
   offered by `new`, and stays a valid name in a plan. Removing a name from the format's closed set
   would be a breaking change under rule 3 below, which is a cost the audit should not have to pay.
2. **The `check` command changes with the format.** `plan_version` is required and the closed
   vocabularies are closed (OQ3, OQ4). The draft already behaves this way, so U1 confirms rather
   than rewrites that behaviour — but the document is the authority from here, and where the two
   differ the document wins and the code changes.

### How the plan format stays stable (the sitewalk coupling)

A format owned by one repository and consumed by another is a coupling, and the coupling is the
whole design. The rules this SOW would bind the project to, and which U1 must write into
`docs/PLAN-FORMAT.md`:

1. **The document is authoritative, not the code.** A consumer is expected to implement from the
   document alone; if a reader cannot, the document is defective.
2. **Additive optional keys keep `plan_version`.** A new optional key is a compatible change,
   because every key except the version marker is optional.
3. **Removing a key, changing a key's meaning, or changing an allowed value requires a
   `plan_version` bump.** The closed vocabularies (kinds, surfaces, stances) count as meaning.
4. **A consumer that does not implement the version it reads must refuse, not guess.** The
   producer's `check` rejects any `plan_version` other than the one it implements.
5. **Every change to the document carries a dated change-log entry naming the consumer-side
   effect.** A change that breaks a consumer is a decision for the principal, because it costs work
   in another repository.
6. **Conformance fixtures are published with the format**: a minimal valid plan and a malformed one
   with its expected message, so the consumer can test against the format without our code.
7. **The producer is strict; the consumer may be tolerant.** `siteplan check` rejects unknown keys,
   so drift is caught where it is created. Whether `sitewalk` warns or fails on them is sitewalk's
   decision, recorded there.

The open question this leaves: OQ4, the open-or-closed field vocabulary. Until it is answered,
rule 3 cannot be written completely, which is why U1 cannot start before ratification.

### How we would know whether the brief was read

The tool's benefit is unobservable from inside this repository, so the plan names the evidence in
advance, and the outcome that would disconfirm it.

| Evidence | What it would show |
| --- | --- |
| A plan file committed in a new project's repository before its first build commit | The brief was an input, not a description written afterwards — O1 |
| A `sitewalk --plan site.json` run recorded against that project | The two tools connect through the file — O2 |
| The built site's URL shape and pages matching `url_rules` and `pages` | The plan constrained the build rather than decorating it |
| The tool invoked at the start of a project, not after the build | A leading indicator, visible before any outcome |
| The brief written once and never referenced again; a plan committed after the build; a built site contradicting its own plan; nobody running either check | Disconfirming. Response per `CONTEXT.md`: delete the tool rather than maintain a document nobody follows — R7 |

## Act

### What already exists, ahead of this plan

Written between 11:54 and 12:00 on 2026-09-21, after revision 1's grant and before this plan, and
left uncommitted. It is recorded here as evidence about feasibility and cost, and as work this plan
must be free to reject. **Nothing here is ratified by being described.**

| Artifact | State, measured 2026-09-21 before 12:09:46 | Bearing on this SOW |
| --- | --- | --- |
| `siteplan/`, 8 modules, 2,150 lines | Uncommitted. CLI, six-kind catalogue (1,096 lines), validator, brief and plan renderers | Shows A1 is feasible and gives U3 a measured starting point — if A1 is ratified |
| `tests/`, 7 files, 1,008 lines, 80 tests | Uncommitted. 80 run, 2 fail; both failures are in test expectations written minutes earlier (a suggestion message and an allowed-value ordering), not in observed tool behaviour | Not evidence of correctness; evidence about where the work is |
| `docs/PLAN-FORMAT.md` | Absent | U1 exists because the authoritative document does not |
| `README.md` | Absent | U4 |
| `scripts/check-project.sh` | Before 12:09:46 it was the template stub that exited 0 without looking at the code; commit `55dbada` replaced it with a stub that fails, so `make ci` now fails until real checks exist | U1 fills it in. The earlier green `make ci` established nothing, which is the point the stub now makes for itself |
| Generated output | All 6 kinds and 60 kind/flag combinations produce a plan the in-tree validator accepts. A `local-business` brief is 9,091 bytes / 125 lines; its plan is 1,360 bytes / 69 lines. Output is deterministic and needs no network | Feasibility evidence for U3, and part of why the estimates are as low as they are |
| Catalogue citations | Four claims materially wrong or too strong: `OnlineStore` described as a subtype of `Store` (it sits under `Organization > OnlineBusiness`); Google's local-business guidance described as "asking for" `telephone` (recommended; only `name` and `address` are required); merchant-listing guidance described as requiring `availability` (recommended, not required); `llms.txt` described as having no consumer (the proposal claims platform adoption, and Google states the files are not needed for Search). Two further claims need qualification: `robots.txt` is a Proposed Standard whose compliance is voluntary, and `/sitemap.xml` is a recommended location rather than a mandated name | C9. The strongest argument for putting U2 ahead of U3 |

The draft also chose, without ratification, a set of implementation decisions — where the
recommendations live, how the CLI is driven, validation strictness, whether the generated files
carry a timestamp, and others. They are recorded in revision 1 (`df09827`) and visible in the
uncommitted code. This SOW judges the *deliverable* and its acceptance criteria, not those choices;
a ratified design that differs discards them.

### Units

| # | State | Result | Inputs / dependencies | Owner | Done when | Estimate |
| --- | --- | --- | --- | --- | --- | --- |
| U1 | **returned** — delivered `757eef3`, `7db7c03`; awaits acceptance | `docs/PLAN-FORMAT.md` and its conformance fixtures: the authoritative format and stability rules, a minimal valid plan, a malformed one, and `check` brought to the document | Selection at revision 3; OQ2–OQ5 answered; the draft validator as evidence only | Heron | Met, on the evidence in "U1 return" below | Actual: 1 session, as estimated |
| U2 | planned — not granted | Citation audit of every labelled recommendation in the catalogue, corrections applied, unverifiable claims demoted to `our judgement`; v1 ships only the kinds and surfaces whose citations pass | OQ2 answered (network for sources, not for the tool); the fact-check method of 2026-09-21; the grant, at pickup | Heron | Every `published practice` label names a source that was read, with the date; the method and the unverified remainder are recorded; the shipped kind set is named | 1–2 sessions; wide |
| U3 | planned — not granted | `siteplan new` completed against the audited catalogue and the ratified CLI contract: the audited kinds, four flags and interactive mode, `BRIEF.md` and `site.json`, the unstated rule, and `--force` removed | U1, U2 | Heron | R3 and R4 pass; tests run offline; `make ci` exits 0 through real checks | 1 session |
| U4 | planned — not granted | Project surfaces: `README.md` (what it does, how to run it, what it does not do), coherent local commits | U1–U3 | Heron | `make ci` and `make records` exit 0 at the delivered commit, and the record carries the evidence | 0.5 session |

**Grant, registered at revision 3 and before any U1 work.** Decider: David, 2026-09-21; basis
revision 2. **Heron** is granted **U1 only**. Included: `docs/PLAN-FORMAT.md`; the conformance
fixtures; bringing `siteplan check` and the tests that cover the format to the document; filling in
`scripts/check-project.sh` with the real checks; an independent implementability assessment by a
worker who did not write the document; and local commits. Excluded: the citation audit (U2), any
change to `siteplan new`'s behaviour or flags (U3), `README.md` (U4), any new dependency, any
network use by the tool, publishing, deploying, spending or outbound messages, and changes to
`CONTEXT.md` or to another repository. Stop condition: U1 is returned for acceptance, or it needs
something outside this grant.

**Two items the grant excludes, recorded so they are not lost.** The ratified CLI contract (OQ5)
contradicts the draft in `new`: it still offers `--force` and still exits 3 on an internal defect.
Bringing `new` to the contract is U3's work, and this record carries both as proposals rather than
fixing them inside U1. The draft's overwrite behaviour also has to be decided at U3 — the
recommendation there will be to refuse and exit 2, since with no `--force` there is no way to force.

**Estimates and their basis.** One "session" is a focused worker session, not a working day. The
basis is weak, and stated so it can be discounted: the draft's 3,158 lines and 80 tests were
written in about six minutes of wall-clock time, and one delegated fact-check covered 15 claims.
The estimates are for *acceptance*, not drafting — the draft has two failing tests, four known
wrong claims, no format document and no README, which is the difference between written and done.
Total 3.5–4.5 sessions, judgement, wide. The estimate that would move most is U2: the audited sample
was not random, so the true defect rate in the catalogue is unknown.

### Pickup plan, U1 (registered at planning time)

Route: (1) apply the principal's answers (OQ3–OQ5), since each changes the document; (2) write
`docs/PLAN-FORMAT.md` — the nine keys, the one required key and its reason, the nested shapes, the
open/closed rule, the stability rules above, the exit codes and the change log; (3) write the
conformance fixtures; (4) bring `siteplan check` and its tests to the document; (5) fill in
`scripts/check-project.sh`; (6) have an assessor who did not write it read the document and try to
write the consumer's validation from it alone, and record what they could not determine.

`picked_up_at` 2026-09-21T13:23:14-06:00, actor Heron, immediately after the grant was registered
at revision 3: the pickup plan was registered at revision 2, before the work, and this line records
who started it and when.

Acceptance criteria, registered before the work:

1. The document names every key, states which are required, defines each nested shape and each
   closed vocabulary, and states that this project owns the format.
2. A reader who cannot see our code can implement the consumer's validation from the document
   alone; the assessor's written finding says so, or names what was missing.
3. `check` accepts every plan the document calls valid — including one whose only key is
   `plan_version` — and rejects every class the document calls invalid, with a message naming the
   offending key and a non-zero exit.
4. The versioning and change-log rules are present, and rule 3 (what requires a version bump) is
   stated without a gap.
5. The fixtures are published with the format and are usable by another repository's tests.

Not in U1: the catalogue audit (U2), the generator (U3), the project surfaces (U4).

### U1 return, 2026-09-21T13:28:49-06:00

**Delivered.** `docs/PLAN-FORMAT.md` freezes `plan_version` 1 — the nine keys, the one required key
and its reason, the nested shapes, the open/closed rule the principal ratified, the reporting form,
the exit codes, the versioning rules and the change log. `docs/fixtures/plan-conformance.json`
carries 45 cases for another repository's tests. `siteplan/format.py` now implements every rule the
document states. `scripts/check-project.sh` runs the real checks. Exact revisions: `757eef3` (the
deliverable) and `7db7c03` (the lines the assessment left open). The draft it was built on is
`0129d28`, committed unratified.

**Evidence, per acceptance criterion.**

| # | Criterion | Evidence |
| --- | --- | --- |
| 1 | Document names every key, the required one, the shapes and the closed vocabularies, and ownership | `tests/test_conformance.py::DocumentCoversTheImplementation` alarms if a key or vocabulary value is left undocumented, against `format.py`; the document was also read by the assessor, who found the key table and the open/closed rule clear |
| 2 | A reader without the code can implement the consumer's validation | The independent assessment below; it is a finding, not acceptance |
| 3 | `check` accepts what the document calls valid and rejects what it calls invalid, naming the key | 45 conformance cases, each asserting the valid flag, the key path and the producer's message; exit codes verified by hand: `0` on a minimal plan, `1` on faults, `2` on a usage error |
| 4 | Versioning and change-log rules present, rule 3 complete | `## Versioning` (seven rules) and `## Change log` in the document; asserted by test |
| 5 | Fixtures published and usable by another repository | `docs/fixtures/plan-conformance.json`: `format`, `plan_version`, and per case `valid`, `invalid_keys`, `expect`; described in the document's "Conformance fixtures" section |

`make ci` exits 0 at `7db7c03`: records clean, package and tests byte-compile, the 45 fixtures
parse, 90 tests pass offline, `python3 -m siteplan --version` answers. All 60 kind/flag
combinations still generate plans the tightened validator accepts.

**Independent assessment.** Tern, a worker who did not write the document and was instructed to read
that file only — no code, no tests, no record — read it four times, and its reading is the evidence
for acceptance criterion 2:

1. **First read:** `sufficient with gaps`, thirteen named gaps. They were real, and they are what the
   amendment at `7db7c03` fixed: the page path grammar, the `<placeholder>` rule and its depth
   contribution, the host-name grammar, trimming, case-sensitivity, the fault count, malformed page
   elements, `purpose` validation, which nested keys exist, and the tension between "unknown keys are
   invalid" and a tolerant consumer.
2. **Second read:** `sufficient with gaps` again — four residual items (duplicate-fault counting, an
   unknown version's fault count, the consumer's exit status, and the fixtures not being inlined) and
   one new item: the fault-path example `identity.schemaTypes` could read as a key of the format. All
   five were closed by stating them.
3. **Third read**, of the revision reconciled with the consumer at `f19dbdf`: **no** sign-off. It
   found three faults the earlier readings had not: the `plan_version` and Structure sections stated
   the producer's rule in universal terms; the note-versus-fault question was unsettled; and the
   worked-consumer paragraph made the document depend on a piece of another repository's code.
4. **Fourth read**, of the delivered revision at `fe8433b`: **`SIGN-OFF: yes`**, with one residual
   tension recorded — rule 4 treats an absent or mistyped version as a fault while the worked
   paragraph calls unknown versions and keys notes; rule 6 resolves the key case, and rule 4 is
   explicit about the version case. It reports no blocking gap for an implementer who has never seen
   either codebase.

The fourth read is of the revision that was delivered, which the second was not: `f19dbdf` and
`fe8433b` changed the two consumer rules and their scope after the second reading. A sign-off is a
reading, not an implementation: no consumer has been written from the document alone, and Moss has
not read it.

**What U1 exposed in the draft.** Six defects, none of which the draft's own tests caught:

1. No cross-key consistency: `pages` deeper than `url_rules.max_depth` were accepted, so a plan
   could contradict itself and still validate.
2. The page path rule was "begins with `/`, no whitespace", which accepted `//a`, `/a//b`,
   `/pricing?plan=pro`, `/a/b/`, two placeholders in one path, `<Slug>` and non-ASCII characters.
3. The host rule was "no whitespace, no `/`, no `:`", which accepted `example..com` and
   `-example.com`; and it trimmed the value before checking it, so `" example.com"` silently became
   valid rather than being reported.
4. Unknown nested keys were reported against the containing object (`identity: unknown key
   "schemaTypes"`) instead of the offending key's path (`identity.schemaTypes`), contradicting the
   reporting form the document promises.
5. Faults in a path said only what was wrong, never what a valid path is.
6. Two test expectations were themselves wrong — a "did you mean" suggestion the code never made,
   and an allowed-value ordering. U1 fixed the tests, not the code: the document requires neither.

**Deviations from the plan as registered.**

- U1's result said "two conformance fixtures". The delivered file is one published vector file with
  45 cases, because another repository's tests want a file they can load rather than two loose
  plans. The intent — published, usable, exercised here — is unchanged; the wording was mine.
- The grant included the `check` command and its tests, not the catalogue. The catalogue's six wrong
  or overstated citations (C9) are untouched and remain U2's work; `new` still offers `--force` and
  exits 3, which the ratified contract forbids, and that remains U3's.

**Not established by this unit.** That the format's readings are the ones Moss needs to implement
against — nobody from `sitewalk` has read the document, and the freeze notice has not been
delivered. That a consumer can in fact be written from it: the assessment is a reading, not an
implementation. That the choices the document settles (a path never carrying a trailing slash, the
ASCII path charset, punycode host names) are the right ones; they were mine to make, they are
recorded, and rule 3 makes them costly to change. That the catalogue's recommendations rest on
sources that were read; that is U2.

### The consumer already exists, and it forced an amendment, 2026-09-21T13:29:41-06:00

Before sending the freeze notice, I read the consumer rather than describing it from memory:
`sitewalk/sitewalk/plan.py` and that project's `RECORD.md`. **`sitewalk --plan` is already built and
its behaviour is ratified by the principal** — units U1–U3 and U5 are delivered there. It reads the
nine keys; it enforces `required_surfaces` and `identity.schema_types`; it names `offering`,
`url_rules`, `crawler_stance`, `pages` and `identity.fields` as *not checked* with the reason for
each; it reports the `plan_version` it read; and it treats a version or a key it does not know as a
note rather than a fault, because the principal answered that project's Q3 that way.

The document I had just frozen said the opposite in two rules: rule 4 required a consumer to refuse
an unimplemented version, and rule 6 called a tolerant consumer a deviation. Delivered as written,
the authoritative format would have contradicted the only consumer of it, and the contradiction
would have been discovered by Moss rather than by me. All three earlier readings — mine, Tern's two —
missed it, because all three read the document in isolation; the check that found it was opening the
consumer's code.

**Amended** at `f19dbdf`: rule 4 now says a consumer must not guess and must not pretend — it may
read a version it does not implement, must report the version it read, and must not present the
result as a check against a version it does not know; rule 6 now says a consumer may carry an
unknown key and report it as *not checked*, naming it and the reason, and must never present an
unchecked key as met. The producer's rules are unchanged: `plan_version` required, `check` rejects
another version or an unknown key. A change-log entry records it, as rule 5 requires, and no valid
plan changed.

**Consequence for the return.** Tern's third reading is of this revision; its first two assessed the
revision at `7db7c03`, which differs in exactly these two rules. The change was made to match a
ratified consumer, not for clarity, and it is the principal's to confirm, because the two rules
govern a promise made to another repository.

**Freeze notice for Moss, to be relayed by the principal** — this repository cannot message another
repository's session:

1. `plan_version` 1 is frozen at `f19dbdf`; the document is `docs/PLAN-FORMAT.md` in this repository,
   and `docs/fixtures/plan-conformance.json` holds 45 cases his tests can load.
2. Nothing sitewalk already reads has changed: the nine keys, their shapes and the closed
   vocabularies are as they were. What changed is the format's statement about *consumers*: his
   implemented behaviour — read what you know, name what you did not check, never report a pass on
   an unreadable plan — is now the document's rule rather than a deviation from it.
3. Two asymmetries are deliberate and worth his reading: `siteplan check` is stricter than
   `sitewalk --plan` (it rejects an unknown key; a consumer may note it), and the fixture file is
   the shared artifact, so the invalid cases in it can be run through his validator to compare
   readings.
4. Anything in the document he cannot implement, or disagrees with, is a format question: it belongs
   in sitewalk's record and comes back here, because a change that breaks his consumer is the
   principal's decision under rule 5.

### Provisional notes for U2–U4

Confirmed at their own pickup, per the 0.5.0 rule that a later pickup plan depends on what the
earlier unit found. U2: audit by source, not by memory; record the date each source was read;
demote anything unverifiable; name the kinds and surfaces that pass, because that set is what v1
ships. U3: a flag that changes nothing must not claim a change; the unstated table stays computed by
diffing rather than written by hand; and `new` comes to the ratified CLI contract, which means
removing `--force` and the exit code 3, and deciding what an existing output file means (proposal:
refuse with a clear message and exit 2). U4: `README.md` states what the tool does not do, and the
unratified parts of the draft are either ratified by then or removed.

## Out of scope

- **Site generation, scaffolding or templates of any kind.** `CONTEXT.md` fences it: the moment it
  writes templates it is a framework, a different project.
- **Crawling, fetching or measuring a live site**, and any network use by the tool at run time.
  The tool asks questions and writes files.
- **Implementing `sitewalk`.** A different repository with its own record; this project supplies
  the format and the fixtures.
- **Accounts, external APIs, telemetry, dependencies.** Standard library only.
- **Publishing, deploying, spending or contacting anyone.** The principal retains all four.
- **Editing the template repository** (`project-setup`) or its process documents, even where this
  record reports them as behind the skill. It is a different repository with its own owner.
- **A configuration file.** `CONTEXT.md`'s scope cap: if the first version cannot produce a
  complete brief in one run, cut questions rather than add configuration.

## Open questions for the principal

| # | Question | Owner | What it blocks |
| --- | --- | --- | --- |
| OQ1 | Which course: A1 (as recommended), A2 (template checklist), A3 (brief only), A4 (format only) or A5 (stop)? | David | Everything. Each answer changes the units, this record, and the estimate |
| OQ2 | May a worker read published sources on the network while auditing citations? The tool itself stays offline | David | U2. Without it, every `published practice` label is an unverified memory and O3 fails |
| OQ3 | Is `plan_version` required, contrary to the literal "every key optional"? This record recommends yes: it is the format's identity | David | U1's acceptance criteria and the consumer contract |
| OQ4 | Are `identity.fields` and `offering.fields` a closed vocabulary, or any Schema.org-shaped name? This record recommends open-but-shaped, so a legitimate property the catalogue does not emit is not rejected | David | U1, and `sitewalk`'s validation |
| OQ5 | Is the CLI contract acceptable as the draft has it — exit codes 0/1/2/3, `--force` to overwrite, and the pair `--not-local` for the negative? | David | U1 and U3 acceptance criteria |
| OQ6 | Who owns `sitewalk`, and when will it consume the format? | David | O2, O5, R6, and the point at which the format can be frozen |
| OQ7 | Which project will first be gated on a plan, so R5 has a trigger? | David | R5, and the success test in `CONTEXT.md` |
| OQ8 | Are the six kinds the right coverage for the first version? This record recommends shipping fewer, audited, over six unaudited | David | U3's scope and U2's size |

### Answers received, 2026-09-21 (before 13:22:07)

Recorded verbatim in substance, with the effect each has on the plan. The questions above stay as
they were registered; these answers are the current state.

| # | Answer | Effect |
| --- | --- | --- |
| OQ1 | **A1 is selected**, and U1 is granted | The selection is above; U2–U4 return for their own grants |
| OQ2 | **Yes** — workers may read published sources; the tool itself stays offline | U2 may cite sources it actually read. The constraint in C2 is about the tool's run time, not about research |
| OQ3 | **`plan_version` is required.** "Every key optional" applies to content keys, not the version gate, because the consumer cannot otherwise tell which contract it validates | U1 writes it as the format's single required key |
| OQ4 | **Closed where the consumer acts, open elsewhere.** `kind` and `required_surfaces` are closed lists — `sitewalk` branches on their values, so an unknown value is a bug. Schema.org vocabulary stays open: unknown values are ignored, not rejected. The rule must be stated in the document | U1 states the rule as a property of the format. Fields and types follow the Schema.org half: open, shape-checked. The other closed vocabularies the consumer branches on — `crawler_stance`, `url_rules.trailing_slash` — follow the closed half |
| OQ5 | **Exit 0 clean, 1 for findings or an invalid plan, 2 for a usage error. No `--force`.** Keep `--not-local` | U1 states the contract and keeps `check` to three codes; the draft's exit 3 and `--force` are U3 proposals, recorded in Act |
| OQ6 | **`sitewalk` exists, owned by Moss, ratified at its own SOW stage.** Tell Moss what is being frozen before the format hardens | R6's owner is Moss; this record carries the freeze notice to be relayed, since a worker here cannot message another repository's session |
| OQ7 | **Open, and it is the principal's.** It does not block U1 | R5 stays trigger-based with no date |
| OQ8 | **Only kinds whose citations pass the audit ship in v1.** Four wrong claims in fifteen is not a rate to publish under a `published practice` label; two audited kinds beat six unaudited | U2's result sets the shipped kind set; U3 implements it. The format's kind vocabulary stays the six names (see Selection, consequence 1) |

Two answers create work this record must keep visible rather than absorb silently: the freeze notice
to Moss (OQ6), and the kind-coverage split between the format and the generator (OQ8).

## Review criteria

Registered before any work. Delivery acceptance (R1–R4) is separate from benefit (R5–R7); R8 is the
format's own obligation.

| # | Criterion | Evidence source | Owner, window or trigger | Finding | Response |
| --- | --- | --- | --- | --- | --- |
| R1 | Delivery: the format document is complete enough for an implementer who cannot read our code | An assessor who did not write it, against acceptance criterion 2 | David or a named independent assessor, at the U1 return | **Independent finding (Tern, 2026-09-21, four readings, code unseen): `SIGN-OFF: yes` on the delivered revision `fe8433b`**, with one residual tension it recorded. The first two readings found thirteen gaps and five residual items, all now stated in the document; the third refused sign-off on three faults, all fixed; the fourth is on the revision that was delivered | Awaiting David's acceptance. A read by Moss as the actual consumer is the check left; a fifth by Tern would add little, since it has now read the delivered text |
| R2 | Delivery: every `published practice` label cites a source that was read, with the date; nothing unverified is labelled as practice | The audit record, and a sample re-read of the sources | Heron returns; the assessor samples at the U2 return | Not started: U2 is not granted | — |
| R3 | Delivery: `new` and `check` behave as the format document says, for every kind and flag combination, offline | The test suite, and a run from a clean checkout | Heron, at the U3 return; `make ci` exits 0 through real checks | Partly settled at U1: `check` conforms and `make ci` now exits 0 through real checks. `new` is unchanged and still contradicts the ratified contract (`--force`, exit 3) | Carry to U3, where `new` is brought to the contract |
| R4 | Delivery: unstated intent is never filled in, and the unstated table matches what the catalogue would change | Generated output checked against the catalogue by test | Heron, at the U3 return | Not started; the draft's implementation is unratified | — |
| R5 | Benefit: a new project's build is gated on a plan file committed before the build | That project's git history | David, trigger: the first project started after ratification (OQ7); no date | Not observable: no project has started from a plan | — |
| R6 | Benefit: `sitewalk --plan` consumes a siteplan-produced file unchanged, with no shared code | The first `sitewalk` run against a plan file | Moss, owner of `sitewalk` (OQ6) | **Partly settled, and not by a run.** `sitewalk --plan` already exists and is ratified; reading its `plan.py` is what found that two of this document's rules contradicted its behaviour, now reconciled at `f19dbdf`. No plan has been passed between the two tools end to end, and Moss has not read the frozen document | Deliver the freeze notice (text in the return). The remaining check is a siteplan-produced plan through `sitewalk --plan` |
| R7 | Disconfirming: the brief is written once and never read, or the built site contradicts its plan | The first gated project's history, and its `sitewalk` run | David, trigger: that project's first deploy | Pending; no project has used a brief | If it holds, reconsider the tool's existence rather than maintain the document (`CONTEXT.md` §Success, and what would stop us) |
| R8 | The format does not break its consumer without a version bump | The change log in `docs/PLAN-FORMAT.md`, against `plan_version` and the consumer's releases | Heron at each format change; David for a breaking change | Satisfied so far, trivially: `plan_version` 1 is the first freeze, with one change-log entry and no later change | — |

Delivery is not benefit. R1–R4 can be settled at the return by reading artifacts and running
checks; R5–R7 are observations about the world and cannot be settled here. Recording them now is
what stops a passing check from being reported as a working product.

## The grant, as registered

The request at revision 2 asked for exactly this and was granted on 2026-09-21; the grant is
recorded beside U1 in Act, which is where it governs the work. In summary: **U1 only**, inside the
fences the Statement of Work registered, with U2–U4 to return for their own grants at pickup.

What the principal retains, unchanged: spending, outbound messages, external agreements, the release
word, the selection of courses, and the grant of every later unit. What revision 2 explicitly did
not request, and this record still does not hold: any new dependency; any network use by the tool;
publishing, deploying, spending or outbound messages; changes to `CONTEXT.md` or to another
repository; implementing `sitewalk`; and ratification of the draft package in the working tree.

## Process-document propagation, 2026-09-21

Commit `55dbada` ("Bring the process documents to Perspicuity 0.5.0", by the principal) replaced
`AGENTS.md`, `docs/RECORDS.md` and `docs/records/README.md` with the template's 0.5.0 versions. It
touched no record of mine. Three things in it change this project's conditions:

- **`scripts/check-project.sh` now fails as a stub**, so `make ci` fails until it holds real checks.
  This is the right failure: the previous stub let `make ci` pass while tests failed. Filling it in
  is part of U1, which is where this record's earlier note about U4 was overtaken.
- **`scripts/check_records.sh` probes the known skill locations** rather than one hard-coded path, so
  the record check no longer skips silently. `make records` currently passes with no mechanical
  errors.
- **The deviations this record reported at revision 2 are resolved**: the stale skill path, the
  0.4.0 field set, the placeholder standing constraints, the mis-assigned project code, and the
  process-record requirement in `docs/records/README.md` are all gone. The report of them stands as
  the finding that prompted the propagation; nothing here needs fixing now.

## Changes

Revision 5, 2026-09-21T13:33:00-06:00. Changed: two amendments to the delivered format, both after
the U1 return and both inside U1's grant, and the record that carries them. `f19dbdf` reconciled the
consumer rules with the consumer that already exists: `sitewalk --plan` is built and ratified, its
tolerant reading of unknown versions and keys is the principal's own answer to that project's
question, and rules 4 and 6 had said the opposite — a document at odds with its only consumer, found
by reading the consumer's code before sending the freeze notice. `fe8433b` scoped the producer's
rules apart from the consumer's after Tern's third reading refused sign-off on the universal wording
of the `plan_version` and Structure sections, the unsettled note-versus-fault question, and the
document appearing to depend on another repository's code. Tern's fourth reading, of the delivered
revision, is `SIGN-OFF: yes`. The record also now carries the freeze notice for Moss, the assessment
history in four readings, and the review findings for R1 and R6. Source: `f19dbdf`, `fe8433b`, the
consumer at `sitewalk/sitewalk/plan.py`, and Tern's four findings. Reason: the format is a coupling,
and a rule that contradicts the ratified consumer is a defect in the format, not in the consumer.
Preserved: revisions 4, 3, 2 and 1 stand as they were written, including the timestamps corrected
below. Affects: the format's two consumer rules; R1 and R6; and the freeze notice now due to Moss.

**Timestamp correction, same revision.** Revisions 2 to 4 were written with clock times that were
estimated rather than read: 12:26 for revision 2; 13:24 and 13:26 for the selection and the pickup;
13:58 and 14:04 for the return; 14:20 for the amendment. The observed times — the commit times in
`git log --format=%cI` — are 12:09:46, 13:23:14, 13:23:14, 13:28:49, 13:28:49 and 13:29:41, and
this revision replaces them. The principal's ratification arrived before 13:22:07, which was read
from the clock, and its exact minute was never observed, so `selected_at` now says that instead of
asserting 13:12. "Measured 2026-09-21T12:22" is corrected the same way: the measurement was taken
before 12:09:46. The wrong values remain in the history of revisions 2 to 4 and are corrected here
rather than silently.

Revision 4, 2026-09-21T13:28:49-06:00. Changed: the record now carries the U1 return — the delivered
artifacts with their exact revisions (`757eef3`, `7db7c03`), the evidence for each of the five
acceptance criteria, the two readings by the independent assessor with the gaps it found and what
the document now states, the six defects U1 exposed in the draft, two deviations from the plan as
registered, and what the unit does not establish; the review findings for R1, R3, R6 and R8, with
the rest unchanged as not started or not observable; the unit table (U1 returned) and the current
position (delivery complete, awaiting acceptance; the freeze notice to Moss still pending). Source:
the working tree at `7db7c03`, `make ci` at that revision, the hand-verified exit codes, and the
assessor's two findings. Reason: a return records what was delivered, against the criteria
registered before it, and keeps delivery separate from benefit. Preserved: revision 3 holds the
selection, the principal's answers and the grant; revision 2 the Statement of Work; revision 1
(`df09827`) the earlier frame and selections. Affects: U1 (returned), R1, R3, R6, R8, and the U2
grant now pending.

Revision 3, 2026-09-21T13:23:14-06:00. Changed: the mode, from `Plan` to `Run`, on the principal's
ratification — U1 is granted, so this run carries it to its return; and the record, which now
records the selection (David, 2026-09-21, basis revision 2), the grant
registered beside U1, the registration of U1's pickup, the principal's answers to OQ1–OQ8 and their
effects, the two consequences of the selection (the format's kind vocabulary is not the generator's
coverage; `check` changes with the format), the resolved material conditions, and the
process-document propagation at `55dbada`. Source: the principal's ratification of 2026-09-21 and
the answers given with it; commit `55dbada`. Reason: register the choice and the grant before the
work that depends on them. Preserved: revision 2 holds the Statement of Work, its five courses, its
comparison, its recommendation and the estimates; revision 1 (`df09827`) holds the earlier frame
and the D1–D9 selections. Neither is deleted; both remain the basis of record for how this
increment was chosen. Affects: U1 (granted), U2–U4 (planned), R1–R8, and the format being frozen.

Revision 2, 2026-09-21T12:09:46-06:00. Changed: the mode, from `Run` to `Plan`, on the principal's
instruction of 2026-09-21 — the deliverable became a Statement of Work and the selection was
reserved to him; and the record, amended into that Statement of Work: five complete courses of
action including not building a tool at all; a consequence comparison with evidence and judgement
marked and the gaps left visible; a recommendation and the tradeoff it accepts; the unratified
draft recorded in Act with its measurements and its known defects; units U1–U4 with estimates and a
U1 pickup plan; out of scope; eight open questions; criteria R1–R8; and the grant requested.
Source: the principal's instruction of 2026-09-21; the working-tree measurements of
2026-09-21 before 12:09:46; the delegated fact-check of 2026-09-21. Reason: work was done ahead of a ratified
plan, and a plan that cannot reject it is a receipt rather than a plan. Preserved: revision 1
(`df09827`) holds the earlier frame, objectives O1–O5, material conditions C1–C7, the D1–D9
implementation selections made under the earlier grant, and the earlier review criteria R1–R5; this
revision supersedes them for future work without deleting them from history. Affects: U1–U4,
R1–R8, OQ1–OQ8, and any decision about the draft package.
