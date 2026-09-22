"""The per-kind catalogue: what siteplan recommends, and where each recommendation rests.

One frozen profile per kind. Every recommendation carries exactly one basis label:

* ``published practice`` - a citable standard, specification or vendor documentation, named in
  the reason.
* ``our judgement`` - no published source settles it.

Where a recommendation has both a published and a judged component, the label names the component
that decides it and the reason names the other. The label rule is stated in every generated brief,
because a reader is entitled to discount the second kind.

The reasons are composed by :func:`advice_for` from the profile's *current* state rather than
stored as finished prose, so a reason cannot go stale when a stated flag changes the value it
describes. A flag that changed nothing appends no sentence: the brief says "nothing changes"
instead of claiming a change it did not make.

Nothing here is fetched at run time. The tool has no network and the citations are text.

Every label in this file was checked against the source it names on 2026-09-21; the audit, its
method and its limits are in `docs/CITATIONS.md`. A claim that cannot name a source it was read
against belongs in `our judgement`, and `tests/test_catalogue_evidence.py` fails a `published
practice` claim that names none.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

from .intent import SiteIntent

BASIS_PRACTICE = "published practice"
BASIS_JUDGEMENT = "our judgement"

#: The basis of each surface, and what the published source actually establishes.
SURFACE_BASIS: dict[str, tuple[str, str]] = {
    "robots.txt": (
        BASIS_PRACTICE,
        "RFC 9309 (2022), a Proposed Standard, requires the rules at /robots.txt in the "
        "top-level path. It is not an Internet Standard, and it binds nothing by itself: the RFC "
        "asks crawlers to honour the rules, says they are not a form of access authorization, and "
        "calls itself no substitute for content security measures.",
    ),
    "sitemap.xml": (
        BASIS_PRACTICE,
        "The sitemaps.org protocol (version 0.9, published jointly by the search engines under "
        "CC BY-SA rather than by a standards body) defines the XML sitemap and its conventions, "
        "and /sitemap.xml is the location it strongly recommends rather than one it mandates.",
    ),
    "json-ld": (
        BASIS_PRACTICE,
        "Schema.org defines the vocabulary, JSON-LD 1.1 is a W3C Recommendation (16 July 2020), "
        "and Google's structured data documentation recommends JSON-LD and lists it as the "
        "recommended format.",
    ),
    "llms.txt": (
        BASIS_JUDGEMENT,
        "llms.txt is a published proposal (llmstxt.org, 2024) with no standards status: no IETF "
        "draft, no W3C document. Server-log data across 137,000 domains reports that 97% "
        "of the files received no requests at all, that AI retrieval bots accounted for about 1% "
        "of the requests that did occur, and that audit tooling was the largest requester; Google "
        "says Search ignores the file and that it neither helps nor harms visibility. We require "
        "it as a one-file bet on agents that navigate a site - not because anything measurably "
        "reads it today - and a site owner who would rather not pay that cost can drop it.",
    ),
    "rss.xml": (
        BASIS_PRACTICE,
        "RSS 2.0 has a published specification - from the RSS Advisory Board, not an IETF, W3C "
        "or ISO standard - and Atom is RFC 4287, a Proposed Standard. A feed is the "
        "long-standing machine-readable surface for dated content.",
    ),
}

#: The published sources a brief may cite. Only those its text actually names are listed.
SOURCES: tuple[tuple[str, str], ...] = (
    ("RFC 9309", "Robots Exclusion Protocol, https://www.rfc-editor.org/rfc/rfc9309"),
    ("sitemaps.org", "XML sitemaps protocol, https://www.sitemaps.org/protocol.html"),
    ("Schema.org", "type and property definitions, https://schema.org/"),
    ("JSON-LD 1.1", "W3C Recommendation, https://www.w3.org/TR/json-ld11/"),
    ("llmstxt.org", "the llms.txt proposal, https://llmstxt.org/ (not a standard)"),
    ("RSS 2.0", "https://www.rssboard.org/rss-specification"),
    ("RFC 4287", "Atom Syndication Format, https://www.rfc-editor.org/rfc/rfc4287"),
    ("RFC 3986", "URI syntax, https://www.rfc-editor.org/rfc/rfc3986"),
    (
        "Ahrefs llms.txt study",
        "server-log analysis of 137,000 domains reporting that 97% of llms.txt files received no "
        "requests: https://ahrefs.com/blog/llmstxt-study/ (fetched 2026-09-21; the page returns "
        "only its title to a text reader, so the figures here come from two secondary reports of "
        "it, cited in docs/CITATIONS.md)",
    ),
    (
        "Google's structured data documentation",
        "the feature guides for Local business, Organization, Merchant listing, Article, "
        "Software app, Carousel and Profile page, with the structured-data general guidelines: "
        "https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data",
    ),
)

URL_WHY = (
    "URL shape is chosen now because changing it later means redirects. RFC 3986 makes the scheme "
    "and host case-insensitive and says they should be normalized to lowercase, so lowercase "
    "hosts are published practice. It makes path segments case-sensitive, so lowercase paths, one "
    "trailing-slash convention and a depth limit are our judgement. The point is to pick one "
    "shape and keep it."
)

CRAWLER_MECHANISM = (
    "The stance is written into robots.txt; RFC 9309 defines that mechanism, and it binds only "
    "the crawlers that choose to follow it. It is not a technical or legal guarantee."
)

PAGES_WHY = (
    "The page set is our reading of what this kind of site needs. That the home page should carry "
    "the identity markup rests on published practice: Schema.org markup describes the page it "
    "appears on."
)


@dataclass(frozen=True)
class Advice:
    """One labelled recommendation, rendered into the brief under its group."""

    group: str
    basis: str
    why: str


@dataclass(frozen=True)
class Surface:
    """A machine-readable surface this kind must publish, with the reason for this kind."""

    name: str
    reason: str


@dataclass(frozen=True)
class UrlRules:
    lowercase: bool
    trailing_slash: str
    max_depth: int
    why: str


@dataclass(frozen=True)
class Profile:
    kind: str
    headline: str
    rationale: str
    identity_types: tuple[str, ...]
    identity_fields: tuple[str, ...]
    offering_types: tuple[str, ...]
    offering_fields: tuple[str, ...]
    surfaces: tuple[Surface, ...]
    urls: UrlRules
    crawler_stance: str
    pages: tuple[tuple[str, str], ...]
    # Notes composed into the advice; the reasons are built from these plus the current values.
    identity_types_note: str
    identity_fields_note: str
    offering_types_basis: str
    offering_types_note: str
    offering_types_note_selling: str
    offering_fields_basis: str
    offering_fields_note: str
    offering_fields_note_selling: str
    crawler_note: str
    pages_note: str
    #: The basis of the identity-type choice. It is a judgement for the kinds where a source
    #: documents the vocabulary but recommends nothing for that kind of site.
    identity_types_basis: str = BASIS_PRACTICE
    #: Set when a note is only true without the location properties, e.g. after --not-local.
    identity_fields_note_without_location: str = ""
    #: The answers the principal stated, as (flag, value), so a reason can cite the answer.
    stated: frozenset[tuple[str, bool]] = frozenset()

    @property
    def surface_names(self) -> tuple[str, ...]:
        return tuple(surface.name for surface in self.surfaces)

    @property
    def page_paths(self) -> tuple[str, ...]:
        return tuple(path for path, _ in self.pages)


# Field order for rendering and for adding a property without shuffling the list.
IDENTITY_FIELD_ORDER: tuple[str, ...] = (
    "name",
    "legalName",
    "url",
    "logo",
    "image",
    "description",
    "jobTitle",
    "address",
    "telephone",
    "email",
    "contactPoint",
    "openingHoursSpecification",
    "geo",
    "areaServed",
    "knowsAbout",
    "sameAs",
)

OFFERING_FIELD_ORDER: tuple[str, ...] = (
    "name",
    "description",
    "image",
    "url",
    "headline",
    "author",
    "datePublished",
    "dateModified",
    "sku",
    "brand",
    "offers",
    "price",
    "priceCurrency",
    "availability",
    "serviceType",
    "provider",
    "areaServed",
    "applicationCategory",
    "operatingSystem",
    "featureList",
    "itemListElement",
    "numberOfItems",
    "potentialAction",
)

LOCATION_FIELDS: tuple[str, ...] = (
    "address",
    "telephone",
    "openingHoursSpecification",
    "geo",
    "areaServed",
)

TRANSACTIONAL_FIELDS: tuple[str, ...] = ("offers", "price", "priceCurrency", "availability")

BOOKING_FIELDS: tuple[str, ...] = ("potentialAction",)


LOCAL_BUSINESS = Profile(
    kind="local-business",
    headline="a business that serves people in a place: a shop, a bakery, a restaurant, a tradesperson",
    rationale=(
        "A local business is looked for by someone asking where to get something nearby, so the "
        "entity that matters is the place, and the facts that matter are the address, the hours "
        "and the way to reach it. The offering is what the business does, which may be a service, "
        "goods, or both."
    ),
    identity_types=("LocalBusiness",),
    identity_fields=(
        "name",
        "url",
        "logo",
        "image",
        "description",
        "address",
        "telephone",
        "openingHoursSpecification",
        "geo",
        "areaServed",
        "sameAs",
    ),
    offering_types=("Service",),
    offering_fields=("name", "description", "serviceType", "areaServed", "provider", "url"),
    surfaces=(
        Surface(
            "robots.txt",
            "It states which paths are not public - a booking form, an admin page - so a crawler "
            "does not treat them as content.",
        ),
        Surface(
            "sitemap.xml",
            "Every page a visitor can reach in one list, including pages no other page links to.",
        ),
        Surface(
            "json-ld",
            "The place, its hours and its services in the form a machine reads without inferring "
            "them from prose, which is the only form it can rely on.",
        ),
        Surface(
            "llms.txt",
            "For an agent that navigates the site: a plain-text map, so it reads the same facts "
            "the pages state.",
        ),
    ),
    urls=UrlRules(
        lowercase=True,
        trailing_slash="never",
        max_depth=2,
        why="a service page sits at /services and nothing needs to nest deeper.",
    ),
    crawler_stance="open",
    pages=(
        ("/", "What the business is, where it is and when it is open, with the identity markup."),
        ("/services", "What it offers, one entry per service, each carrying the offering markup."),
        ("/about", "Who runs it and what they stand for, for a reader deciding whether to trust it."),
        ("/contact", "Address, hours, telephone and a map link, in one place."),
    ),
    identity_types_note=(
        "Google's structured data documentation for local businesses asks for the most specific "
        "sub-type possible, so if Schema.org defines a closer subtype - `Bakery`, `Restaurant`, "
        "`Plumber` and hundreds more - use it: a subtype carries everything `LocalBusiness` does."
    ),
    identity_fields_note=(
        "Google's structured data documentation for local businesses requires `name` and "
        "`address`, and recommends `telephone`, `geo`, `openingHoursSpecification` and `url`; the "
        "rest is our judgement."
    ),
    identity_fields_note_without_location=(
        "Google's structured data documentation for local businesses requires `name` and "
        "`address`; `address` is not required here."
    ),
    offering_types_basis=BASIS_JUDGEMENT,
    offering_types_note=(
        "`Service` is the neutral type for a business that offers work rather than goods. If it "
        "sells goods, `Product` with `Offer` is what Google's structured data documentation for "
        "merchant listings describes; if it serves food, Schema.org describes the offerings with "
        "`Menu` and `MenuItem`, which `hasMenuItem` links."
    ),
    offering_types_note_selling=(
        "`Product` with `Offer` is the published pattern for a product page, and Google's "
        "structured data documentation for merchant listings is written against it. That this "
        "business's goods are described this way rather than as a `Service` is our judgement."
    ),
    offering_fields_basis=BASIS_JUDGEMENT,
    offering_fields_note=(
        "`serviceType`, `provider` and `areaServed` are what make a `Service` checkable against "
        "the page that describes it."
    ),
    offering_fields_note_selling=(
        "`offers` carries the price, and `price`, `priceCurrency` and `availability` are what "
        "make it checkable; the rest of the list is our judgement about how much a product page "
        "owes a reader."
    ),
    crawler_note=(
        "the purpose of the site is to be found by someone asking for what this business does "
        "nearby. A business that does not want automated answers should choose `selective` "
        "instead."
    ),
    pages_note=(
        "It is deliberately short: on this kind of site every extra page competes with the one "
        "that answers the question."
    ),
)


ONLINE_STORE = Profile(
    kind="online-store",
    headline="a shop: products with prices, sold online and shipped",
    rationale=(
        "A store is judged on its products, and a product is a price and an availability "
        "statement attached to a thing. The machine-readable problem is per-product, so the "
        "identity of the store matters less than the consistency of the product pages."
    ),
    identity_types=("OnlineStore",),
    identity_fields=("name", "url", "logo", "image", "description", "contactPoint", "sameAs"),
    offering_types=("Product", "Offer"),
    offering_fields=(
        "name",
        "description",
        "image",
        "sku",
        "brand",
        "offers",
        "price",
        "priceCurrency",
        "availability",
        "url",
    ),
    surfaces=(
        Surface(
            "robots.txt",
            "Cart, checkout and account paths must not be crawled, and this is where that is said.",
        ),
        Surface(
            "sitemap.xml",
            "The catalogue is the site, and a sitemap is how a consumer enumerates it, including "
            "products reached only through search or filtering.",
        ),
        Surface(
            "json-ld",
            "Each product page states what the product is, what it costs and whether it is in "
            "stock, at the price it is actually sold for.",
        ),
        Surface(
            "llms.txt",
            "For an agent that navigates the catalogue: a map, so it reads the same facts a "
            "shopper does.",
        ),
    ),
    urls=UrlRules(
        lowercase=True,
        trailing_slash="never",
        max_depth=4,
        why="a product page under a category needs the room: /category/product is common, and "
        "deeper than that is usually a filter pretending to be a page.",
    ),
    crawler_stance="selective",
    pages=(
        ("/", "What the store sells, who runs it and how buying works."),
        ("/products", "The catalogue, in a form a visitor or a crawler can enumerate."),
        ("/product/<slug>", "One product: what it is, what it costs and whether it is available."),
        ("/about", "Who runs the store and what they promise about an order."),
        ("/contact", "How to reach a person about an order, including returns."),
        ("/policies", "Shipping, returns and privacy, where a buyer looks before paying."),
    ),
    identity_types_note=(
        "`OnlineStore` sits under `Organization` in Schema.org's hierarchy - `Organization` > "
        "`OnlineBusiness` > `OnlineStore` - so it carries the organization properties without a "
        "second block, and Google's structured data documentation recommends the subtype for an "
        "ecommerce site."
    ),
    identity_fields_note=(
        "A buyer deciding whether to trust a store needs to know who runs it and how to reach "
        "them. The address is not required unless the store also has a counter."
    ),
    offering_types_basis=BASIS_PRACTICE,
    offering_types_note=(
        "`Product` is the documented type for the thing sold. With nothing stated about selling "
        "there is no `Offer` here, and a store that does not sell is a contradiction worth "
        "settling before the build."
    ),
    offering_types_note_selling=(
        "`Product` with an `Offer` is the published pattern for a product page, and Google's "
        "structured data documentation for merchant listings is written against it."
    ),
    offering_fields_basis=BASIS_PRACTICE,
    offering_fields_note=(
        "The property names are Schema.org's; with nothing sold, no price is required. Our "
        "judgement adds `description`, `image` and `url` to the required set."
    ),
    offering_fields_note_selling=(
        "Google's structured data documentation for merchant listings requires `name` and "
        "`image` on the `Product` and `price` and `priceCurrency` on its `Offer`, and recommends "
        "`availability`; `sku` and `brand` are what make two listings the same product, and our "
        "judgement adds `description`, `image` and `url` to the required set."
    ),
    crawler_note=(
        "the catalogue should be readable by anything that might recommend it, while the cart, "
        "checkout, account pages and filter permutations should not be: they are either private "
        "or unbounded duplicates of pages already listed."
    ),
    pages_note=(
        "A store needs the policies a buyer checks before paying on a page of their own, because "
        "that is where they are looked for."
    ),
)


CONTENT_SITE = Profile(
    kind="content-site",
    headline="a site that publishes writing for people to read: a magazine, a blog, a research site",
    rationale=(
        "A content site is a body of dated work. What a machine needs is who published each piece "
        "and when, and what the site as a whole is, so that a citation can be attributed rather "
        "than guessed."
    ),
    identity_types=("Organization", "WebSite"),
    identity_fields=("name", "url", "logo", "description", "contactPoint", "sameAs"),
    offering_types=("Article", "BlogPosting"),
    offering_fields=(
        "headline",
        "description",
        "image",
        "author",
        "datePublished",
        "dateModified",
        "url",
    ),
    surfaces=(
        Surface(
            "robots.txt",
            "It keeps non-public paths - drafts, previews, admin - out of any index, and states "
            "the stance in one place.",
        ),
        Surface("sitemap.xml", "Every article, including the ones only reachable from an archive."),
        Surface(
            "json-ld",
            "Each article states its headline, author and dates, which is what makes it citable "
            "rather than merely quotable.",
        ),
        Surface(
            "llms.txt",
            "For an agent that navigates the site: a map of what it covers, so it can find the "
            "article that addresses a question rather than stopping at the home page.",
        ),
        Surface("rss.xml", "A feed is how a reader or an agent follows the site without polling it."),
    ),
    urls=UrlRules(
        lowercase=True,
        trailing_slash="never",
        max_depth=3,
        why="an article lives at /articles/<slug>; a dated archive path may add one level, and "
        "more than that makes a URL unguessable and unmergeable.",
    ),
    crawler_stance="open",
    pages=(
        ("/", "What the site publishes and who writes it, with the identity markup."),
        ("/articles", "Every published article, newest first."),
        ("/articles/<slug>", "One article, its author and its dates."),
        ("/about", "Who writes here, and what the site is for."),
        ("/contact", "How to reach the people who write it, including corrections."),
    ),
    identity_types_basis=BASIS_JUDGEMENT,
    identity_types_note=(
        "Google's structured data documentation for organizations recommends placing the "
        "organization's markup on the home page or on a single page that describes it. That "
        "`Organization` and `WebSite` together are the identity for a publication - and that a "
        "one-person publication is better described by `Person` - is our judgement."
    ),
    identity_fields_note=(
        "`sameAs` is the one that matters most here: it is how a machine ties the site to the "
        "same organization's other published profiles."
    ),
    offering_types_basis=BASIS_PRACTICE,
    offering_types_note=(
        "Schema.org defines `Article` and `BlogPosting` for published writing, and Google's "
        "structured data documentation for articles is written against them."
    ),
    offering_types_note_selling=(
        "`Article` and `BlogPosting` describe the writing; `Offer` is the published way to state "
        "the price of access to it. That both belong on the same page is our judgement."
    ),
    offering_fields_basis=BASIS_PRACTICE,
    offering_fields_note=(
        "Google's structured data documentation for articles has no required properties and "
        "recommends `headline`, `image`, `author`, `datePublished` and `dateModified`; those make "
        "a piece attributable and datable, which is the whole of its value to a citation. "
        "`description` and `url` are our additions."
    ),
    offering_fields_note_selling=(
        "`price` and `priceCurrency` state what access costs, and `availability` is meaningful "
        "only if access can sell out. That these belong alongside the article's own fields is our "
        "judgement."
    ),
    crawler_note=(
        "a site that publishes in order to be read and cited should refuse nothing by default. A "
        "paywalled or partly private publication should choose `selective`."
    ),
    pages_note=(
        "The article page carries the offering markup, and the index exists so that a reader or a "
        "crawler can enumerate the body of work without following links from the home page."
    ),
)


SAAS = Profile(
    kind="saas",
    headline="a product reached through a browser: software sold by subscription, with documentation",
    rationale=(
        "A software product is described in two registers: marketing pages that say what it does "
        "and who it is for, and documentation that says how to use it. A machine usually arrives "
        "at the second while answering a question, so the documentation is a first-class surface, "
        "not an appendix."
    ),
    identity_types=("Organization", "WebSite"),
    identity_fields=("name", "url", "logo", "description", "contactPoint", "sameAs"),
    offering_types=("SoftwareApplication",),
    offering_fields=(
        "name",
        "description",
        "applicationCategory",
        "operatingSystem",
        "featureList",
        "url",
    ),
    surfaces=(
        Surface(
            "robots.txt",
            "The application, the account area and the API are not public pages, and this is where "
            "that is stated rather than assumed.",
        ),
        Surface("sitemap.xml", "Marketing pages and documentation, in one enumerable list."),
        Surface(
            "json-ld",
            "The product, its category and its platform on the pages that describe it, instead of "
            "leaving them to be inferred from feature prose.",
        ),
        Surface(
            "llms.txt",
            "For an agent that navigates the documentation: a map of it, which is the cheapest "
            "surface a software product can publish.",
        ),
    ),
    urls=UrlRules(
        lowercase=True,
        trailing_slash="never",
        max_depth=3,
        why="documentation is a tree, so /docs/<page> is expected; a version prefix belongs in a "
        "path segment rather than another level.",
    ),
    crawler_stance="selective",
    pages=(
        ("/", "What the product does and who it is for."),
        ("/pricing", "What it costs and what each plan includes, in one comparable place."),
        ("/docs", "How to use it, starting here."),
        ("/docs/<page>", "One task or concept, with the version it applies to."),
        ("/about", "Who builds it, and what the company is."),
        ("/contact", "How to reach the people who build it: sales, support or security."),
    ),
    identity_types_basis=BASIS_JUDGEMENT,
    identity_types_note=(
        "Google's structured data documentation for organizations recommends placing the "
        "organization's markup on the home page or on a single page that describes it. That the "
        "vendor is `Organization` and the site is `WebSite`, and that keeping the two apart stops "
        "a machine from treating a company page as a product page, is our judgement."
    ),
    identity_fields_note=(
        "A buyer of business software checks who the vendor is, so `sameAs` and a reachable "
        "`contactPoint` carry more weight here than a logo does."
    ),
    offering_types_basis=BASIS_PRACTICE,
    offering_types_note=(
        "Schema.org defines `SoftwareApplication` for a software product, with "
        "`WebApplication` for one that runs only in a browser, and Google's structured data "
        "documentation documents a software app feature built on it."
    ),
    offering_types_note_selling=(
        "`SoftwareApplication` describes the product and `Offer` states what a plan costs. That "
        "the two belong in one block is our judgement."
    ),
    offering_fields_basis=BASIS_PRACTICE,
    offering_fields_note=(
        "Google's structured data documentation for software apps requires `name` and a price on "
        "an `Offer`, and one of `aggregateRating` or `review`, and recommends `applicationCategory` "
        "and `operatingSystem`. This plan requires the two recommended properties and leaves the "
        "price to what you state about selling and the rating to whether the site wants that "
        "feature; `description`, `featureList` and `url` are our additions."
    ),
    offering_fields_note_selling=(
        "`price` and `priceCurrency` are what make a plan comparable with another plan; "
        "`applicationCategory` and `operatingSystem` are the properties that make the product "
        "itself comparable."
    ),
    crawler_note=(
        "the documentation and the marketing pages should be readable by anything that might "
        "recommend the product, while the application, the account area and the API should not be "
        "crawled at all."
    ),
    pages_note=(
        "`/pricing` is required on its own path because it is the page a machine and a buyer both "
        "look for first, and burying it on the home page makes it unquotable."
    ),
)


DIRECTORY = Profile(
    kind="directory",
    headline="a site whose value is the list: it collects and organises entries that belong to others",
    rationale=(
        "A directory is a list plus a decision procedure about what belongs on it. The machine-"
        "readable problem is the list itself - its order, its size and its entries - because an "
        "entry page and a category page are otherwise indistinguishable to a crawler."
    ),
    identity_types=("WebSite", "Organization"),
    identity_fields=("name", "url", "logo", "description", "contactPoint", "sameAs"),
    offering_types=("ItemList", "ListItem"),
    offering_fields=(
        "name",
        "description",
        "url",
        "itemListElement",
        "position",
        "numberOfItems",
    ),
    surfaces=(
        Surface(
            "robots.txt",
            "Search and filter pages are unbounded near-duplicates of the entries; this is where "
            "they are excluded so the entries themselves can be found.",
        ),
        Surface(
            "sitemap.xml",
            "Every entry in one list, so a consumer can enumerate the directory instead of "
            "crawling the index.",
        ),
        Surface(
            "json-ld",
            "The list as an ordered set of entries, on the page that shows it, with the count, so "
            "a machine can tell a complete list from a page of it.",
        ),
        Surface(
            "llms.txt",
            "For an agent that navigates the directory: a map of what it covers and how it is "
            "organised.",
        ),
    ),
    urls=UrlRules(
        lowercase=True,
        trailing_slash="never",
        max_depth=3,
        why="an entry is /listings/<slug> and a category is /categories/<slug>; anything deeper "
        "is a filter combination that should not be a URL at all.",
    ),
    crawler_stance="selective",
    pages=(
        ("/", "What the directory covers, who keeps it and how an entry gets in."),
        ("/listings", "The index of entries, in a form a machine can enumerate."),
        ("/listings/<slug>", "One entry and its facts, attributed to its source."),
        ("/categories/<slug>", "One category of entries, with the list markup."),
        ("/about", "Who runs the directory and how entries are chosen."),
        ("/submit", "How to add or correct an entry."),
    ),
    identity_types_basis=BASIS_JUDGEMENT,
    identity_types_note=(
        "Google's structured data documentation for organizations recommends placing the "
        "organization's markup on the home page or on a single page that describes it. That a "
        "directory's identity is the site plus the person or organisation running it, and that "
        "the entries are not the site's identity, is our judgement."
    ),
    identity_fields_note=(
        "The selection procedure is the product here, so who runs the directory has to be stated "
        "rather than implied."
    ),
    offering_types_basis=BASIS_JUDGEMENT,
    offering_types_note=(
        "Schema.org defines `ItemList` and `ListItem` for an ordered set of things, and Google's "
        "structured data documentation documents a carousel built on an `ItemList` of at least "
        "two `ListItem`s. Its documented host types are narrow - course list, movie, recipe and "
        "restaurant - so for a general directory the list markup is our reading of those types, "
        "not a documented feature for it."
    ),
    offering_types_note_selling=(
        "`ItemList` and `ListItem` describe the list; `Offer` states what a paid placement costs. "
        "That the offer belongs on the placement page rather than on the entries is our judgement."
    ),
    offering_fields_basis=BASIS_JUDGEMENT,
    offering_fields_note=(
        "Google's carousel documentation requires an `ItemList` of at least two `ListItem`s of "
        "the same type, each carrying a `position` and the item's `url` - which is why `position` "
        "is in the list. `numberOfItems`, and using it so a consumer can tell a complete list "
        "from its first page, is our judgement."
    ),
    offering_fields_note_selling=(
        "`price` and `priceCurrency` state what a placement costs, and `numberOfItems` still "
        "describes the list itself. Keeping the two apart on the page is our judgement."
    ),
    crawler_note=(
        "entries should be readable by anything that might recommend one, while search results "
        "and filter permutations should not be crawled: they are unbounded near-duplicates of "
        "pages already listed."
    ),
    pages_note=(
        "A `/submit` page is required, because a directory that cannot be corrected by the people "
        "it describes accumulates errors that no amount of markup fixes."
    ),
)


PERSONAL = Profile(
    kind="personal",
    headline="a site about one person: who they are, what they have done and how to reach them",
    rationale=(
        "A personal site is small, and its job is to be the authoritative page about one person "
        "rather than the fourth-best guess. That makes `sameAs` links to profiles the person "
        "controls the main machine-readable work."
    ),
    identity_types=("Person", "WebSite"),
    identity_fields=("name", "url", "image", "description", "jobTitle", "sameAs", "knowsAbout"),
    offering_types=("Person",),
    offering_fields=("name", "description", "jobTitle", "knowsAbout", "url", "sameAs"),
    surfaces=(
        Surface("robots.txt", "One file stating what is and is not meant to be crawled."),
        Surface("sitemap.xml", "Every page, so the site is enumerated rather than guessed at."),
        Surface(
            "json-ld",
            "The person and the profiles that are provably the same person, which is what "
            "`sameAs` exists for.",
        ),
        Surface(
            "llms.txt",
            "For an agent that navigates the site: one small text file stating what each page is "
            "for, at a cost of almost nothing.",
        ),
    ),
    urls=UrlRules(
        lowercase=True,
        trailing_slash="never",
        max_depth=2,
        why="a personal site is a handful of pages; anything deeper is a file tree leaking into "
        "the URL.",
    ),
    crawler_stance="open",
    pages=(
        ("/", "Who this is, in a paragraph, with the identity markup."),
        ("/about", "The longer version: what they do and what they have done."),
        ("/contact", "How to reach them, and what they are reachable about."),
    ),
    identity_types_basis=BASIS_JUDGEMENT,
    identity_types_note=(
        "Google's structured data documentation documents a profile page built on `Person`. That "
        "a personal site should carry both types, because 'the site about this person' and 'this "
        "person' are different questions, is our judgement."
    ),
    identity_fields_note=(
        "`sameAs` is the load-bearing property on a personal site: it is how a machine confirms "
        "that this page and a profile elsewhere are the same person."
    ),
    offering_types_basis=BASIS_JUDGEMENT,
    offering_types_note=(
        "On a personal site the identity and the offering are the same entity, so the offering is "
        "named as `Person` rather than left empty. If the site publishes work, `Article` and "
        "`BlogPosting` describe the work itself."
    ),
    offering_types_note_selling=(
        "`Person` is still the site's subject, and `Product` with `Offer` describes what is being "
        "sold. That a personal site selling something should say so on its own page rather than "
        "in the identity block is our judgement."
    ),
    offering_fields_basis=BASIS_JUDGEMENT,
    offering_fields_note=(
        "`jobTitle` and `knowsAbout` are what make a personal site answerable to a question about "
        "a field rather than only to one about a name."
    ),
    offering_fields_note_selling=(
        "`price`, `priceCurrency` and `availability` are what make a sale checkable; `jobTitle` "
        "and `knowsAbout` are what identify the seller. Our judgement puts both on the page that "
        "sells."
    ),
    crawler_note=(
        "a personal site is usually meant to be read and cited. Whether you want automated "
        "systems reading it is a preference rather than a technical question, so `selective` or "
        "`closed` is a legitimate answer here and only you can give it."
    ),
    pages_note=(
        "Three pages are enough: the home page answers who, `/about` answers what, and `/contact` "
        "answers how."
    ),
)


PROFILES: dict[str, Profile] = {
    profile.kind: profile
    for profile in (LOCAL_BUSINESS, ONLINE_STORE, CONTENT_SITE, SAAS, DIRECTORY, PERSONAL)
}


# --- adjustments driven by what the principal stated -------------------------------------------------

#: What selling directly changes, per kind: (offering types, offering fields).
SELLS_YES: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "local-business": (
        ("Product", "Offer"),
        ("name", "description", "image", "url", "offers", "price", "priceCurrency", "availability"),
    ),
    "online-store": (("Product", "Offer"), ONLINE_STORE.offering_fields),
    "content-site": (
        ("Article", "BlogPosting", "Offer"),
        CONTENT_SITE.offering_fields + ("offers", "price", "priceCurrency", "availability"),
    ),
    "saas": (
        ("SoftwareApplication", "Offer"),
        SAAS.offering_fields + ("offers", "price", "priceCurrency"),
    ),
    "directory": (
        ("ItemList", "ListItem", "Offer"),
        DIRECTORY.offering_fields + ("offers", "price", "priceCurrency"),
    ),
    "personal": (
        ("Person", "Product", "Offer"),
        PERSONAL.offering_fields + ("offers", "price", "priceCurrency", "availability"),
    ),
}

#: What not selling changes, per kind. Kinds whose profile is already non-transactional are absent,
#: because for them the honest answer is that nothing changes.
SELLS_NO: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "online-store": (
        ("Product",),
        tuple(field for field in ONLINE_STORE.offering_fields if field not in TRANSACTIONAL_FIELDS),
    ),
}

#: Combinations that contradict the kind. The adjustment is still applied - the principal said it -
#: but the brief says out loud that the two do not fit.
TENSIONS: dict[tuple[str, str, bool], str] = {
    (
        "local-business",
        "local",
        False,
    ): "The kind is a local business, and you stated that it does not serve a local area. The "
    "location properties are dropped below, but a business with no local area may be a different "
    "kind - `online-store` or `content-site`.",
    (
        "online-store",
        "sells",
        False,
    ): "The kind is a store, and you stated that it does not sell directly. The plan below "
    "requires no prices, which is what an online store without selling means; if that is not what "
    "you meant, the kind is wrong.",
    (
        "content-site",
        "publishes",
        False,
    ): "The kind is a content site, and you stated that it publishes nothing. The plan below "
    "requires no feed; a site that publishes nothing is not a content site.",
    (
        "saas",
        "local",
        True,
    ): "A software product that serves a local area is unusual. The location properties are "
    "required below because you stated it, not because the kind expects it.",
}

_FLAG_GROUPS: dict[str, tuple[str, ...]] = {
    "sells": ("offering_types", "offering_fields"),
    "local": ("identity_fields",),
    "publishes": ("surfaces", "pages"),
    "bookings": ("offering_fields", "pages"),
}

_FLAG_SENTENCE: dict[tuple[str, bool], str] = {
    ("sells", True): "You stated that the site sells directly, so the transactional properties "
    "are required here.",
    ("sells", False): "You stated that the site does not sell directly, so the transactional "
    "properties are dropped.",
    ("local", True): "You stated that the site serves a local area, so the location properties "
    "are required here.",
    ("local", False): "You stated that the site does not serve a local area, so the location "
    "properties are dropped.",
    ("publishes", True): "You stated that the site publishes content, so a feed and a dated "
    "content section are required here.",
    ("publishes", False): "You stated that the site does not publish content, so no feed is "
    "required.",
    ("bookings", True): "You stated that a visitor can book a time, so a booking page and the "
    "booking action are required here.",
}


def _quoted(names: tuple[str, ...]) -> str:
    return ", ".join(f"`{name}`" for name in names)


def _joined(names: tuple[str, ...]) -> str:
    return " and ".join(f"`{name}`" for name in names)


def advice_for(profile: Profile) -> tuple[Advice, ...]:
    """Compose the labelled recommendations from the profile's current state."""
    identity_note = profile.identity_fields_note
    if "address" not in profile.identity_fields and profile.identity_fields_note_without_location:
        identity_note = profile.identity_fields_note_without_location
    selling = "Offer" in profile.offering_types

    entries = (
        Advice(
            "identity_types",
            profile.identity_types_basis,
            f"Schema.org defines {_joined(profile.identity_types)}. {profile.identity_types_note}",
        ),
        Advice(
            "identity_fields",
            BASIS_JUDGEMENT,
            f"The property names are Schema.org properties of "
            f"{_joined(profile.identity_types)}, so a consumer knows what they mean; that these "
            f"are the ones this site must publish is our judgement. {identity_note}",
        ),
        Advice(
            "offering_types",
            profile.offering_types_basis,
            profile.offering_types_note_selling if selling else profile.offering_types_note,
        ),
        Advice(
            "offering_fields",
            profile.offering_fields_basis,
            profile.offering_fields_note_selling if selling else profile.offering_fields_note,
        ),
        Advice(
            "urls",
            BASIS_JUDGEMENT,
            URL_WHY + f" Depth {profile.urls.max_depth} is enough here: {profile.urls.why}",
        ),
        Advice(
            "crawler",
            BASIS_JUDGEMENT,
            f"We recommend the stance {profile.crawler_stance} for this kind, because "
            f"{profile.crawler_note} " + CRAWLER_MECHANISM,
        ),
        Advice(
            "pages",
            BASIS_JUDGEMENT,
            PAGES_WHY + (f" {profile.pages_note}" if profile.pages_note else ""),
        ),
    )

    composed: list[Advice] = []
    for item in entries:
        extra = [
            _FLAG_SENTENCE[(flag, value)]
            for flag, value in sorted(profile.stated)
            if item.group in _FLAG_GROUPS[flag]
        ]
        composed.append(replace(item, why=item.why + " " + " ".join(extra)) if extra else item)
    return tuple(composed)


