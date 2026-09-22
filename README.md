# siteplan

Turn a site's intent into an agent-first design brief: `BRIEF.md` for a person to read, and
`site.json` — the plan file — for a tool to check a built site against.

`siteplan` makes the decisions that are cheap once and expensive later: which Schema.org entities
describe the site, which machine-readable surfaces it must publish, what shape its URLs take, how it
treats crawlers, and what each page is for. It writes them down before the build, not after.

## What it does

- **Asks, and does not invent.** Inputs come from flags or from `--interactive`. Anything not
  supplied is recorded as unstated, and the brief says what stating it would change.
- **Writes `BRIEF.md`.** Every recommendation carries one of two labels: `published practice`, with
  the source named and read, or `our judgement`, with the fact it rests on named. You are entitled
  to discount the second.
- **Writes `site.json`.** The machine-readable plan, specified in
  [`docs/PLAN-FORMAT.md`](docs/PLAN-FORMAT.md) and consumed by `sitewalk --plan`.
- **Checks a plan file.** `siteplan check` reports every fault in a plan against the format, one
  line per fault, naming the key.

## How to run it

Python 3.11 or later, standard library only. No install step, no dependency, no network, no build.

```sh
# ask for the answers
python3 -m siteplan new --interactive

# or state them
python3 -m siteplan new --site example.com --name "East Side Bakery" \
    --kind local-business --sells --local --out plans/

# validate a plan, and then let a built site report against it
python3 -m siteplan check plans/site.json
sitewalk --plan plans/site.json
```

**Inputs.** `--site`, `--name`, `--kind`, `--out` (default `.`), `--interactive`, and four answer
pairs: `--sells`/`--no-sells`, `--local`/`--not-local`, `--publishes`/`--no-publishes`,
`--takes-bookings`/`--no-takes-bookings`. Neither flag of a pair leaves that answer **unstated**,
which is a third state and not a default.

**Kinds**: `content-site`, `directory`, `local-business`, `online-store`, `personal`, `saas`. The
kind selects the recommendations; it is required, because guessing one would invent the plan.

**Exit codes**: `0` clean, `1` findings or an invalid plan, `2` a usage error. An existing
`BRIEF.md` or `site.json` is refused rather than overwritten — write somewhere else with `--out DIR`,
or move the files first.

## What it does not do

- **No code generation, no scaffolding, no site templates.** It writes two files. The moment it
  emits templates it is a framework, which is a different project.
- **No crawling, no fetching, no network at all.** It asks questions and writes files. The test
  suite holds that shut: one test asserts no package module imports anything that can reach the
  network, and another runs the whole tool with sockets patched to fail.
- **No accounts, external APIs, telemetry or dependencies.**
- **It measures nothing about a live site, and it does not predict whether an agent will find,
  understand or recommend a site.** Passing `siteplan check` means the file follows the format;
  passing `sitewalk --plan` means a built site matches its plan. Neither is evidence of success,
  traffic, ranking or citation.
- **It does not decide for you.** A plan is a statement of intent that you own: the recommendations
  are recommendations, the labels say where each one comes from, and you disagree by editing the
  plan.

## Where the rest of it is

| | |
| --- | --- |
| [`docs/PLAN-FORMAT.md`](docs/PLAN-FORMAT.md) | The plan file format. This project owns it; `sitewalk` implements the consumer side from this document alone. |
| [`docs/CITATIONS.md`](docs/CITATIONS.md) | The audit behind every `published practice` label: what was read, when, and what changed. |
| [`docs/fixtures/plan-conformance.json`](docs/fixtures/plan-conformance.json) | 45 conformance cases, loadable by another repository's tests. |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | The settled technical shape and the alternatives that were rejected. |
| [`RECORD.md`](RECORD.md) | The project record: the basis, the units, the evidence, and what is not established. |
| `make ci` | The checks: the records, byte-compilation, the fixtures, the offline test suite, and the entry point. |
