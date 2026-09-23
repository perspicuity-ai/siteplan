---
name: siteplan
description: >-
  Write an agent-first design brief (BRIEF.md) and a machine-readable plan file (site.json) for a
  website before anyone builds it. Offer it when a new website, landing page or other project that
  publishes web pages is about to be built, before the first build commit. It records the
  Schema.org entities, the machine-readable surfaces, the URL shape, the crawler stance and the
  purpose of each page. It does not generate code, fetch anything or measure a live site.
---

# siteplan

`siteplan` turns what a site is for into two files. `BRIEF.md` is for a person to read. `site.json`
is the plan file, for a tool to check a built site against. The tool is standard-library Python,
version 3.11 or later. It needs no install step, no network and no account.

In this file, `<skill-dir>` is the directory that holds this `SKILL.md`. That directory is also the
root of the tool's repository.

## When to offer it

Offer `siteplan` when one of these conditions is true:

- The user starts a new website, landing page or other project that publishes web pages.
- The user is about to write the first page, template or route for such a project.
- The user asks which structured data, URL shape or crawler rules a new site needs.

Offer it before the build starts. The decisions in the brief are cheap before the build and
expensive after it.

Tell the user which two files the tool writes. Ask the user before you run it.

Do not use `siteplan` to check a site that exists. The tool never reads a site.

## Collect the answers

1. Ask the user for the domain of the site.
2. Ask the user for the name of the site or the business.
3. Run the help command below to see the kinds of site and the answer flags.
4. Ask the user which kind of site it is.
5. Ask the user each yes-or-no question that the help command lists.

```sh
PYTHONPATH="<skill-dir>" python3 -m siteplan new --help
```

If no kind fits the site, tell the user. Do not choose the nearest kind without the user's
agreement.

Give an answer flag only for an answer that the user gives. If the user gives no answer, give no
flag. The tool then records that answer as unstated. Do not guess an answer.

## Run it

Run these two commands from the root of the project that the user builds. Replace each placeholder
with the user's answer. `<dir>` is the project directory for the two files, for example `plan`.
Add the answer flags from the user to the first command.

```sh
PYTHONPATH="<skill-dir>" python3 -m siteplan new --site <domain> --name "<name>" --kind <kind> --out <dir>
PYTHONPATH="<skill-dir>" python3 -m siteplan check <dir>/site.json
```

The first command writes `<dir>/BRIEF.md` and `<dir>/site.json`. The second command validates the
plan file against the plan format. Both commands exit with code 0 when they succeed.

If a command exits with a different code, show the user the message that the tool printed. Do not
run the command again with values that the user did not give.

## After the run

1. Ask the user to read `BRIEF.md` before the build starts.
2. Commit `BRIEF.md` and `site.json` in the project before the first build commit.
3. If the project keeps a decision record, cite `site.json` and its commit in that record.

A consumer such as `sitewalk --plan` reads `site.json` later, to check the built site against the
plan.

## Report the result

Include these items when you report the run to the user:

- The paths of the two files.
- The kind of site, and each answer that the user did not give.
- For each recommendation that you repeat, its label from `BRIEF.md`: `published practice` or
  `our judgement`.
- The first quoted paragraph in the next section, word for word.

A report without that paragraph is incomplete. Do not present the plan as evidence that an agent
will find, understand or recommend the site. Do not present an `our judgement` recommendation as
published practice.

## What this does not establish

The text below is quoted verbatim from the `BRIEF.md` that `siteplan new` writes. The first
paragraph is from its section "What this brief is". The list is its section "What this brief does
not claim", in full. The check in `scripts/check-project.sh` fails when a quoted line stops
matching the tool's output.

> **A plan is a statement of intent. It does not predict whether an agent will find, understand or recommend the site.**
>
> - It does not predict whether an agent will find, understand or recommend this site.
> - It does not measure anything about a live site, and it fetched nothing.
> - It does not rank the labels: a `published practice` recommendation can still be wrong for this site, and an `our judgement` one can still be right.
> - It does not fill in what you did not say. An unstated input stays unstated above, and the plan below is the kind's recommendation, not your answer.
> - It does not build, scaffold or generate anything. It writes two files.

## Limits of this skill

- The skill does not make the decisions. The user owns the plan and can edit `site.json`.
- The tool supports only the kinds of site that the help command lists.
- The check proves that the commands in this file run and that the quotation matches the tool's
  output. It does not prove that a session offers the skill at the right moment.
- `README.md` and `CONTEXT.md` in `<skill-dir>` describe the tool in full. `docs/PLAN-FORMAT.md`
  specifies the plan file.
