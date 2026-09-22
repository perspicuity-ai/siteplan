# Citation audit

Every labelled recommendation in the kind catalogue (`siteplan/kinds.py`), checked against the
source it names, with the date each source was read.

This file exists because the labels are the product's only claim to trustworthiness, and a label
whose source does not say what the claim says is worse than no label: it borrows an authority it has
not earned. A first check of this catalogue — fifteen claims, chosen by hand rather than by
enumerating them — found four materially wrong and two overstated. This audit enumerates every
labelled claim instead, so what it reports is a count rather than an impression.

Audited 2026-09-21 by Heron for unit U2 of the project record (`RECORD.md`), with the source reads
delegated to two named workers who did not write the catalogue: **Plover** (Schema.org and vendor
documentation) and **Sanderling** (specifications and standards). Quotes are shortened; the URL is
the authority.

## Method, and what it does and does not establish

1. **Enumerate, do not sample.** The claim list is generated mechanically from the catalogue: the
   five surface bases, the advice for all six kinds, and the shared claims in `URL_WHY`,
   `CRAWLER_MECHANISM` and `PAGES_WHY`. It is complete by construction: 47 labelled claims
   (42 per kind, 5 surface).
2. **Read the source, not the memory of it.** Each claim's named source was fetched on 2026-09-21
   and read for the sentence that supports or refutes the claim.
3. **Label from the deciding component.** Where a source establishes what a term means but
   recommends nothing for this kind of site, the claim is a judgement and the source is named
   inside it as the fact it is. This is why labels moved down as well as up: the label names what
   decides the recommendation, not what makes it look respectable.
4. **The check is human.** `tests/test_catalogue_evidence.py` enforces only that a `published
   practice` claim names a source in `SOURCES`. It cannot tell whether the source says what the
   claim says, and no mechanical check can. This file is a reading with dates on it, not a pass.

**What a rate from this file means, and what it does not.** The scope is exhaustive over *labelled
claims in this catalogue*, which is stronger than the earlier hand-picked set of fifteen. It is not
a rate over "siteplan's claims about the web": it covers what the catalogue says, at the depth to
which each source was read. `supported` means one reader found the supporting sentence in the named
source on the date given. It does not mean the source is correct, current, or the only relevant
one, and it says nothing about claims in a future catalogue. The earlier convenience sample's rate
of four wrong out of fifteen should not be read as a property of anything except that sample; this
audit's own counts are below, with the same limit. Findings added after the first pass, such as
the `llms.txt` study above, are labelled as reported evidence rather than read evidence.

## What the audit found

| Count | Finding |
| --- | --- |
| 15 | claims carrying `published practice` before the audit |
| 2 | of them materially wrong: `OnlineStore` described as a subtype of `Store`, and `availability` described as required by the merchant-listing guidance |
| 2 | overstated: `robots.txt` presented without its Proposed-Standard status and voluntary nature, and `/sitemap.xml` presented as a defined location rather than a recommended one |
| 5 | labelled as practice although a source documents the vocabulary but recommends nothing for that kind of site: the identity types for `content-site`, `saas`, `directory` and `personal`, and the offering types for `directory` |
| 2 | judgement-labelled claims that the evidence does settle, and which are now `published practice`: the offering fields for `content-site` and for `saas` |
| 2 | further materially wrong claims found *inside judgement-labelled reasons*, which no label check would have caught: the local-business field note claiming the vendor guidance "asks for" `telephone`, and the `llms.txt` note claiming no consumer exists |
| 12 | claims carrying `published practice` after the audit, each naming a source that was read |
| 35 | claims carrying `our judgement` after the audit |

The last row of findings is the one worth keeping: **three of the four wrong claims were not
borrowed authority, they were wrong facts inside honest-looking prose.** The label discipline cannot
catch that. Reading the source can, and only that.

## Surface claims

