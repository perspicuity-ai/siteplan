---
format: perspicuity-work/1
id: sp-project
revision: 2
skill_version: 0.5.0
updated: 2026-09-21
created_at: "2026-09-21T11:56:00-06:00"
updated_at: "2026-09-21T12:26:00-06:00"
record_status: open
work_status: waiting
---

# Siteplan

The project record and, at this revision, the **Statement of Work** for the first increment. It is
the parent of every record in this repository.

**This revision recommends; it does not select.** David ratifies. No unit below is granted, and
nothing in the working tree is ratified by being described here.

## Current position

Principal and decider: David.

Work owner: Heron (coordinator).

Mode: `Plan`, changed from `Run` at 2026-09-21T12:20:00-06:00 on the principal's instruction of
2026-09-21: the deliverable is a Statement of Work, and the run stops when the plan is registered
and the grant is requested. `Run` was correct for revision 1, which carried a settled scope: the
principal's earlier instruction named three deliverables and the record registered the units for
them. The principal has since reserved the selection, so this revision prepares the basis and
recommends, and does not select. The earlier mode and its grant are preserved in revision 1
(commit `df09827`).

Decision: `recommended` — course A1, the format-first two-file tool, at revision 2 of this record.
The recommendation and the reasoning are in "Recommendation"; the selection is David's.

Work scope: the Statement of Work for the first increment of `siteplan`, ending at the principal's
ratification of the recommendation and of a grant for U1. The work it authorises has not started.

Work: revision 1 registered the frame, the design alternatives and a selection made under an
earlier grant; it is preserved in commit `df09827`. Between that commit and this revision, a draft
package and test suite were written and left uncommitted, ahead of the plan that would have
authorised them. This revision measures that draft, records it as unratified work in Act, and
builds the plan that must be able to reject it. Measurements taken 2026-09-21 at 12:22.

Outcome: nothing observed about the world. The draft generates files; no project has used one, and
no consumer has read one. The unit table is an intended result, not a result.

Next: David ratifies or amends course A1 and the grant for U1, answering the open questions that
change the plan. As a separate pending move, Heron picks up U1 once that grant is registered.

Blocked: no unit may start. The missing input is the principal's ratification, and behind it the
answers to OQ1–OQ4, which change U1's acceptance criteria.

Waiting on: David.

Dependency: David's ratification of the recommendation and the U1 grant — owner David, resolving
step: his reply to this record. Nothing else is missing.

Review due: no timed obligation. R5–R7 are trigger-based and are stated in Review.

Authority: at this revision, none to act. Revision 1's grant (`df09827`) authorised the naming, the
record and the tool as instructed then; the principal has changed the mode, which supersedes it for
work not yet accepted. This revision asks for a new grant. The principal retains spending, outbound
messages, external agreements and the release word, and now also the selection among courses.

| Stage | began_at | registered_at / exact basis revision | finished_at |
| --- | --- | --- | --- |
| Frame and Decide | 2026-09-21T11:52:00-06:00 | [`CONTEXT.md`](CONTEXT.md) as supplied 2026-09-21; principal's instructions of 2026-09-21 | 2026-09-21T12:26:00-06:00 |
| Act | 2026-09-21T12:26:00-06:00 | revision 2 of this record: units U1–U4, estimates, U1 pickup plan | pending — no unit is granted |
| Review | 2026-09-21T12:26:00-06:00 | revision 2 of this record: criteria R1–R8 | pending |

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
| C8 | A draft `siteplan/` package and `tests/` suite exist uncommitted, written ahead of this plan and reviewed by nobody | Given | The working tree, measured 2026-09-21T12:22 | U1, U3, U4: they judge it. Its measurements are usable; its decisions are not ratified |
| C9 | A 15-item fact-check of the catalogue's citations was run on 2026-09-21 against primary sources; it found four claims materially wrong or too strong in the tree, and two needing qualification. None is corrected | Given | The delegated fact-check of 2026-09-21, sources fetched live; the defects are listed in Act | U2, and O3: a catalogue whose citations are wrong cannot carry evidence labels |
| U1 | Whether the remaining catalogue claims hold up: the checked sample was chosen by me, not at random | Uncertainty | Only the checked items are verified | U2's estimate and O3. Resolved by: auditing the remaining labelled claims and recording the date each source was read |
| U2 | Whether any consumer reads `llms.txt`. The proposal claims platform adoption; Google's documentation says such files are not needed for Search and do not affect visibility | Uncertainty | Two conflicting claims, and no measurement either way | Whether `llms.txt` is recommended as a requirement or as a labelled bet; OQ8. Resolved by: evidence of a consumer, or by demoting it to a stated judgement |
| U3 | Whether the six kinds cover the projects the principal will start | Uncertainty | The six come from the principal's instruction, not from an inventory of planned sites | U3's scope; OQ8 |
| U4 | When `sitewalk` will exist, and who owns it, so that the format is exercised by a real consumer | Uncertainty | No record of sitewalk's staffing or timing beyond its own `CONTEXT.md` | O2, O5, R6. Resolved by: OQ6 |
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

