# The plan file format

The authoritative specification of `site.json`, the machine-readable plan that `siteplan` produces
and that `sitewalk --plan` consumes.

**This project owns the format.** `sitewalk` implements the consumer side in its own repository and
links back here; the two tools share no code, and this document is the whole interface between them.
Where this document and `siteplan`'s code disagree, this document is right and the code is the
defect.

| | |
| --- | --- |
| Format | `plan_version` **1** |
| First frozen | 2026-09-21 (project record `sp-project`, revision 3, unit U1) |
| Producer | `siteplan` in this repository |
| Consumer | `sitewalk --plan`, a separate repository |

## What a plan is

A plan is a **statement of intent to build against**. It records the decisions that are cheap once
and expensive later: which Schema.org entities describe a site, which machine-readable surfaces it
must publish, what shape its URLs take, how it treats crawlers, and what each page is for.

**A plan is not a prediction and not a measurement.** It does not predict whether an agent will
find, understand or recommend a site; a plan that validates is a well-formed statement of intent,
not evidence of success, traffic, ranking or citation. Nothing in this format is fetched from a live
site: the file is written, read, and compared against a site that claims to follow it.

The plan is what a build is checked against. Where it is silent, a consumer has nothing to check,
which is why every key except the version marker is optional: **a partial plan is valid**, and a
consumer must not treat an absent key as a failure.

## Structure

The file is a single JSON object — no arrays or scalars at the top level — with nine keys, at most
one level of nesting, and no key that is not listed here.

| Key | Type | Required | Meaning |
| --- | --- | --- | --- |
| `plan_version` | integer | **yes** | The version of this format the file follows. Must be `1`. |
| `site` | string | no | The bare domain the plan is for, e.g. `example.com`. |
| `kind` | string | no | The kind of site, from the closed list below. |
| `required_surfaces` | array of string | no | Machine-readable surfaces the site must publish, from the closed list below. |
| `identity` | object | no | `schema_types` and `fields`: what the site is. |
| `offering` | object | no | `schema_types` and `fields`: what the site provides. |
| `url_rules` | object | no | `lowercase`, `trailing_slash`, `max_depth`: the shape of every URL. |
| `crawler_stance` | string | no | How the site treats crawlers, from the closed list below. |
| `pages` | array of object | no | `path` and `purpose`: what each page is for. |

`plan_version` is required because a file that does not name its format cannot be validated safely:
the consumer cannot tell which contract it is holding. Every other key is optional, so a plan whose
only key is `plan_version` is valid and means "nothing is decided yet".

Unknown keys are **invalid at every level**. A key a consumer does not understand is a decision that
was not made, and a plan that drifts silently from what was agreed is the failure this format exists
to expose.

Each object admits exactly the keys named for it, and nothing else. Nesting stops at the second
level:

| Object | Keys it admits |
| --- | --- |
| the file itself | the nine keys in the table above |
| `identity`, `offering` | `schema_types`, `fields` |
| `url_rules` | `lowercase`, `trailing_slash`, `max_depth` |
| each element of `pages` | `path`, `purpose` |

A validator reports **one fault per problem**, each naming the offending key's own path — `kind`,
`url_rules.max_depth`, `pages[2].path`, or `identity.schemaTypes` for the camelCase misspelling of
the key `schema_types` — followed by what is wrong with it. It does not stop at the first fault, so
one run lists everything that is wrong, and one problem yields exactly one fault: a missing required
key, a value of the wrong type, a key that does not belong, a duplicate entry, a value outside a
closed vocabulary, or a page deeper than `max_depth`. A `plan_version` that is absent, of the wrong
type, or a different integer is one fault, never several. Where a list holds a repeated value, the
first occurrence stands and each later one is a fault.

Values are read **exactly as written**. Nothing is trimmed, normalised or case-folded: `" example.com"`
and `"sitemap.XML"` are faults, not values to be tidied. Closed-vocabulary values are
case-sensitive. Two identically-named keys in the same JSON object are a matter for the JSON parser,
not for this format, and a producer must not emit them.

## The open and closed rule

Whether an unknown value is an error depends on whether the consumer acts on it. This is a property
of the format, not a convention to be inferred:

