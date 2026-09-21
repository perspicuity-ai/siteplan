# Context

What siteplan is, why it exists, and what "good" looks like.

**Project code:** `sp`

## The product, in one paragraph

`siteplan` turns a site's intent into an agent-first design brief. You tell it what the site is
for and who it serves; it returns the decisions that have to be made before anyone builds —
which Schema.org entities describe this business, which machine-readable surfaces the site must
publish, what shape the URLs take, how the site treats crawlers, and what each page is for. It
also emits the same decisions as a machine-readable **plan file**, so a built site can later be
checked against the plan it was supposed to follow.

## Why it exists

These decisions are cheap once, at the start, and expensive later: URL shape and entity model
are the two things a site cannot change without migrations and redirects, and both determine
whether a machine can tell what the site is.

Nothing today records them. `findmynextbite.food` publishes an `Organization` block and no
offering markup, and `perspicuity.ai` publishes no structured data at all — not because anyone
decided that, but because nobody decided anything.

`siteplan` exists so the decision is made once, in writing, before the build.

## Outcomes

1. **Every new project starts from a brief.** The plan file is an input to the build, not a
   description written afterwards.
2. **The brief is checkable.** `sitewalk --plan site.json` reports a built site against the plan
   it claims to follow. The two tools connect through the file, not through shared code.

## The claim boundary

`siteplan` recommends a **design**. It does not know whether that design will be found,
understood or recommended by any agent, and it does not measure anything about a live site. A
plan is a statement of intent to build against, and passing it is not evidence of success.

Where a recommendation rests on published practice it says so; where it is our judgement it says
that instead. A reader is entitled to discount the second.

## What we are deliberately not doing

- **No code generation and no scaffolding.** It produces a plan, not a site. The moment it
  writes templates it becomes a framework, and a framework is a different project.
- **No crawling and no network.** It asks questions and writes files.
- **No accounts and no external APIs.** Standard library only.
- **No guessing at unstated intent.** If the brief does not say what the site sells, the plan
  says so rather than inventing an answer.

## The plan file

`siteplan` owns this format, because it is the producer. `sitewalk` implements the consumer side
and links back here. Both repositories document it; this one is authoritative.

It is deliberately small — a handful of keys, no nesting beyond one level, and every key
optional so a partial plan is still usable:

```json
{
  "plan_version": 1,
  "site": "example.com",
  "kind": "local-business",
  "required_surfaces": ["robots.txt", "sitemap.xml", "llms.txt"],
  "identity": {"schema_types": ["LocalBusiness"], "fields": ["name", "address", "telephone"]},
  "offering": {"schema_types": ["Service"], "fields": ["name", "description"]},
  "url_rules": {"lowercase": true, "trailing_slash": "never", "max_depth": 3},
  "crawler_stance": "open",
  "pages": [{"path": "/", "purpose": "what the business is and where it is"}]
}
```

## Success, and what would stop us

- **Passes** when a new project's build is gated on a plan this tool produced.
- **Fails** if the brief is written once and never read, or if the plan file drifts from what the
  build actually does — in which case the honest outcome is to delete the tool, not to maintain
  a document nobody follows.
- **Scope cap:** if the first version cannot produce a complete brief in one run, cut the number
  of questions rather than adding a configuration file.
