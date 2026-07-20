# Website files

This directory contains the static Keystone website.

- `index.html` is the landing page.
- `styles.css` contains the shared website styles.
- `specification.template.html` is the authored page template.
- `specification.html` is generated from root [`SPEC.md`](../SPEC.md). Do not
  edit it directly.

Regenerate the specification page from the repository root:

```sh
python3 scripts/render_specification.py
```