- **Closed vocabularies are the values a consumer branches on.** An unknown value is **invalid**: it
  is a bug or a newer format, not an extension. The closed vocabularies are `kind`,
  `required_surfaces`, `crawler_stance` and `url_rules.trailing_slash`.
- **The Schema.org vocabulary is open.** `identity.schema_types`, `identity.fields`,
  `offering.schema_types` and `offering.fields` name terms from a vocabulary that is large and moves
  without this project, so their values are **carried through and not checked against a list**.
  A consumer ignores a name it does not know, and never changes its structure because of one. Their
  **shape** is still checked, so that a value which cannot be a Schema.org name at all is caught
  where it is written: a type name starts with an upper-case letter, a property name with a
  lower-case letter, and both continue with letters and digits only.
- **Everything else is closed by shape**: required types, non-empty collections, positive integers,
  and the path rule for `pages`.

## The keys

### `plan_version`

An integer, and it must be exactly `1`. A consumer that reads a version it does not implement must
refuse the file rather than guess: an unknown version means the contract is not the one it knows.
The producer's `check` rejects anything but `1`, with the expected and actual values in the message.

### `site`

A bare host name: one or more dot-separated DNS labels, each of 1–63 ASCII letters, digits or
hyphens, not beginning or ending with a hyphen, with an optional final dot for the root form.
`example.com` and `example.com.` are valid. Host names are case-insensitive, so `Example.COM` is
valid too; a producer writes them lower-case. A non-ASCII name must be punycode.

Everything else is invalid: `https://example.com` (scheme), `example.com/pricing` (path),
`example.com:8080` (port), `example..com` (empty label), `-example.com` (leading hyphen), and any
value with whitespace. An empty string is not a value anywhere in this format; omit the key instead.

Paths belong in `pages`, not here. A producer that is given a URL normalises it to the bare host
and says in its brief what it dropped; it does not silently record the whole URL.

### `kind` — closed

One of six names. The format defines the names; which kinds a generator offers profiles for is a
separate question, decided and recorded in this repository, so a valid plan may name a kind the
current generator does not implement.

| Value | The kind of site |
| --- | --- |
| `content-site` | Publishes writing for people to read: a magazine, a blog, a research site. |
| `directory` | Collects and organises entries that belong to others. |
| `local-business` | Serves people in a place: a shop, a bakery, a restaurant, a tradesperson. |
| `online-store` | Sells products online and ships them. |
| `personal` | Is about one person. |
| `saas` | A software product reached through a browser. |

### `required_surfaces` — closed

A non-empty array of unique names, each from this list. These are the machine-readable surfaces the
site **must** publish; the plan is what a consumer checks them against.

| Value | The surface |
| --- | --- |
| `json-ld` | Schema.org JSON-LD in the HTML of the pages it describes. |
| `llms.txt` | A plain-text map of the site at `/llms.txt`, as proposed at llmstxt.org. Not a standard, and no consumer is guaranteed. |
| `robots.txt` | Crawler access rules at `/robots.txt`, per RFC 9309. |
| `rss.xml` | A dated feed, RSS 2.0 or Atom. |
| `sitemap.xml` | An XML sitemap per the sitemaps.org protocol. |

### `identity` and `offering`

Each is an object with up to two keys, and at least one of them:

| Key | Type | Meaning |
| --- | --- | --- |
| `schema_types` | non-empty array of unique Schema.org **type** names | The entities that describe this site (`identity`) or what it provides (`offering`). |
| `fields` | non-empty array of unique Schema.org **property** names | The properties the site must expose for those entities. |

The vocabulary is open, as above. Names are Schema.org's own spelling — `openingHoursSpecification`,
not `opening_hours` — so that a consumer can pass them to a Schema.org-aware reader without a
translation table. Presence of the object means the site claims something about it; an object with
neither key is invalid, and an empty array is invalid: omit the key instead, because an empty list
requires nothing and so says something different from an absent one.

The producer's catalogue carries the field lists it recommends; the format does not require any
particular set, and a plan with `fields: ["servesCuisine"]` is valid even though no catalogue in
this project emits it.

### `url_rules`

An object with up to three keys, at least one of them:

