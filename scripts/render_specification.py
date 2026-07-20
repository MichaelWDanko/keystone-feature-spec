#!/usr/bin/env python3
"""Render the canonical SPEC.md into the static specification page."""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "SPEC.md"
TEMPLATE = ROOT / "site" / "specification.template.html"
OUTPUT = ROOT / "site" / "specification.html"


def inline(value: str) -> str:
    escaped = html.escape(value, quote=True)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)


def slugify(value: str) -> str:
    value = value.lower().replace("`", "")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def render(markdown: str) -> tuple[str, str]:
    output: list[str] = []
    toc: list[tuple[str, str]] = []
    paragraph: list[str] = []
    list_type: str | None = None
    list_items: list[str] = []
    code_lines: list[str] | None = None
    section_open = False
    skipped_title = False

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            output.append(f"<p>{inline(' '.join(paragraph))}</p>")
            paragraph = []

    def flush_list() -> None:
        nonlocal list_type, list_items
        if list_type:
            output.append(f"<{list_type}>")
            output.extend(f"  <li>{item}</li>" for item in list_items)
            output.append(f"</{list_type}>")
            list_type = None
            list_items = []

    lines = markdown.replace("\r\n", "\n").split("\n")
    for line in lines:
        if code_lines is not None:
            if line.startswith("```"):
                output.append(f"<pre><code>{html.escape(chr(10).join(code_lines))}</code></pre>")
                code_lines = None
            else:
                code_lines.append(line)
            continue

        if line.startswith("```"):
            flush_paragraph()
            flush_list()
            code_lines = []
            continue

        heading = re.match(r"^(#{1,3})\s+(.+)$", line)
        if heading:
            flush_paragraph()
            flush_list()
            level = len(heading.group(1))
            text = heading.group(2)
            if level == 1 and not skipped_title:
                skipped_title = True
                continue
            if level == 2:
                if section_open:
                    output.append("</section>")
                section_id = slugify(text)
                toc.append((section_id, text))
                output.append(f'<section id="{section_id}">')
                output.append(f"<h2>{inline(text)}</h2>")
                section_open = True
            else:
                output.append(f"<h{level}>{inline(text)}</h{level}>")
            continue

        unordered = re.match(r"^\s*-\s+(.+)$", line)
        ordered = re.match(r"^\s*\d+\.\s+(.+)$", line)
        if unordered or ordered:
            flush_paragraph()
            next_type = "ul" if unordered else "ol"
            if list_type and list_type != next_type:
                flush_list()
            list_type = next_type
            list_items.append(inline((unordered or ordered).group(1)))
            continue

        if list_type and re.match(r"^\s{2,}\S", line):
            list_items[-1] += " " + inline(line.strip())
            continue

        if not line.strip():
            flush_paragraph()
            flush_list()
            continue

        flush_list()
        paragraph.append(line.strip())

    flush_paragraph()
    flush_list()
    if code_lines is not None:
        raise ValueError("Unclosed Markdown code fence")
    if section_open:
        output.append("</section>")

    toc_html = "\n".join(
        f'            <li><a href="#{section_id}">{html.escape(text)}</a></li>'
        for section_id, text in toc
    )
    content_html = "\n".join(f"          {line}" for line in output)
    return toc_html, content_html


def build() -> str:
    toc, content = render(SOURCE.read_text(encoding="utf-8"))
    template = TEMPLATE.read_text(encoding="utf-8")
    rendered = template.replace("{{SPEC_TOC}}", toc)
    rendered = rendered.replace("{{SPEC_CONTENT}}", content)
    return "<!-- Generated from SPEC.md by scripts/render_specification.py. -->\n" + rendered


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if site/specification.html is stale")
    arguments = parser.parse_args()
    rendered = build()

    if arguments.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != rendered:
            print("site/specification.html is stale; run scripts/render_specification.py", file=sys.stderr)
            return 1
        print("site/specification.html matches SPEC.md")
        return 0

    OUTPUT.write_text(rendered, encoding="utf-8")
    print(f"Rendered {OUTPUT.relative_to(ROOT)} from {SOURCE.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
