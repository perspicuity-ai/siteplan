"""siteplan - turn a site's intent into an agent-first design brief.

Two things come out of a run:

* ``BRIEF.md`` - the human-readable brief, one labelled basis per recommendation.
* ``site.json`` - the machine-readable plan, which ``sitewalk --plan`` consumes.

Standard library only, no network, no crawling, no code generation. The plan file format is
specified in ``docs/PLAN-FORMAT.md``; this project owns it.
"""

__version__ = "0.1.0"