| Key | Type | Values | Meaning |
| --- | --- | --- | --- |
| `lowercase` | boolean | `true`, `false` | Whether every path is lower-case. |
| `trailing_slash` | string | `never`, `always` | Which form every URL takes. A consumer branches on this value, so it is closed: `sometimes` is not a rule, it is the absence of one. |
| `max_depth` | integer | 1 or more | The greatest path depth any page may have. `/` is depth 0, `/a` is depth 1, `/a/b` is depth 2. |

If `pages` is also present, every page's depth must be **no greater than** `max_depth`: a plan whose
pages contradict its own URL rules is invalid. This is the only rule that spans two keys, and it
exists because a plan that breaks it cannot be followed without one of the two being wrong.

### `crawler_stance` — closed

One of three values. The stance is expressed by the site's `robots.txt`, which is why it appears in
`required_surfaces` as well; RFC 9309 defines the mechanism, and it binds only crawlers that choose
to follow it.

| Value | Meaning |
| --- | --- |
| `open` | No crawler is refused by default. |
| `selective` | General crawling is allowed and named classes of crawler or path are restricted — typically search and discovery allowed, bulk reuse or unbounded filter permutations disallowed. |
| `closed` | Everything except an explicitly named set of crawlers is refused. |

### `pages`

A non-empty array of objects. Each element must be an object — a string, number, array or `null`
element is invalid — and each has exactly two keys, both required:

| Key | Type | Meaning |
| --- | --- | --- |
| `path` | string | A site-relative path: `/`, or slash-separated segments beginning with `/`. |
| `purpose` | string | What the page is for, in one sentence, in the principal's terms. |

**The path rule.** A path is `/` alone, or `/` followed by one or more non-empty segments separated
by single slashes. Each segment is made of ASCII letters, digits and the path characters
`- . _ ~ % ! $ & ' ( ) * + , ; = : @`, or is a single `<placeholder>` segment naming a family of
pages: `/product/<slug>` means one page per product. A placeholder's name is lower-case letters,
digits, hyphens and underscores. **At most one placeholder per path.**

So `//a`, `/a//b`, `/pricing/` (a trailing slash), `/pricing?plan=pro` (a query), `/#top` (a
fragment), `/product/<Slug>` and `/a/<x>/<y>` are all invalid, as is anything with whitespace or a
non-ASCII character. A path never carries a trailing slash, even when `trailing_slash` is
`always`: `path` names the page, and `trailing_slash` describes the URLs the site serves. A path is
therefore written one way and only one way, which is what makes the "paths are unique" rule mean
something.

**Depth.** A placeholder segment counts as one segment. `/` is depth 0, `/product/<slug>` is depth
2, and a page may not be deeper than `url_rules.max_depth`.

`purpose` is the part of the plan a human reads to decide whether the page set is right, and the
part a consumer can compare against a page's actual content. Its wording is not validated beyond
being a non-empty string: whether it is one sentence is a matter for its reader, not the checker.

## Validation summary

`siteplan check FILE` applies every rule above and reports **one line per fault**, each naming the
key path it concerns, in the form `<key path>: <problem>`. It never stops at the first fault, so one
run lists everything that is wrong.

| Exit code | Meaning |
| --- | --- |
| `0` | The file follows this format. |
| `1` | The file is invalid, unreadable, or not JSON. Every fault is listed on standard error. |
| `2` | A usage error — the wrong arguments, not a fault in the file. |

Exit `0` means the file is a well-formed plan. It does **not** mean the plan is good, that a site
following it will succeed, or that anything was measured. It is the format's own check.

## Versioning

The format is a coupling between two repositories, so it changes under rules rather than by
convenience:

1. **This document is authoritative, not the code.** A consumer implements from the document alone;
   if the document is not enough to do that, the document is defective.
2. **Additive optional keys keep `plan_version`.** Every key except the version marker is optional,
   so a new optional key does not invalidate an existing consumer's reading of a plan.
3. **Removing a key, changing a key's meaning, or changing a closed vocabulary requires a
   `plan_version` bump.** Adding a value to a closed vocabulary does too, because a consumer
   branches on those values and an older one would treat a new value as a fault.