| Surface | Label | Source, read 2026-09-21 | Verdict | What the source says, and what changed |
| --- | --- | --- | --- | --- |
| `robots.txt` | published practice | [RFC 9309](https://www.rfc-editor.org/rfc/rfc9309) | supported, qualified | The Robots Exclusion Protocol: a **Proposed Standard** (September 2022), not an Internet Standard. It requires the rules at `/robots.txt` in the top-level path. It binds nothing by itself: the RFC asks crawlers to honour the rules, says "these rules are not a form of access authorization", and calls itself no substitute for content security measures. The catalogue text now says all of that rather than calling compliance voluntary. |
| `sitemap.xml` | published practice | [sitemaps.org protocol](https://www.sitemaps.org/protocol.html) | supported, qualified | Sitemap protocol 0.9, published jointly by the search engines under CC BY-SA — not an IETF, W3C or ISO standard. It defines the XML sitemap and `lastmod`, and it *strongly recommends* the root location: `/sitemap.xml` is a convention, not a mandate. The text now says "recommends". |
| `json-ld` | published practice | [JSON-LD 1.1](https://www.w3.org/TR/json-ld11/), [Google's intro to structured data](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data) | supported | JSON-LD 1.1 is a W3C Recommendation (16 July 2020). Google's documentation lists JSON-LD as "(Recommended)" and says it recommends JSON-LD "if your site's setup allows it" — while noting the other supported formats are "equally fine" if valid. The word "recommended", not "required", is now the claim. |
| `llms.txt` | our judgement | [llmstxt.org](https://llmstxt.org/), [Google's AI-optimization guidance](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide), [Ahrefs llms.txt study](https://ahrefs.com/blog/llmstxt-study/) | supported as a judgement, with new evidence against the benefit | Proposed by Jeremy Howard in September 2024; no IETF draft, no W3C document, no ISO standard. Google's guidance says such files are not needed for Search and "neither harm nor help" visibility. **A server-log study across 137,000 domains reports that 97% of llms.txt files received no requests at all in May 2026, that AI retrieval bots accounted for about 1.1% of the requests that did occur (GPTBot 4.5%, ClaudeBot 0.8%), and that SEO audit tooling was the largest requester at 21.7%.** The label stays `our judgement` deliberately: the evidence does not support requiring the file, so the requirement is a one-file bet on agents that navigate a site, and the catalogue text now says exactly that rather than claiming a reader. |
| `rss.xml` | published practice | [RSS 2.0](https://www.rssboard.org/rss-specification), [RFC 4287](https://www.rfc-editor.org/rfc/rfc4287) | supported, qualified | RSS 2.0 version 2.0.11, published by the RSS Advisory Board in 2009 — a self-published board specification, not an IETF, W3C or ISO standard, and frozen in practice. Atom is RFC 4287, a Proposed Standard (December 2005). Both are published specifications for a dated feed. |

## The limit of any mechanical check here

**The label check catches borrowed authority; only reading catches a wrong fact.** Three of the four
wrong claims the first check found were wrong *facts* inside judgement-labelled prose — the
local-business note that said the vendor guidance "asks for" `telephone`, and the `llms.txt` note
that said no consumer exists — and no label check can see either of them, because in both cases the
label was honest and the sentence was not.

`tests/test_catalogue_evidence.py` enforces that a `published practice` claim names a source, and
that is the right enforcement precisely because it does not pretend to enforce agreement. A test
that claimed to check agreement would be a check that cannot fail. What enforces agreement is a
person reading the source, which is why this file exists, why it names its readers, and why it
carries a date on every row.

## The practice claims, by kind

| Kind | Group | The claim | Source read 2026-09-21 | Verdict |
| --- | --- | --- | --- | --- |
| `local-business` | identity types | `LocalBusiness`, and the most specific sub-type where one exists | [schema.org/LocalBusiness](https://schema.org/LocalBusiness), [Google local business](https://developers.google.com/search/docs/appearance/structured-data/local-business) | supported: "A particular physical business or branch of an organization"; Google: "Use the most specific LocalBusiness sub-type possible" |
| `online-store` | identity types | `OnlineStore` | [schema.org/OnlineStore](https://schema.org/OnlineStore), [Google organization](https://developers.google.com/search/docs/appearance/structured-data/organization) | supported after correction: `Organization` > `OnlineBusiness` > `OnlineStore`, and Google recommends "using the OnlineStore subtype instead of OnlineBusiness" for an ecommerce site. The catalogue had said `Store`. |
| `online-store` | offering types | `Product` with `Offer` | [Google merchant listing](https://developers.google.com/search/docs/appearance/structured-data/merchant-listing) | supported |
| `online-store` | offering fields | `name`, `image`, `offers`, `price`, `priceCurrency`, `availability`, `sku`, `brand` | Google merchant listing | supported after correction: `Product` requires `name`, `image` and `offers`; `Offer` requires `price` or `priceSpecification.price`, and `priceCurrency`; **`availability` is recommended, not required**. The catalogue had said required. |
| `content-site` | offering types | `Article` and `BlogPosting` for published writing | [schema.org/Article](https://schema.org/Article), [Google article](https://developers.google.com/search/docs/appearance/structured-data/article) | supported: Google documents `Article`, `NewsArticle` and `BlogPosting`, and has no required properties for them |
| `content-site` | offering fields | `headline`, `image`, `author`, `datePublished`, `dateModified` | Google article | supported, **moved up from judgement**: those five are exactly the recommended properties; `description` and `url` remain our additions and the text says so |
| `saas` | offering types | `SoftwareApplication`, with `WebApplication` for browser-only products | [schema.org/SoftwareApplication](https://schema.org/SoftwareApplication), [Google software app](https://developers.google.com/search/docs/appearance/structured-data/software-app) | supported: the vendor documents a software app feature built on the type |
| `saas` | offering fields | `name`, `description`, `applicationCategory`, `operatingSystem`, `featureList`, `url` | Google software app | supported, **moved up from judgement**: the guidance requires `name`, a price on an `Offer`, and one of `aggregateRating` or `review`, and recommends `applicationCategory` and `operatingSystem`. The plan requires the two recommended properties and leaves price and rating to the selling answer; `description`, `featureList` and `url` are our additions, and the text says so. |

## The judgement claims

35 claims carry `our judgement`. Most of them are the same seven decisions repeated per kind, each
naming the fact it rests on:

| Group, per kind | The fact inside it, with its source | Why it is a judgement |
| --- | --- | --- |
| URL rules (6) | RFC 3986 makes the scheme and host case-insensitive and says they should be normalized to lowercase; paths are case-sensitive | Lowercase paths, one trailing-slash convention and a depth limit are our rules. No source settles URL shape for a site. |
| Crawler stance (6) | RFC 9309 defines the mechanism and binds only crawlers that choose to honour it | Which stance suits a kind of site is a judgement about that kind of site. |
| Pages (6) | Google's structured-data guidelines: "Don't mark up content that is not visible to readers of the page" | The page set is our reading of what the kind needs, not a documented list. |
| Identity fields (6) | Schema.org's property definitions; Google's local-business, organization, merchant-listing and article guides where they give required or recommended lists | Which of those properties a site *must* publish is our selection. |
| Identity types (4): `content-site`, `saas`, `directory`, `personal` | Schema.org defines the types; Google recommends placing organization markup on the home page or on one page describing the organization, and documents a profile page built on `Person` | The types are documented; pairing them as the identity for these kinds of site is our reading, and the texts now say so. |
| Offering types and fields (5): `local-business` types and fields, `directory` types, `personal` types and fields | Schema.org's definitions; Google's carousel documentation (an `ItemList` of at least two `ListItem`s of one type, each with a `position` and a `url`) | The documented features do not cover these cases — the carousel's host types are narrow, and a service or a person is not a product listing — so the reading is ours. |
| Surface `llms.txt` | The proposal at llmstxt.org, and Google's statement that Search ignores such files | Recommending the file is a bet on tooling that reads it. |

## A source added after the first pass, and what could be read of it

The principal supplied the `llms.txt` lead on 2026-09-21 and asked that the study be read before it
was cited. It was attempted, and the limit is worth recording: **the Ahrefs page returns only its
title to a text reader** — "We Analyzed 137K Sites: 97% of llms.txt Files Never Get Read", HTTP 200,
body not extractable — so the methodology could not be read at first hand. The figures used above
come from two secondary reports of it ([Search Engine Journal](https://www.searchenginejournal.com/97-of-llms-txt-files-got-no-requests-ahrefs-data-shows/579478/), [PPC Land](https://ppc.land/llms-txt-adoption-rises-8-8x-but-97-of-files-get-zero-ai-requests/)),
which describe it as server-log data from 137,000 domains for May 2026, reported alongside
Originality.ai's adoption tracker (36,120 files, an 8.8x rise in a year).

That is enough to state the finding as *reported evidence* and not enough to call it verified: the
sample's selection, the log's coverage and the treatment of bots that never request the file are all
unread. Under this project's own rule, a claim whose source was not read does not get a `published
practice` label, which is one more reason the `llms.txt` requirement stays a judgement.

## What this audit did not establish

- **That the sources are right.** Each verdict is one reader's finding that the named source says
  what the claim says, on the date given. Whether a vendor's guidance will still say it next year,
  or whether a specification's advice matches what crawlers do, is outside this audit.
- **That the recommendations work.** No claim here is about whether a site following the plan is
  found, understood or recommended by anything. The claim boundary in `CONTEXT.md` is untouched.
- **That the reading is the only possible one.** Three sources were read at the level of the page
  that states the rule rather than its full normative text, and the schema.org property verdicts
  were taken from the published vocabulary dump rather than from each property's page.
- **That a later claim is honest.** The test enforces that a `published practice` label names a
  source; it cannot enforce that the source agrees. Only a reading does that, which is why this file
  carries dates and names the readers.
