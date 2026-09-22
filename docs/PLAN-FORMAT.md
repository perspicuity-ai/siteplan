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
to expose. That is the rule for the file, and for the producer that writes and checks it; what a
*consumer* may do with an unknown key — carry it, and report it as not checked — is rule 6 below.
The two are not in conflict: the file stays invalid, and the consumer says so.

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
case-sensitive.

**A JSON object in a plan must not repeat a key, and that is the format's business rather than the
parser's.** JSON leaves the outcome to the implementation — one parser keeps the last value, another
the first — so two compliant readers can take different plans from the same bytes with no fault on
either side. A plan whose text repeats a key within one object is therefore **invalid**, and a
validator detects it by parsing with a duplicate-aware reader rather than by trusting a default:
`siteplan check` reports the repeated key and exits `1`.

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

An integer, and it must be exactly `1`. The producer's `check` rejects anything else — absent, of
another type, or a different integer — with the expected and actual values in the message. **This
requirement is the producer's**: what a consumer may and must do with a version it does not
implement is rule 4 below, which permits reading it and forbids pretending it was checked.

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
| `json-ld` | Schema.org JSON-LD in the HTML of the site's pages, and on the **home page** in particular: see "What satisfies `json-ld`" below. |
| `llms.txt` | A plain-text map of the site at `/llms.txt`, as proposed at llmstxt.org. Not a standard, and no major search engine or AI vendor states that it reads one; Google's guidance says Search ignores such files. |
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

### What this document chose rather than found

Three rules in it are this project's decisions, not findings about how a plan must work. A reader is
entitled to disagree with any of them, and they are listed here so that a later reader can tell a
judgement from a finding:

| Rule | The choice | What reversing it would cost |
| --- | --- | --- |
| A `path` never carries a trailing slash, even when `trailing_slash` is `always` | the page's canonical name is written one way, so `/a` and `/a/` cannot both appear and "paths are unique" means something | a `plan_version` bump under rule 3, because it changes what a valid plan is |
| Path segments are ASCII, with a defined character set | one spelling per path, and `lowercase` has something to mean | the same |
| `site` is a host name, so a non-ASCII name must be punycode | one spelling per host, matching DNS itself | the same |

Each is defensible; none is proved, and no source settles them. They are stated so that a consumer
knows what to implement, and marked as choices so that nobody later mistakes them for evidence.

## What satisfies `json-ld`

`json-ld` is the one surface in the vocabulary that is not a file a consumer can fetch, so what
satisfies it has to be stated rather than inferred — and until this section existed, two compliant
consumers could return different verdicts for the same site:

- **A site satisfies `json-ld` when its home page carries Schema.org JSON-LD.** That is where the
  identity markup belongs, and Google's organization guidance says so in as many words: "We recommend
  placing this information on your home page, or a single page that describes your organization."
  A site whose only JSON-LD sits on a deep page does **not** satisfy the surface; a check that accepts
  it would pass a site no machine can identify from its front door.
- **Markup on other pages is described by that page's `purpose`, and is information rather than the
  verdict.** A consumer may report the types it found elsewhere — an `Article` on an article page, a
  `Product` on a product page — and doing so is useful. It does not change whether the surface is met,
  because the plan does not say which types belong on which page and the format does not invent one.
- **A consumer checking this surface says which page it looked at.** "json-ld: met" without the page
  is the same class of claim as a verdict on a version the consumer does not know.