| Artifact | State, measured 2026-09-21T12:22 | Bearing on this SOW |
| --- | --- | --- |
| `siteplan/`, 8 modules, 2,150 lines | Uncommitted. CLI, six-kind catalogue (1,096 lines), validator, brief and plan renderers | Shows A1 is feasible and gives U3 a measured starting point — if A1 is ratified |
| `tests/`, 7 files, 1,008 lines, 80 tests | Uncommitted. 80 run, 2 fail; both failures are in test expectations written minutes earlier (a suggestion message and an allowed-value ordering), not in observed tool behaviour | Not evidence of correctness; evidence about where the work is |
| `docs/PLAN-FORMAT.md` | Absent | U1 exists because the authoritative document does not |
| `README.md` | Absent | U4 |
| `scripts/check-project.sh` | Still the template's stub, so `make ci` exits 0 *without looking at the code* | The green check establishes nothing about the draft; U4 |
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
| U1 | planned — not granted | `docs/PLAN-FORMAT.md` and its conformance fixtures: the authoritative format and stability rules, a minimal valid plan, a malformed one | `CONTEXT.md` §The plan file; OQ3, OQ4, OQ5 answered; the draft validator as evidence only | Heron | The U1 pickup plan below | 1 session; 2 if the strictness model changes |
| U2 | planned — not granted | Citation audit of every labelled recommendation in the catalogue, corrections applied, unverifiable claims demoted to `our judgement` | OQ2 answered (network for sources, not for the tool); the fact-check method of 2026-09-21 | Heron | Every `published practice` label names a source that was read, with the date; the method and the unverified remainder are recorded | 1–2 sessions; wide |
| U3 | planned — not granted | `siteplan new` and `check` completed against the audited catalogue: six kinds, four flags and interactive mode, `BRIEF.md` and `site.json`, the unstated rule | U1, U2 | Heron | R3 and R4 pass; tests run offline; `make ci` exits 0 through real checks | 1 session |
| U4 | planned — not granted | Project surfaces: `README.md` (what it does, how to run it, what it does not do), real `scripts/check-project.sh`, coherent local commits | U1–U3 | Heron | `make ci` and `make records` exit 0 at the delivered commit, and the record carries the evidence | 0.5 session |

**Estimates and their basis.** One "session" is a focused worker session, not a working day. The
basis is weak, and stated so it can be discounted: the draft's 3,158 lines and 80 tests were
written in about six minutes of wall-clock time, and one delegated fact-check covered 15 claims.
The estimates are for *acceptance*, not drafting — the draft has two failing tests, four known
wrong claims, no format document and no README, which is the difference between written and done.
Total 3.5–4.5 sessions, judgement, wide. The estimate that would move most is U2: the audited sample
was not random, so the true defect rate in the catalogue is unknown.

### Pickup plan, U1 (registered at planning time)

Route: (1) answer OQ3–OQ5, since each changes the document; (2) write `docs/PLAN-FORMAT.md` — the
nine keys, the one required key and its reason, the nested shapes, the closed vocabularies, the
stability rules above, the exit codes and the change log; (3) write the two conformance fixtures;
(4) bring `siteplan check` and its tests to the document; (5) have an assessor who did not write it
read the document and try to write the consumer's validation from it alone, and record what they
could not determine.

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

### Provisional notes for U2–U4

Confirmed at their own pickup, per the 0.5.0 rule that a later pickup plan depends on what the
earlier unit found. U2: audit by source, not by memory; record the date each source was read;
demote anything unverifiable. U3: a flag that changes nothing must not claim a change, and the
unstated table stays computed by diffing rather than written by hand. U4: the check script must fail
when the package does not byte-compile or a test fails, because `make ci` currently passes without
looking at the code.

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

## Review criteria

Registered before any work. Delivery acceptance (R1–R4) is separate from benefit (R5–R7); R8 is the
format's own obligation.

