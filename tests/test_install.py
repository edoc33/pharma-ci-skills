import importlib.util
import tempfile
import unittest
from pathlib import Path

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
                    expected = (installer.PLUGIN / "reference" / reference).read_bytes()
                    self.assertEqual((target / "references" / reference).read_bytes(), expected)
                self.assertTrue((target / "scripts/vp_client.py").is_file())
                source = installer.PLUGIN / "skills" / target.name
                for original in source.rglob("*"):
                    if original.is_file():
                        self.assertEqual((target / original.relative_to(source)).read_bytes(), original.read_bytes())

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
