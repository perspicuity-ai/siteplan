"""The no-network fence, checked mechanically rather than promised.

Two checks: no module in the package imports a networking module, and a full run of ``new`` and
``check`` completes while socket creation is patched to fail. The second is the stronger one,
because it does not depend on recognizing every way Python can reach the network.
"""

from __future__ import annotations

import ast
import socket
import unittest
from pathlib import Path
from unittest import mock

from siteplan import format as plan_format
from siteplan.cli import PLAN_NAME

from tests.support import REPO_ROOT, make_site, run_cli, temp_dir

PACKAGE = REPO_ROOT / "siteplan"

#: Module roots that would let the tool reach the network. ``urllib.parse`` is allowed: it parses
#: a domain out of a string and opens nothing.
FORBIDDEN = {
    "asyncio",
    "ftplib",
    "http",
    "httplib",
    "imaplib",
    "poplib",
    "requests",
    "smtplib",
    "socket",
    "socketserver",
    "ssl",
    "telnetlib",
    "urllib.error",
    "urllib.request",
    "urllib3",
    "webbrowser",
    "xmlrpc",
}


def imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            found.add(node.module)
    return found


class SourcesImportNothingThatReachesTheNetwork(unittest.TestCase):
    def test_package_imports(self) -> None:
        files = sorted(PACKAGE.glob("*.py"))
        self.assertTrue(files, "no package modules found")
        for path in files:
            for module in imported_modules(path):
                root = module.split(".")[0]
                full = ".".join(module.split(".")[:2])
                with self.subTest(module=path.name, imported=module):
                    self.assertNotIn(root, FORBIDDEN)
                    self.assertNotIn(full, FORBIDDEN)

    def test_the_scanner_would_notice(self) -> None:
        """The check above is only worth having if it can fail."""
        with temp_dir() as name:
            sample = Path(name) / "sample.py"
            sample.write_text("import socket\nfrom urllib.request import urlopen\n", encoding="utf-8")
            found = imported_modules(sample)
        self.assertIn("socket", found)
        self.assertIn("urllib.request", found)


class ARunWorksWithSocketsDisabled(unittest.TestCase):
    def test_new_and_check_without_sockets(self) -> None:
        def refuse(*args: object, **kwargs: object) -> None:
            raise AssertionError("siteplan tried to open a socket")

        with temp_dir() as name, mock.patch("socket.socket", refuse), mock.patch(
            "socket.create_connection", refuse
        ), mock.patch("socket.getaddrinfo", refuse):
            self.assertEqual(socket.socket, refuse)  # the patch is live
            code, _, err = make_site(
                name,
                "--kind",
                "online-store",
                "--site",
                "example.com",
                "--sells",
                "--local",
                "--publishes",
                "--takes-bookings",
            )
            self.assertEqual(0, code, err)
            self.assertEqual([], plan_format.validate(__import__("json").loads(
                (Path(name) / PLAN_NAME).read_text(encoding="utf-8")
            )))
            check_code, _, check_err = run_cli("check", str(Path(name) / PLAN_NAME))
        self.assertEqual(0, check_code, check_err)


if __name__ == "__main__":
    unittest.main()
