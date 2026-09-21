#!/bin/sh
# Project checks. Everything that must be true before a commit belongs here.
#
# `make ci` runs this after the record check, so a failure here fails the build. What it
# establishes, and what it does not:
#
#   * the package and the tests byte-compile;
#   * the test suite passes with no network -- including the plan-format conformance fixtures in
#     docs/fixtures/, which pin what `siteplan check` accepts and rejects;
#   * `python3 -m siteplan` is runnable as the documented entry point.
#
# It does not establish that the format is a good format, that the recommendations are right, or
# that any site follows its plan. Those are review findings, not checks.
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

echo "project checks passed"
