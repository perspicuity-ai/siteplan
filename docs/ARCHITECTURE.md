# Architecture

The settled technical view of `siteplan`: how the pieces fit at run time, what was chosen, and what
was rejected. The full basis — the alternatives, their consequences and the selection — is in
[`RECORD.md`](../RECORD.md); this file is the short version a reader wants before touching the code,
and it links rather than restates, so the two cannot drift into disagreement.

## The shape

One process, no server and no state. `python3 -m siteplan <command>` runs, reads its arguments, and
exits:

```
argv ──> cli.main ──> intent.SiteIntent ──> kinds.apply_intent ──> Profile
                          (flags or                │                   │
                           interactive)            │                   ├──> brief.render ──> BRIEF.md
                                                   │                   └──> plan.build   ──> site.json
                                                   └──> format.validate (the producer checks its own output)

siteplan check FILE ──> format.read_plan ──> format.validate ──> faults on stderr, exit 1
```

`sitewalk --plan site.json` is a separate process in a separate repository. There is no shared code
and no import between them: [`PLAN-FORMAT.md`](PLAN-FORMAT.md) is the whole interface.

## Decisions

Each decision names what was rejected, so it is not relitigated by the next reader who has not seen
the alternatives. The reasoning and the selection are in [`RECORD.md`](../RECORD.md).

**D1. The recommendations live in code, as data (`siteplan/kinds.py`), not in a config file.**
Rejected: a JSON or YAML catalogue loaded at run time (a second format, a loader, and a validator for
the loader; a data file can be edited into an invalid state silently) and asking a model at run time
(a dependency, non-deterministic, and an unlabelled judgement behind a respectable-looking brief).
Code is typed, diffable and testable.

**D2. Two artifacts from one source: `BRIEF.md` and `site.json`, both rendered from one `Profile`.**
Rejected: JSON only, rendered on demand (a brief that needs a command run to be read is the "written
once and never read" failure `CONTEXT.md` names) and the plan embedded in the brief as a fenced
block (two parsers for one file, and the halves drift the moment one is edited by hand).

**D3. The producer is strict about the format; the consumer is tolerant and must disclose what it
did not check.** Rejected: symmetric tolerance (a plan that drifts silently is the failure the
format exists to expose) and symmetric strictness (it would put two independently released
repositories into lockstep). The reasoning is rules 4 and 6 of the format document.

**D4. Exit codes are three, and there is no `--force`.** `0` clean, `1` findings or an invalid plan,
`2` a usage error. Rejected: a fourth code for an internal defect (a plan the generator cannot
validate is an invalid plan, which is a finding) and an overwrite flag (a plan is the record of a
decision; replacing it silently destroys the thing the tool exists to keep).

**D5. The catalogue's claims are labelled, and audited by reading rather than by a test.** A test
enforces the weaker half — a `published practice` claim must name a source — and
[`CITATIONS.md`](CITATIONS.md) carries the reading, with dates and named readers. Rejected: a test
that claims to verify agreement between a claim and its source (it would be a check that cannot
fail) and unlabelled prose (the failure the first audit found four times).

## What is deliberately absent

- **No network code of any kind.** No package module imports a networking module, and a test runs the
  whole tool with sockets patched to fail.
- **No dependency, no build step, no packaging.** The package is imported from the repository root;
  `python3 -m siteplan` is the entry point.
- **No generated site, template or scaffold.** The tool writes two files and stops.
- **No configuration file.** The scope cap in [`CONTEXT.md`](../CONTEXT.md): if the first version
  cannot produce a complete brief in one run, cut questions rather than add configuration.
- **No accounts, storage, telemetry or personal data.** Nothing is written except the two output
  files, and nothing about a person is collected.
- **No measurement of any live site.** `siteplan` never sees a site; that is `sitewalk`'s job, and
  the two connect only through the plan file.
