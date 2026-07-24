#!/usr/bin/env python3
"""Validate a Keystone feature-spec collection using only the standard library."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


NAME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9-]*(?:\.[A-Za-z][A-Za-z0-9-]*)*$")
REFERENCE_PATTERN = re.compile(r"^- `([^`]+)`\s*$")
SOURCE_PATTERN = re.compile(r"^Source:\s*`([^`]+)`\s*$")
REMOVED_SECTIONS = {"Status", "Verification"}
TODO_PREFIX = "TODO."


@dataclass(frozen=True)
class Document:
    name: str
    path: Path
    lines: list[str]
    is_todo: bool


def section_lines(document: Document, title: str) -> list[tuple[int, str]]:
    start: int | None = None
    result: list[tuple[int, str]] = []
    for number, line in enumerate(document.lines, start=1):
        if line == f"## {title}":
            start = number + 1
            continue
        if start is not None and line.startswith("## "):
            break
        if start is not None:
            result.append((number, line))
    return result


def ancestors(name: str) -> list[str]:
    segments = name.split(".")
    return [".".join(segments[:index]) for index in range(1, len(segments))]


def load_documents(root: Path) -> tuple[dict[str, Document], list[str]]:
    documents: dict[str, Document] = {}
    errors: list[str] = []
    for path in sorted(root.glob("*.md")):
        identifier = path.stem
        is_todo = identifier.startswith(TODO_PREFIX)
        name = identifier.removeprefix(TODO_PREFIX) if is_todo else identifier
        if not NAME_PATTERN.fullmatch(name):
            errors.append(f"{path}: invalid feature name {name!r}")
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        expected = f"# {name}"
        actual = lines[0] if lines else ""
        if actual != expected:
            errors.append(f"{path}: first line must be {expected!r}")
        if identifier in documents:
            errors.append(f"{path}: duplicate document name {identifier!r}")
        documents[identifier] = Document(name, path, lines, is_todo)
    if not documents:
        errors.append(f"{root}: no specification Markdown files found")
    return documents, errors


def validate_references(documents: dict[str, Document]) -> list[str]:
    errors: list[str] = []
    for document in documents.values():
        for number, line in section_lines(document, "Related specifications"):
            match = REFERENCE_PATTERN.fullmatch(line)
            if not match:
                continue
            reference = match.group(1)
            if reference not in documents:
                errors.append(
                    f"{document.path}:{number}: unknown related specification {reference!r}"
                )
            elif not document.is_todo and documents[reference].is_todo:
                errors.append(
                    f"{document.path}:{number}: active specifications must not depend "
                    f"on TODO document {reference!r}"
                )
    return errors


def validate_sections(documents: dict[str, Document]) -> list[str]:
    errors: list[str] = []
    for document in documents.values():
        for number, line in enumerate(document.lines, start=1):
            if not line.startswith("## "):
                continue
            title = line.removeprefix("## ")
            if title in REMOVED_SECTIONS:
                errors.append(
                    f"{document.path}:{number}: {title!r} is not a Feature Spec "
                    "section; express current supported behavior as requirements"
                )
    return errors


def validate_exceptions(documents: dict[str, Document]) -> list[str]:
    errors: list[str] = []
    for document in documents.values():
        active_sources = set(ancestors(document.name)) & documents.keys()
        todo_sources = {
            f"{TODO_PREFIX}{name}" for name in ancestors(document.name)
        } & documents.keys()
        valid_sources = active_sources | (todo_sources if document.is_todo else set())
        for number, line in section_lines(document, "Exceptions"):
            match = SOURCE_PATTERN.fullmatch(line)
            if not match:
                continue
            source = match.group(1)
            if source not in valid_sources:
                errors.append(
                    f"{document.path}:{number}: exception source {source!r} "
                    "must be an applicable existing namespace parent"
                )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="Path to a feature-spec directory")
    arguments = parser.parse_args()
    root = arguments.root
    if not root.is_dir():
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 2

    documents, errors = load_documents(root)
    errors.extend(validate_sections(documents))
    errors.extend(validate_references(documents))
    errors.extend(validate_exceptions(documents))

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    active_count = sum(not document.is_todo for document in documents.values())
    todo_count = sum(document.is_todo for document in documents.values())
    todo_label = "TODO document" if todo_count == 1 else "TODO documents"
    print(
        f"Validated {active_count} active specifications and "
        f"{todo_count} {todo_label} in {root}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
