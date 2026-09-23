#!/bin/sh
# Project checks. Everything that must be true before a commit belongs here.
#
# `make ci` runs this after the record check, so a failure here fails the build. What it
# establishes, and what it does not:
#
#   * the package and the tests byte-compile;
#   * the test suite passes with no network -- including the plan-format conformance fixtures in
#     docs/fixtures/, which pin what `siteplan check` accepts and rejects;
#   * `python3 -m siteplan` is runnable as the documented entry point;
#   * SKILL.md names the skill `siteplan` and carries a description, every `sh` block in it runs
#     from a directory outside this repository and writes both files, and every line it quotes
#     under "What this does not establish" appears verbatim in the BRIEF.md that run wrote.
#
# It does not establish that the format is a good format, that the recommendations are right, or
# that any site follows its plan. Nor does it establish that any session offers the skill, or that
# a report of a run carries the boundary. Those are review findings, not checks.
set -eu

cd "$(dirname "$0")/.."

PYTHON="${PYTHON:-python3}"

echo "== byte-compile =="
"$PYTHON" -m compileall -q siteplan tests

echo "== plan format: the conformance fixtures parse =="
"$PYTHON" -c '
import json, pathlib
path = pathlib.Path("docs/fixtures/plan-conformance.json")
document = json.loads(path.read_text(encoding="utf-8"))
version = document["plan_version"]
count = len(document["cases"])
assert version == 1, "the fixtures describe another plan_version"
print(f"{path}: {count} cases for plan_version {version}")
'

echo "== tests: offline, including the fixtures =="
"$PYTHON" -m unittest discover -s tests -t .

echo "== entry point =="
"$PYTHON" -m siteplan --version

echo "== skill: SKILL.md's commands run, and its boundary quotation matches the tool's output =="
"$PYTHON" - <<'PY'
import os, pathlib, re, subprocess, sys, tempfile

root = pathlib.Path.cwd().resolve()
skill = (root / "SKILL.md").read_text(encoding="utf-8")


def fail(message):
    print(f"SKILL.md: {message}", file=sys.stderr)
    sys.exit(1)


# The front matter is what a harness reads to list the skill.
front = re.match(r"---\n(.*?)\n---\n", skill, re.S)
if not front:
    fail("no front matter")
if not re.search(r"^name: siteplan$", front.group(1), re.M):
    fail("the front matter must carry 'name: siteplan'")
described = re.search(r"^description:[ \t]*(.*?)(?=^\S|\Z)", front.group(1), re.S | re.M)
description = " ".join(described.group(1).split()) if described else ""
description = re.sub(r"^[>|][-+]?\s*", "", description)
if not description:
    fail("the front matter carries no description")
if len(description) > 1024:
    fail(f"the description is {len(description)} characters; the limit is 1024")

# Every documented command, run in document order from a directory outside this repository.
blocks = re.findall(r"^```sh\n(.*?)^```", skill, re.S | re.M)
if not blocks:
    fail("no ```sh block, so no documented command")
script = "".join(blocks)
values = {"<skill-dir>": str(root), "<domain>": "example.com", "<name>": "East Side Bakery",
          "<kind>": "local-business", "<dir>": "plan"}
for placeholder, value in values.items():
    script = script.replace(placeholder, value)
leftover = re.findall(r"<[a-z-]+>", script)
if leftover:
    fail(f"the commands use placeholders this check does not know: {sorted(set(leftover))}")
environment = {key: value for key, value in os.environ.items() if key != "PYTHONPATH"}
with tempfile.TemporaryDirectory() as work:
    run = subprocess.run(["sh", "-eu", "-c", script], cwd=work, env=environment,
                         capture_output=True, text=True)
    if run.returncode != 0:
        fail(f"the documented commands exited {run.returncode}:\n{script}\n{run.stdout}{run.stderr}")
    written = pathlib.Path(work, "plan")
    for name in ("BRIEF.md", "site.json"):
        if not (written / name).is_file():
            fail(f"the documented commands did not write plan/{name}")
    brief = " ".join((written / "BRIEF.md").read_text(encoding="utf-8").split())

# The boundary: quoted, sourced, and word for word what the tool wrote.
section = re.search(r"^## What this does not establish\n(.*?)(?=^## |\Z)", skill, re.S | re.M)
if not section:
    fail("no '## What this does not establish' section")
if "`BRIEF.md`" not in section.group(1):
    fail("the boundary section does not name BRIEF.md as its source")
items, current = [], []
for line in section.group(1).splitlines():
    if not line.startswith(">"):
        continue
    text = line[1:].strip()
    if not text or text.startswith("- "):
        if current:
            items.append(" ".join(current))
        current = [text[2:]] if text else []
    else:
        current.append(text)
if current:
    items.append(" ".join(current))
items = [" ".join(item.split()) for item in items if item.strip()]
if not items:
    fail("the boundary section quotes nothing")
missing = [item for item in items if item not in brief]
if missing:
    fail("these quoted lines are not in the BRIEF.md the tool wrote:\n  " + "\n  ".join(missing))
print(f"SKILL.md: {len(blocks)} command blocks ran outside the repository; "
      f"{len(items)} quoted boundary lines match the tool's BRIEF.md")
PY

echo "project checks passed"