def _order(fields: tuple[str, ...], order: tuple[str, ...]) -> tuple[str, ...]:
    """Sort fields into the canonical order, keeping unknown names last and stable."""
    known = [field for field in order if field in fields]
    extra = [field for field in fields if field not in order]
    return tuple(known + extra)


def _add_page(
    pages: tuple[tuple[str, str], ...], path: str, purpose: str
) -> tuple[tuple[str, str], ...]:
    return pages if any(existing == path for existing, _ in pages) else pages + ((path, purpose),)


def _add_surface(surfaces: tuple[Surface, ...], name: str, reason: str) -> tuple[Surface, ...]:
    if any(surface.name == name for surface in surfaces):
        return surfaces
    return surfaces + (Surface(name, reason),)


def _drop_surface(surfaces: tuple[Surface, ...], name: str) -> tuple[Surface, ...]:
    return tuple(surface for surface in surfaces if surface.name != name)


def _stated(profile: Profile, flag: str, value: bool) -> Profile:
    return replace(profile, stated=profile.stated | {(flag, value)})


def _apply_flag(profile: Profile, flag: str, value: bool) -> Profile:
    """Apply one stated flag. Unstated flags are never applied, and never guessed.

    An answer that changes nothing is recorded as stated but leaves the profile alone, so the brief
    can say "nothing changes" rather than claiming a change that did not happen.
    """
    if flag == "sells":
        table = SELLS_YES if value else SELLS_NO
        if profile.kind not in table:
            return profile
        types, fields = table[profile.kind]
        fields = _order(fields, OFFERING_FIELD_ORDER)
        if types == profile.offering_types and fields == profile.offering_fields:
            return profile
        return _stated(
            replace(profile, offering_types=types, offering_fields=fields), flag, value
        )

    if flag == "local":
        if value:
            fields = _order(profile.identity_fields + LOCATION_FIELDS, IDENTITY_FIELD_ORDER)
        else:
            fields = tuple(
                field for field in profile.identity_fields if field not in LOCATION_FIELDS
            )
        if fields == profile.identity_fields:
            return profile
        return _stated(replace(profile, identity_fields=fields), flag, value)

    if flag == "publishes":
        if value:
            surfaces = _add_surface(
                profile.surfaces,
                "rss.xml",
                "You stated that the site publishes content, so a feed lets a reader or an agent "
                "follow it without polling.",
            )
            has_section = any(
                path.startswith(("/blog", "/articles", "/writing")) for path in profile.page_paths
            )
            pages = profile.pages
            if not has_section:
                pages = _add_page(
                    pages, "/blog", "Dated posts, newest first, each carrying BlogPosting markup."
                )
                pages = _add_page(pages, "/blog/<slug>", "One post, its author and its dates.")
            changed = replace(profile, surfaces=surfaces, pages=pages)
        else:
            surfaces = _drop_surface(profile.surfaces, "rss.xml")
            if surfaces == profile.surfaces:
                return profile
            changed = replace(profile, surfaces=surfaces)
        return _stated(changed, flag, value)

    if flag == "bookings":
        if not value:
            return profile  # not booking a time changes nothing the plan requires
        fields = _order(profile.offering_fields + BOOKING_FIELDS, OFFERING_FIELD_ORDER)
        pages = _add_page(
            profile.pages,
            "/book",
            "Pick an available time and complete the booking, with the booking action markup.",
        )
        if fields == profile.offering_fields and pages == profile.pages:
            return profile
        return _stated(replace(profile, offering_fields=fields, pages=pages), flag, value)

    raise ValueError(f"unknown flag: {flag}")  # pragma: no cover - flags are fixed


