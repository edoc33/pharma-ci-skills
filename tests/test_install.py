import importlib.util
import re
import shlex
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("install_codex", ROOT / "scripts/install_codex.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.destination = Path(self.temp.name) / "skills with spaces"

    def test_dry_run_writes_nothing(self):
        targets = installer.install(self.destination, True)
        self.assertEqual(len(targets), installer.SKILL_COUNT)
        self.assertFalse(self.destination.exists())

    def test_every_installation_is_self_contained(self):
        targets = installer.install(self.destination)
        for target in targets:
            with self.subTest(skill=target.name):
                self.assertTrue((target / "SKILL.md").is_file())
                for reference in installer.REFERENCES:
                    self.assertTrue((target / "references" / reference).is_file())
                self.assertTrue((target / "scripts/vp_client.py").is_file())
                source = installer.PLUGIN / "skills" / target.name
                for original in source.rglob("*"):
                    if original.is_file() and original.suffix != ".md":
                        self.assertEqual((target / original.relative_to(source)).read_bytes(), original.read_bytes())
                for original in (installer.PLUGIN / "examples").rglob("*"):
                    if original.is_file():
                        self.assertEqual((target / "examples" / original.relative_to(installer.PLUGIN / "examples")).read_bytes(), original.read_bytes())
                for original in (ROOT / "docs/starter-pack").rglob("*"):
                    if original.is_file() and original.suffix != ".md":
                        self.assertEqual((target / "docs/starter-pack" / original.relative_to(ROOT / "docs/starter-pack")).read_bytes(), original.read_bytes())

    def test_installed_instructions_resolve_resources_without_checkout(self):
        targets = installer.install(self.destination)
        for target in targets:
            with self.subTest(skill=target.name):
                skill = (target / "SKILL.md").read_text()
                self.assertNotIn("${CLAUDE_PLUGIN_ROOT}", skill)
                self.assertNotIn("../../reference/", skill)
                self.assertNotIn("../../examples/", skill)
                for resource in re.findall(r"`((?:references|examples)/[^`]+)`", skill):
                    self.assertTrue((target / resource).is_file(), resource)
                for document in target.rglob("*.md"):
                    for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", document.read_text()):
                        path = link.split("#", 1)[0]
                        if path and "://" not in path and not path.startswith("mailto:"):
                            resolved = (document.parent / unquote(path)).resolve()
                            self.assertTrue(resolved.is_relative_to(target), f"External install dependency: {document}: {link}")
                            self.assertTrue(resolved.exists(), f"Broken installed link: {document}: {link}")
                helper = str(target / "scripts/vp_client.py")
                command = "python3 " + shlex.quote(helper) + " --help"
                self.assertIn(shlex.quote(helper), skill)
                result = subprocess.run(shlex.split(command), cwd=self.temp.name, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_missing_examples_fail_before_dry_run_or_writes(self):
        with patch.object(installer, "EXAMPLES", (*installer.EXAMPLES, "missing-required.csv")):
            with self.assertRaises(ValueError):
                installer.install(self.destination, True)
        self.assertFalse(self.destination.exists())

    def test_existing_skill_stops_before_other_skills_are_written(self):
        existing = self.destination / "pharma-ci-watchlist"
        existing.mkdir(parents=True)
        (existing / "SKILL.md").write_text("user changes")
        with self.assertRaises(FileExistsError):
            installer.install(self.destination)
        self.assertEqual((existing / "SKILL.md").read_text(), "user changes")
        self.assertEqual(sorted(p.name for p in self.destination.iterdir()), ["pharma-ci-watchlist"])


if __name__ == "__main__":
    unittest.main()