4. **A consumer must not guess, and must not pretend.** It may read a `plan_version` it does not
   implement — the two tools release independently, and a consumer that refuses an unfamiliar
   version puts both repositories into lockstep — but it must report the version it read, and it
   must not present its result as a check against a version it does not know. The producer's
   `check` implements version 1 only and rejects any other value.
5. **Every change carries a dated entry in the change log below, naming the consumer-side effect.**
   A change that breaks a consumer is the principal's decision, because it costs work in another
   repository.
6. **Unknown keys are invalid, and the producer rejects them.** A consumer may carry an unknown key
   and report it as *not checked*, naming the key and the reason; it must never present an unchecked
   key as met. This is not a deviation: the format is expected to grow, and a consumer that refused
   to read a file because it had grown would force the two repositories into lockstep. The format
   fixes the finding — a file with an unknown key is invalid — and leaves the consumer's process,
   including its exit status, to that consumer. The producer's `check` is the exception: its three
   codes are fixed above.
7. **Conformance fixtures are published with the format** — see below — so a consumer can test
   itself against this document without reading this project's code.

## Conformance fixtures

`docs/fixtures/plan-conformance.json` holds cases for validating a plan file: valid plans, invalid
plans, and for each invalid one the key that must be named in the finding. Its shape:

```json
{
  "format": "siteplan-plan-conformance/1",
  "plan_version": 1,
  "cases": [
    {"name": "...", "covers": "what the case establishes", "valid": true, "plan": {}},
    {"name": "...", "covers": "...", "valid": false, "invalid_keys": ["pages[0].path"],
     "expect": "a substring the producer's own message must contain", "plan": {}}
  ]
}
```

A consumer can run the cases through its own validation: a `valid` case must produce no finding, and
an invalid case must produce a finding naming each key in `invalid_keys`. `expect` is a
producer-side regression check, not a requirement on a consumer's wording. The cases are not inlined
in this document: the file is the artifact a consumer's tests load, and this section is the contract
it keeps. The fixtures are exercised by this repository's tests on every `make ci`, so they cannot
rot unnoticed.

## For the consumer

`plan_version` **1** was first frozen on 2026-09-21 and is the version a consumer should implement.
The stable parts are the nine keys, the shapes above, the closed vocabularies, and the rule that a
consumer reports what it did not check. The parts expected to grow without a version bump are the
Schema.org vocabularies in `identity` and `offering`, which move independently of this project.

**A worked consumer already exists.** `sitewalk --plan` implements this format in a separate
repository with no shared code. It reads the nine keys; it **enforces** `required_surfaces` against
the files the site publishes and `identity.schema_types` against the home page's JSON-LD; it names
`offering`, `url_rules`, `crawler_stance`, `pages` and `identity.fields` in its output as *not
checked*, with the reason for each; it reports the `plan_version` it read, and treats a version or a
key it does not know as a note rather than a fault; and it exits non-zero when a plan cannot be read
at all, because a gate that cannot read its own plan must not report a pass. Its behaviour is
compatible with this document as written, and it is the reference reading of the rules above.

Two things follow for anyone writing another consumer. It is conforming to read a version or a key
you do not implement and report it; it is not conforming to present an unchecked key as met, or to
report a pass on a plan you could not read. And the fixture file above exists so your tests can
check your reading against this document without reading either implementation.

Questions about this format, and any change to it, are recorded in `RECORD.md` in this repository —
that is the durable channel. A change that would break a consumer is a decision for the project's
principal, not for the producer's worker.

## Change log

| Date | `plan_version` | Change | Consumer-side effect |
| --- | --- | --- | --- |
| 2026-09-21 | 1 | First freeze. The nine keys, the open/closed rule, the versioning rules and the conformance fixtures are published as `plan_version` 1. | None: this is the first published version. |
| 2026-09-21 | 1 | Rules 4 and 6 corrected after reading the consumer that already exists: a consumer may read a version or a key it does not implement, must report it, and must not present it as checked or as a pass. The producer's rules are unchanged — `plan_version` is still required and `check` still rejects any other value or unknown key. | None to what a valid plan is. It removes an instruction that would have contradicted `sitewalk --plan`, which the principal had already ratified as tolerant of unknown versions and keys. |