def apply_intent(profile: Profile, intent: SiteIntent) -> Profile:
    """Apply every flag the principal stated, in a fixed order. Unstated flags change nothing."""
    result = profile
    for flag, value in (
        ("sells", intent.sells),
        ("local", intent.local),
        ("publishes", intent.publishes),
        ("bookings", intent.takes_bookings),
    ):
        if value is not None:
            result = _apply_flag(result, flag, value)
    return result


def with_flag(profile: Profile, flag: str, value: bool) -> Profile:
    """Apply one stated answer on its own.

    Used for the brief's "what changes if you state it" section, which is computed by diffing
    rather than written by hand, so it cannot drift from the catalogue.
    """
    return _apply_flag(profile, flag, value)


def tensions(profile: Profile, intent: SiteIntent) -> tuple[str, ...]:
    """Combinations of kind and stated answer that do not fit each other."""
    found: list[str] = []
    for (kind, flag, value), message in TENSIONS.items():
        if kind != profile.kind:
            continue
        if intent.answer(flag) is value:
            found.append(message)
    return tuple(found)


def changes(before: Profile, after: Profile) -> tuple[str, ...]:
    """Describe what one stated answer would change, by diffing two profiles."""
    notes: list[str] = []
    for label, old, new in (
        ("identity fields", before.identity_fields, after.identity_fields),
        ("offering @type", before.offering_types, after.offering_types),
        ("offering fields", before.offering_fields, after.offering_fields),
        ("required surfaces", before.surface_names, after.surface_names),
        ("pages", before.page_paths, after.page_paths),
    ):
        added = [item for item in new if item not in old]
        removed = [item for item in old if item not in new]
        if not added and not removed:
            continue
        if added and not removed:
            notes.append(f"{label} would add {_quoted(tuple(added))}")
        elif removed and not added:
            notes.append(f"{label} would drop {_quoted(tuple(removed))}")
        else:
            notes.append(f"{label} would become {_quoted(new)}")
    if before.crawler_stance != after.crawler_stance:
        notes.append(f"crawler stance would become `{after.crawler_stance}`")
    return tuple(notes)
