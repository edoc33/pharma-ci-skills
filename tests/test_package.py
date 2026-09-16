import json
import re
import unittest
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/pharma-ci"
SKILL_COUNT = 9
REFERENCES = ("rule-grammar.md", "sources.md", "visualping-api.md", "m365-route.md")
BANNED = ("—",)  # em dash


class PackageTests(unittest.TestCase):
    def test_marketplace_points_to_matching_plugin_version(self):
        marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
        entry = marketplace["plugins"][0]
        directory = ROOT / entry["source"]
        plugin = json.loads((directory / ".claude-plugin/plugin.json").read_text())
        self.assertEqual(entry["name"], plugin["name"])
        self.assertEqual(entry["version"], plugin["version"])
        self.assertEqual(marketplace["metadata"]["version"], plugin["version"])

    def test_skill_names_and_shared_resources_are_discoverable(self):
        skills = list((PLUGIN / "skills").glob("*/SKILL.md"))
        self.assertEqual(len(skills), SKILL_COUNT)
        for skill in skills:
            with self.subTest(skill=skill.parent.name):
                text = skill.read_text()
                self.assertTrue(text.startswith("---\n"))
                frontmatter = text.split("---", 2)[1]
                name = re.search(r"^name: ([a-z0-9-]+)$", frontmatter, re.M)
                self.assertIsNotNone(name)
                self.assertEqual(name.group(1), skill.parent.name)
                self.assertIn("description:", frontmatter)
                self.assertTrue((skill.parent / "references/first-run.md").is_file())
                self.assertTrue((skill.parent / "agents/openai.yaml").is_file())
                for reference in REFERENCES:
                    self.assertTrue((skill.parent / "../../reference" / reference).resolve().is_file())

    def test_no_banned_characters_or_secrets(self):
        for document in [ROOT / "README.md", *list((ROOT / "docs").rglob("*.md")), *list(PLUGIN.rglob("*.md"))]:
            text = document.read_text()
            with self.subTest(document=str(document.relative_to(ROOT))):
                for char in BANNED:
                    self.assertNotIn(char, text)
                self.assertIsNone(re.search(r"\b(vp_[A-Za-z0-9]{16,}|sk-[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,})\b", text))

    def test_local_document_links_exist(self):
        documents = [ROOT / "README.md", *list((ROOT / "docs").rglob("*.md")), *list(PLUGIN.rglob("*.md"))]
        for document in documents:
            for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", document.read_text()):
                path = link.split("#", 1)[0]
                if not path or "://" in path or path.startswith("mailto:") or "${" in path:
                    continue
                with self.subTest(document=str(document.relative_to(ROOT)), link=link):
                    self.assertTrue((document.parent / unquote(path)).exists(), f"Missing local target: {link}")

    def test_example_csvs_have_headers(self):
        for csv_file in (PLUGIN / "examples").glob("*.csv"):
            with self.subTest(csv=csv_file.name):
                first = csv_file.read_text().splitlines()[0]
                self.assertIn(",", first)


if __name__ == "__main__":
    unittest.main()