A plan that wants markup on a particular page says so in that page's `purpose`, in the principal's
words. A consumer that checks a purpose against the page is making a judgement, not applying a rule,
and must say which it is doing.

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
4. **Keys grow; versions announce.** An unknown key and an unknown version are not the same kind of
   change, and a consumer treats them differently. This rule is the reason for the difference, and
   it is here so that a later reader does not "simplify" the version check away as redundant with
   the key check:

   - **An unknown key is additive growth.** A consumer may carry it and report it as *not checked*,
     naming every key it did not check, so that no reader can reach a "met" without knowing that
     something was left unchecked. That disclosure is the condition that makes tolerance
     permissible — not advice about it — and it is why rule 6 permits what the producer rejects.
   - **An unknown version is the format announcing that a key's meaning may have moved**, which is
     the only thing a version is for; ignoring it defeats the announcement. So the verdict depends
     on the version: a **known or older** `plan_version` is read normally, because an older plan is
     fully specified by its own version, and that is exactly why accepting older versions is safe;
     an **unknown or newer** version makes the verdict **conditional**, and it must not be presented
     as a clean result. In the default mode the summary carries the condition; under the strict gate
     — `sitewalk --strict` — it is an error finding and exits non-zero. A gate that certifies a plan
     whose semantics it cannot know is the failure this rule prevents.

   **Reading continues.** A consumer that meets a version it does not implement reports the condition
   and goes on checking the keys it recognises; it does not abandon the file because of the version
   alone, and it does not present what it checked as a verdict on a version it does not know.

   **"Older" means an older version of this format, not an older-looking number.** `plan_version` is a
   positive integer, and `1` is the only version this document defines. A value of `0`, a negative
   number, a string, a list, or no value at all is not an older version and is not a newer one: it is
   **a fault in the file**. A consumer reports it as a fault rather than as a condition — there is no
   version to be conditional about — and under its strict gate, a plan the consumer cannot place
   against any version it knows must exit non-zero rather than certify the plan. The producer's
   `check` implements version 1 only, rejects every other value, and rejects an absent or mistyped one
   with a message naming `plan_version`.
5. **Every change carries a dated entry in the change log below, naming the consumer-side effect.**
   A change that breaks a consumer is the principal's decision, because it costs work in another
   repository.
6. **Unknown keys are invalid, and the producer rejects them.** A consumer may carry an unknown key
   and report it as *not checked*, naming the key and the reason; it must never present an unchecked
   key as met, and **naming every key it ignored is the condition of that permission, not advice**.
   This is not a deviation: the format is expected to grow, and a consumer that refused to read a
   file because it had grown would force the two repositories into lockstep. The format fixes the
   finding — a file with an unknown key is invalid — and leaves the consumer's process, including
   its exit status, to that consumer. The producer's `check` is the exception: its three codes are
   fixed above.

   **The disclosure must survive into whatever a machine reads.** Naming the ignored keys only in
   prose is not the condition met: a consumer that emits structured output must carry every key it
   did not check into that output, so that no automated reader can see a "met" without also seeing
   what was left unchecked. The condition of tolerance is the disclosure, and a disclosure only a
   human can see does not satisfy it.
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

A consumer can run the cases through its own validation. A `valid` case must raise no fault. An
invalid case must produce a finding naming each key in `invalid_keys`; a consumer that reads plans
rather than validating them may report such a key as a note instead of a fault, but it must name it
and must not report the case as met. `expect` is a producer-side regression check, not a requirement
on a consumer's wording. The cases are not inlined in this document: the file is the artifact a
consumer's tests load, and this section is the contract it keeps. The fixtures are exercised by this
repository's tests on every `make ci`, so they cannot rot unnoticed.

## For the consumer

`plan_version` **1** was first frozen on 2026-09-21 and is the version a consumer should implement.
The stable parts are the nine keys, the shapes above, the closed vocabularies, and the rule that a
consumer reports what it did not check. The parts expected to grow without a version bump are the
Schema.org vocabularies in `identity` and `offering`, which move independently of this project.

**A worked consumer already exists**, and this paragraph is a worked case, not a second authority:
the rules above stand on their own, and a reader who never opens another repository's code can
implement from them. `sitewalk --plan` implements this format in a separate repository with no
shared code. It reads all nine keys: it **enforces** `required_surfaces` against the files the site
publishes and `identity.schema_types` against the home page's JSON-LD, while `site` and `kind` are
read and reported; it names `offering`, `url_rules`, `crawler_stance`, `pages` and `identity.fields`
in its output as *not checked*, with the reason for each; it reports the `plan_version` it read and
treats a version or a key it does not know as a note rather than a fault; and it exits non-zero when
a plan cannot be read at all, because a gate that cannot read its own plan must not report a pass.
**One part of that is behind this document rather than ahead of it**: rule 4 now requires an unknown
or newer version to make the verdict conditional, carried in the summary and treated as an error by
the strict gate (`sitewalk --strict`). `sitewalk` still records it as a note, and carrying that
requirement into its gate is recorded as its own unit in that repository. The document states the
rule; it does not claim the consumer has it yet.

Two things follow for anyone writing another consumer. It is conforming to read a version or a key
you do not implement and report it as not checked; it is not conforming to present an unchecked key
as met, or to report a pass on a plan you could not read. And the fixture file above exists so your
tests can check your reading against this document without reading either implementation.

