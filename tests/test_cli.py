"""The command line itself: usage errors, the interactive mode, and the module entry point."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

from siteplan import cli
from siteplan import format as plan_format

from tests.support import REPO_ROOT, make_site, read_brief, read_plan, run_cli, temp_dir


class UsageErrors(unittest.TestCase):
    def test_unknown_kind_is_rejected(self) -> None:
        with temp_dir() as name:
            code, _, err = make_site(name, "--kind", "shop")
        self.assertEqual(2, code)
        self.assertIn("invalid choice", err)

    def test_kind_is_required(self) -> None:
        with temp_dir() as name:
            code, _, err = make_site(name, "--site", "example.com")
        self.assertEqual(2, code)
        self.assertIn("--kind is required", err)

    def test_contradictory_flags_are_rejected(self) -> None:
        with temp_dir() as name:
            code, _, err = make_site(name, "--kind", "saas", "--sells", "--no-sells")
        self.assertEqual(2, code)
        self.assertIn("contradict each other", err)

    def test_check_rejects_an_unknown_argument(self) -> None:
        code, _, err = run_cli("check")
        self.assertEqual(2, code)
        self.assertIn("usage", err)

    def test_no_subcommand_is_a_usage_error(self) -> None:
        code, _, err = run_cli()
        self.assertEqual(2, code)
        self.assertIn("usage", err)


class ExitCodeContract(unittest.TestCase):
    """Three codes, ratified: 0 clean, 1 findings or an invalid plan, 2 a usage error."""

    def test_success_is_zero(self) -> None:
        with temp_dir() as name:
            code, _, err = make_site(name, "--kind", "saas", "--site", "example.com")
        self.assertEqual(0, code, err)

    def test_a_plan_that_fails_its_own_check_is_one(self) -> None:
        """The catalogue is the only thing that can produce this, and it is a finding, not a crash."""
        with temp_dir() as name, mock.patch(
            "siteplan.cli.plan.build", return_value={"site": "example.com"}
        ):
            code, _, err = make_site(name, "--kind", "saas")
        self.assertEqual(1, code)
        self.assertIn("fails its own check", err)
        self.assertIn("defect in the kind catalogue", err)

    def test_every_usage_error_is_two(self) -> None:
        cases = {
            "unknown kind": ("--kind", "shop"),
            "no kind": ("--site", "example.com"),
            "contradictory answers": ("--kind", "saas", "--sells", "--no-sells"),
            "unknown flag": ("--kind", "saas", "--force"),
            "no subcommand": (),
        }
        for label, argv in cases.items():
            with self.subTest(case=label), temp_dir() as name:
                code, _, _ = make_site(name, *argv) if argv else run_cli()
                self.assertEqual(2, code)

    def test_no_fourth_code_appears_in_the_module_contract(self) -> None:
        """The docstring is the contract a reader sees; `return 3` was the old fourth code."""
        source = (Path(__file__).resolve().parent.parent / "siteplan" / "cli.py").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("return 3", source)
        self.assertNotIn("--force", source.replace("no ``--force``", "").replace("No --force", ""))


class CheckCommand(unittest.TestCase):
    def test_accepts_a_generated_plan(self) -> None:
        with temp_dir() as name:
            self.assertEqual(0, make_site(name, "--kind", "saas", "--site", "example.com")[0])
            path = Path(name) / cli.PLAN_NAME
            code, out, err = run_cli("check", str(path))
        self.assertEqual(0, code, err)
        self.assertIn("ok", out)
        self.assertIn("kind saas", out)

    def test_rejects_a_malformed_plan_with_messages_on_stderr(self) -> None:
        with temp_dir() as name:
            path = Path(name) / "bad.json"
            path.write_text('{"plan_version": 1, "kind": "shop"}', encoding="utf-8")
            code, out, err = run_cli("check", str(path))
        self.assertEqual(1, code)
        self.assertEqual("", out)
        self.assertIn("1 problem", err)
        self.assertIn("kind: expected one of", err)

    def test_reports_every_fault_it_finds(self) -> None:
        with temp_dir() as name:
            path = Path(name) / "bad.json"
            path.write_text(
                '{"plan_version": 1, "kind": "shop", "required_surfaces": ["humans.txt"]}',
                encoding="utf-8",
            )
            code, _, err = run_cli("check", str(path))
        self.assertEqual(1, code)
        self.assertIn("2 problems", err)

    def test_missing_file_exits_non_zero(self) -> None:
        with temp_dir() as name:
            code, _, err = run_cli("check", str(Path(name) / "absent.json"))
        self.assertEqual(1, code)
        self.assertIn("cannot read", err)


class InteractiveMode(unittest.TestCase):
    answers = ["local-business", "example.com", "East Side Bakery", "y", "y", "n", ""]

    def test_answers_are_used_and_recorded(self) -> None:
        with temp_dir() as name, mock.patch("builtins.input", side_effect=self.answers):
            code, out, err = make_site(name, "--interactive")
            self.assertEqual(0, code, err)
            plan_file = read_plan(Path(name))
            brief = read_brief(Path(name))
        self.assertEqual("local-business", plan_file["kind"])
        self.assertEqual("example.com", plan_file["site"])
        self.assertIn("Offer", plan_file["offering"]["schema_types"])
        self.assertIn("asked interactively", brief)
        self.assertIn("Press Enter to leave an answer unstated", out)

    def test_supplied_flags_are_not_asked_again(self) -> None:
        with temp_dir() as name, mock.patch(
            "builtins.input", side_effect=["y", "y", "n", ""]
        ) as prompt:
            code, _, err = make_site(name, "--kind", "saas", "--site", "example.com",
                                     "--name", "Example", "--interactive")
            self.assertEqual(0, code, err)
            asked = " ".join(call.args[0] for call in prompt.call_args_list)
        self.assertNotIn("Which kind of site", asked)
        self.assertNotIn("Site domain", asked)
        self.assertIn("sell something directly", asked)

    def test_enter_leaves_an_answer_unstated(self) -> None:
        with temp_dir() as name, mock.patch(
            "builtins.input", side_effect=["personal", "", "", "", "", "", ""]
        ):
            code, _, err = make_site(name, "--interactive")
            self.assertEqual(0, code, err)
            brief = read_brief(Path(name))
            plan_file = read_plan(Path(name))
        self.assertNotIn("site", plan_file)
        self.assertIn("**unstated**", brief)

    def test_input_ending_early_writes_nothing(self) -> None:
        with temp_dir() as name, mock.patch("builtins.input", side_effect=EOFError):
            code, _, err = make_site(name, "--interactive")
            self.assertEqual(2, code)
            self.assertIn("input ended", err)
            self.assertEqual([], list(Path(name).iterdir()))

    def test_an_empty_kind_is_refused_rather_than_guessed(self) -> None:
        with temp_dir() as name, mock.patch("builtins.input", side_effect=[""]):
            code, _, err = make_site(name, "--interactive")
        self.assertEqual(2, code)
        self.assertIn("a kind is required", err)


class ModuleEntryPoint(unittest.TestCase):
    """`python3 -m siteplan` is the documented way to run this, so run it for real."""

    def test_version(self) -> None:
        done = subprocess.run(
            [sys.executable, "-m", "siteplan", "--version"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, done.returncode, done.stderr)
        self.assertIn("siteplan", done.stdout)

    def test_new_then_check(self) -> None:
        with temp_dir() as name:
            new = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "siteplan",
                    "new",
                    "--kind",
                    "directory",
                    "--site",
                    "example.com",
                    "--out",
                    name,
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, new.returncode, new.stderr)
            check = subprocess.run(
                [sys.executable, "-m", "siteplan", "check", str(Path(name) / cli.PLAN_NAME)],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(0, check.returncode, check.stderr)
        self.assertIn("ok", check.stdout)

    def test_it_can_be_run_from_another_directory(self) -> None:
        """The package is imported from this repository, not from the caller's directory."""
        with temp_dir() as name:
            done = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "siteplan",
                    "new",
                    "--kind",
                    "personal",
                    "--out",
                    name,
                ],
                cwd=name,
                env={"PYTHONPATH": str(REPO_ROOT), "PATH": "/usr/bin:/bin"},
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(0, done.returncode, done.stderr)


class HelpText(unittest.TestCase):
    def test_help_names_the_fences(self) -> None:
        code, out, _ = run_cli("--help")
        self.assertEqual(0, code)
        self.assertIn("No network, no crawling, no code generation", out)

    def test_kind_help_lists_every_kind(self) -> None:
        code, out, _ = run_cli("new", "--help")
        self.assertEqual(0, code)
        for kind in plan_format.KINDS:
            self.assertIn(kind, out)

    def test_intent_flag_help_lists_the_pairs(self) -> None:
        _, out, _ = run_cli("new", "--help")
        for flag in ("--sells", "--no-sells", "--local", "--not-local", "--publishes",
                     "--no-publishes", "--takes-bookings"):
            self.assertIn(flag, out)


if __name__ == "__main__":
    unittest.main()