| # | Criterion | Evidence source | Owner, window or trigger | Finding | Response |
| --- | --- | --- | --- | --- | --- |
| R1 | Delivery: the format document is complete enough for an implementer who cannot read our code | An assessor who did not write it, against acceptance criterion 2 | David or a named independent assessor, at the U1 return | Pending | — |
| R2 | Delivery: every `published practice` label cites a source that was read, with the date; nothing unverified is labelled as practice | The audit record, and a sample re-read of the sources | Heron returns; the assessor samples at the U2 return | Pending | — |
| R3 | Delivery: `new` and `check` behave as the format document says, for every kind and flag combination, offline | The test suite, and a run from a clean checkout | Heron, at the U3 return; `make ci` exits 0 through real checks | Pending | — |
| R4 | Delivery: unstated intent is never filled in, and the unstated table matches what the catalogue would change | Generated output checked against the catalogue by test | Heron, at the U3 return | Pending | — |
| R5 | Benefit: a new project's build is gated on a plan file committed before the build | That project's git history | David, trigger: the first project started after ratification (OQ7); no date | Pending | — |
| R6 | Benefit: `sitewalk --plan` consumes a siteplan-produced file unchanged, with no shared code | The first `sitewalk` run against a plan file | The sitewalk owner, unnamed until that project is staffed (OQ6) | Pending | — |
| R7 | Disconfirming: the brief is written once and never read, or the built site contradicts its plan | The first gated project's history, and its `sitewalk` run | David, trigger: that project's first deploy | Pending | If it holds, reconsider the tool's existence rather than maintain the document (`CONTEXT.md` §Success, and what would stop us) |
| R8 | The format does not break its consumer without a version bump | The change log in `docs/PLAN-FORMAT.md`, against `plan_version` and the consumer's releases | Heron at each format change; David for a breaking change | Pending | — |

Delivery is not benefit. R1–R4 can be settled at the return by reading artifacts and running
checks; R5–R7 are observations about the world and cannot be settled here. Recording them now is
what stops a passing check from being reported as a working product.

## The grant requested

Ratify course **A1** and register a grant for **U1** only. U2–U4 each need their own grant at
pickup, under the 0.5.0 rule that a grant permits its own unit; the principal can say now whether
he expects to grant them in sequence.

**Included in the U1 grant**: writing `docs/PLAN-FORMAT.md`; writing the two conformance fixtures;
bringing `siteplan check` and its tests to the document; having an independent assessor read the
document for implementability; committing those locally in this repository.

**Explicitly not requested**: any new dependency; any network use by the tool; publishing,
deploying, spending or outbound messages; changes to `CONTEXT.md` or to the template repository;
implementing `sitewalk`; authority to select among the courses in this record; and ratification of
the work already in the working tree, which this grant does not cover and which the plan is free to
reject.

**Stop condition**: U1 is returned for acceptance, or it needs something outside this grant —
including an answer to OQ3, OQ4 or OQ5 that the principal has not given.

## Template deviations reported, not fixed

The process documents came from a template written against Perspicuity 0.4.0; the installed skill
is 0.5.0. Reported rather than repaired, because the template is a different repository:

- `AGENTS.md` and `docs/KICKOFF.md` point at `/home/david/.codex/skills/perspicuity/SKILL.md`,
  which resolves today only through an undocumented symlink; the installed skill is under
  `/home/david/.dsh/`.
- The process documents describe the 0.4.0 record shape: no working mode in `Current position`, no
  `in_review` in the work-status set, and no `Blocked`/`Waiting on` fields.
- `AGENTS.md`'s standing-constraints section is still the template's placeholder: one real rule and
  an instruction to fill in the rest.
- `docs/RECORDS.md` lists the project code `sp` as belonging to "this template" rather than to this
  project.
- `AGENTS.md` §Your first task and `docs/KICKOFF.md` direct the first worker to revise three
  process documents and file `docs/records/<date>-process-record-conventions.md` before feature
  work. The principal's instructions of 2026-09-21 scoped the sessions differently, so that record
  is not filed. It remains the missing worked example for `docs/records/`.

## Changes

Revision 2, 2026-09-21T12:26:00-06:00. Changed: the mode, from `Run` to `Plan`, on the principal's
instruction of 2026-09-21 — the deliverable became a Statement of Work and the selection was
reserved to him; and the record, amended into that Statement of Work: five complete courses of
action including not building a tool at all; a consequence comparison with evidence and judgement
marked and the gaps left visible; a recommendation and the tradeoff it accepts; the unratified
draft recorded in Act with its measurements and its known defects; units U1–U4 with estimates and a
U1 pickup plan; out of scope; eight open questions; criteria R1–R8; and the grant requested.
Source: the principal's instruction of 2026-09-21; the working-tree measurements of
2026-09-21T12:22; the delegated fact-check of 2026-09-21. Reason: work was done ahead of a ratified
plan, and a plan that cannot reject it is a receipt rather than a plan. Preserved: revision 1
(`df09827`) holds the earlier frame, objectives O1–O5, material conditions C1–C7, the D1–D9
implementation selections made under the earlier grant, and the earlier review criteria R1–R5; this
revision supersedes them for future work without deleting them from history. Affects: U1–U4,
R1–R8, OQ1–OQ8, and any decision about the draft package.