Questions about this format, and any change to it, are recorded in `RECORD.md` in this repository —
that is the durable channel. A change that would break a consumer is a decision for the project's
principal, not for the producer's worker.

### Why these keep `plan_version` 1

Every entry above clarifies a case the document left undefined rather than changing a case it
defined, so rule 2 applies and no bump is needed. **G4 is the one worth arguing about**, and the
reasoning is recorded rather than assumed: the document already said a producer must not emit a
repeated key, so no valid plan is affected; what changes is that a file which was previously
*undefined* is now *invalid*. Rule 3 lists removing a key, changing a key's meaning and changing a
closed vocabulary as the bump-triggering changes, and defining an undefined file is none of those. A
reader who disagrees should say so before a consumer implements against this revision, because the
cost of being wrong is a `plan_version` 2 that both repositories must handle.

## Change log

| Date | `plan_version` | Change | Consumer-side effect |
| --- | --- | --- | --- |
| 2026-09-21 | 1 | First freeze. The nine keys, the open/closed rule, the versioning rules and the conformance fixtures are published as `plan_version` 1. | None: this is the first published version. |
| 2026-09-21 | 1 | Rules 4 and 6 corrected after reading the consumer that already exists: a consumer may read a version or a key it does not implement, must report it, and must not present it as checked or as a pass. The producer's rules are unchanged — `plan_version` is still required and `check` still rejects any other value or unknown key. | None to what a valid plan is. It removes an instruction that would have contradicted `sitewalk --plan`, which the principal had already ratified as tolerant of unknown versions and keys. |
| 2026-09-21 | 1 | **What satisfies `json-ld` is defined** (G1 in the consumer's clarity review): the home page must carry Schema.org JSON-LD, markup elsewhere is information rather than the verdict, and a consumer says which page it looked at. This was the one surface that is not a file, so nothing defined it by fetching; two compliant consumers could return different verdicts for the same site. | **A consumer that accepted JSON-LD on any page must change.** `sitewalk`'s `json-ld` check reads any crawled page today, so this rule is work for it. A plan-level clarification: no key, shape or vocabulary changed. |
| 2026-09-21 | 1 | **Reading continues past a version the consumer does not implement, "older" means an older version of this format rather than a smaller number, and an absent or mistyped `plan_version` is a fault rather than a condition** (G2 and G3). The absent-or-mistyped behaviour is the principal's ruling of 2026-09-21, given when the consumer asked whether a missing version should gate; it is written here because a second implementer cannot reach it from the document otherwise. | None to what a valid plan is. A consumer must keep checking the keys it recognises, and must refuse to certify a plan it cannot place against any known version. |
| 2026-09-21 | 1 | **A JSON object in a plan must not repeat a key** (G4), and a validator detects it with a duplicate-aware parse. JSON leaves the outcome to the implementation, so two compliant readers could take different plans from the same bytes; the file is now invalid rather than undefined. | **Both implementations now refuse it.** `sitewalk` already does, with tests covering a top-level duplicate, a nested one, the legitimate repeat of a key in different objects, and that all fixture cases still load; `siteplan check` does from this revision and exits `1`. This is the one item here that narrows what is accepted — see the note below on rule 2 versus rule 3. |
| 2026-09-21 | 1 | **The disclosure of ignored keys must survive into machine-readable output** (G5): naming them only in prose does not meet the condition that makes tolerance permissible. | **A consumer that names unchecked keys only in human-readable notes must carry them into its structured output.** Work for `sitewalk`; nothing changes for a valid plan. |
| 2026-09-21 | 1 | A valid conformance case was added for `json-ld` presence, because no case exercised the one surface with no file behind it — which is why the fixture set could not have caught G1. | None: a new case for consumers to run. |
| 2026-09-21 | 1 | Rule 4 sharpened, at the principal's direction, to separate an unknown key from an unknown version: keys grow, versions announce. An unknown key stays tolerable when every ignored key is named; an unknown or newer version makes the verdict conditional, carried in the summary and an error under the strict gate. The three judgement-based choices (trailing slash, ASCII segments, punycode hosts) are now listed as choices rather than findings. | **`sitewalk --strict` must treat an unknown or newer `plan_version` as an error, and the default summary must carry the condition.** That is a change in the consumer, recorded as its own unit there; it is not a change to what a valid plan is, so `plan_version` stays 1. |
