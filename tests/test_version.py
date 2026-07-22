import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


class VersionTests(unittest.TestCase):
    def test_version_is_semantic_and_matches_public_surfaces(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertRegex(version, r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")

        surfaces = (
            "README.md",
            "SPEC.md",
            "agent-prompt.md",
            "site/index.html",
            "site/specification.template.html",
        )
        for relative_path in surfaces:
            with self.subTest(path=relative_path):
                content = (ROOT / relative_path).read_text(encoding="utf-8")
                self.assertIn(version, content)

    def test_zero_major_version_is_identified_as_a_draft(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        if version.startswith("0."):
            for relative_path in ("README.md", "SPEC.md", "agent-prompt.md", "site/index.html"):
                with self.subTest(path=relative_path):
                    content = (ROOT / relative_path).read_text(encoding="utf-8").lower()
                    self.assertIn("draft", content)


if __name__ == "__main__":
    unittest.main()
