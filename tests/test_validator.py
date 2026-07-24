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
            self.assertTrue(
                any("applicable existing namespace parent" in error for error in errors)
            )

    def test_accepts_todo_document_with_target_name_heading(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "TODO.Settings.Accounts")
            path = root / "TODO.Settings.Accounts.md"
            path.write_text(
                "# Settings.Accounts\n\n## Requirements\n\n"
                "- Accounts MUST be validated.\n",
                encoding="utf-8",
            )
            documents, errors = validator.load_documents(root)
            self.assertEqual(errors, [])
            self.assertEqual(documents["TODO.Settings.Accounts"].name, "Settings.Accounts")
            self.assertTrue(documents["TODO.Settings.Accounts"].is_todo)

    def test_allows_active_and_todo_documents_for_same_target(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "Settings.Accounts")
            (root / "TODO.Settings.Accounts.md").write_text(
                "# Settings.Accounts\n\n## Requirements\n\n"
                "- Accounts MUST support pausing.\n",
                encoding="utf-8",
            )
            documents, errors = validator.load_documents(root)
            self.assertEqual(errors, [])
            self.assertEqual(
                set(documents), {"Settings.Accounts", "TODO.Settings.Accounts"}
            )

    def test_todo_exception_can_reference_todo_parent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "TODO.Settings.md").write_text(
                "# Settings\n\n## Requirements\n\n- Settings MUST persist.\n",
                encoding="utf-8",
            )
            (root / "TODO.Settings.Accounts.md").write_text(
                "# Settings.Accounts\n\n## Exceptions\n\n### Temporary accounts\n\n"
                "Source: `TODO.Settings`\n\nException: Temporary accounts MAY expire.\n\n"
                "Rationale: Their owner chose a limited lifetime.\n",
                encoding="utf-8",
            )
            documents, errors = validator.load_documents(root)
            errors.extend(validator.validate_exceptions(documents))
            self.assertEqual(errors, [])

    def test_active_specification_cannot_reference_todo_document(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "Settings")
            (root / "TODO.Settings.Accounts.md").write_text(
                "# Settings.Accounts\n",
                encoding="utf-8",
            )
            self.write(
                root,
                "Settings.General",
                "\n## Related specifications\n\n- `TODO.Settings.Accounts`\n",
            )
            documents, errors = validator.load_documents(root)
            errors.extend(validator.validate_references(documents))
            self.assertTrue(any("must not depend on TODO" in error for error in errors))

    def test_active_exception_cannot_reference_todo_parent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "Settings")
            (root / "TODO.Settings.md").write_text(
                "# Settings\n\n## Requirements\n\n- Settings MUST persist.\n",
                encoding="utf-8",
            )
            self.write(
                root,
                "Settings.Accounts",
                "\n## Exceptions\n\n### Invalid TODO source\n\n"
                "Source: `TODO.Settings`\n",
            )
            documents, errors = validator.load_documents(root)
            errors.extend(validator.validate_exceptions(documents))
            self.assertTrue(
                any("applicable existing namespace parent" in error for error in errors)
            )

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

    def test_rejects_status_section(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "Settings", "\n## Status\n\nImplemented\n")
            documents, errors = validator.load_documents(root)
            errors.extend(validator.validate_sections(documents))
            self.assertTrue(any("'Status' is not" in error for error in errors))

    def test_rejects_verification_section(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(
                root,
                "Settings",
                "\n## Verification\n\n- Confirm settings persist.\n",
            )
            documents, errors = validator.load_documents(root)
            errors.extend(validator.validate_sections(documents))
            self.assertTrue(any("'Verification' is not" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
