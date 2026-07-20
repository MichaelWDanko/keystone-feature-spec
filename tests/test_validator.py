from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "validate_feature_spec.py"
SPEC = importlib.util.spec_from_file_location("validate_feature_spec", SCRIPT)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


class ValidatorTests(unittest.TestCase):
    def write(self, root: Path, name: str, body: str = "") -> None:
        (root / f"{name}.md").write_text(f"# {name}\n{body}", encoding="utf-8")

    def test_resolves_all_namespace_ancestors(self) -> None:
        self.assertEqual(
            validator.ancestors("Settings.Accounts.Removal"),
            ["Settings", "Settings.Accounts"],
        )

    def test_accepts_existing_parent_as_exception_source(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "Settings")
            self.write(
                root,
                "Settings.Accounts",
                "\n## Exceptions\n\n### Secret field\n\nSource: `Settings`\n",
            )
            documents, errors = validator.load_documents(root)
            errors.extend(validator.validate_exceptions(documents))
            self.assertEqual(errors, [])

    def test_rejects_sibling_as_exception_source(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "Settings")
            self.write(root, "Settings.General")
            self.write(
                root,
                "Settings.Accounts",
                "\n## Exceptions\n\n### Invalid source\n\n"
                "Source: `Settings.General`\n",
            )
            documents, errors = validator.load_documents(root)
            errors.extend(validator.validate_exceptions(documents))
            self.assertTrue(any("existing namespace parent" in error for error in errors))

    def test_rejects_unknown_related_specification(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(
                root,
                "Settings",
                "\n## Related specifications\n\n- `Missing.Specification`\n",
            )
            documents, errors = validator.load_documents(root)
            errors.extend(validator.validate_references(documents))
            self.assertTrue(any("unknown related specification" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
