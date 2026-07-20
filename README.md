# Keystone

**Keep essential feature requirements beside the code.**

Keystone records the essential behavior a project intends to preserve. It does
not need to describe everything. Tests alone cannot protect a defined feature:
an agent can remove the behavior and its tests while leaving the remaining
suite green. Keystone keeps selected requirements outside the implementation so
people and coding agents can review what must remain before changing code.

- **Tests answer:** Does the code behave as expected?
- **Keystone answers:** Does the project still preserve its defined features?

## Getting started

Give [`agent-prompt.md`](agent-prompt.md) to a coding agent. It drafts the
feature context, adds `KEYSTONE.md`, updates existing agent guidance, asks
before creating `AGENTS.md`, and proposes a focused set of essential
requirements for approval.

The setup adds:

```text
your-project/
├── KEYSTONE.md
├── AGENTS.md  (existing or approved)
└── feature-spec/
    ├── Settings.md
    ├── Settings.Accounts.md
    └── Search.md
```

## `KEYSTONE.md` explains the project and guides agents

This root-level file can explain what is being built, distinguish relevant
surfaces, and map them to feature names. It stays compatible with `README.md`
as the human-facing overview and `AGENTS.md` as repository-wide working
guidance.

For example, a native Mac app with a local MCP surface could explain that:

```text
Mail.*  describes behavior shared across both surfaces.
App.*   describes the native Mac experience.
MCP.*   describes the local MCP surface.
```

Read the full [Keystone agent guidance](KEYSTONE.md).

## Describe the features that must stay

You do not need to document every feature. For each one you want to protect,
create a Markdown file named after the feature. Describe what it must do, not
how the code is built.

```markdown
# Settings.Accounts

## Requirements

- Every configured account MUST appear exactly once.
- Users MUST be able to add, edit, recover, and remove accounts.
- Removing one account MUST NOT modify another account.
```

Need to describe something more specific? Add another part to the filename,
separated by a dot. `Settings.Accounts.Removal.md` includes the requirements
from `Settings.md` and `Settings.Accounts.md` because its name starts with those
names. The new file only needs the added requirements for removing an account.

Read the [full specification](SPEC.md) or the
[worked example](examples/feature-spec/Settings.Accounts.md).

## Repository map

- Root Markdown files define Keystone and explain how to adopt it.
- [`examples/`](examples/) contains a small example Keystone specification set.
- [`scripts/`](scripts/) contains the validator and website renderer.
- [`tests/`](tests/) contains validator tests.
- [`site/`](site/) contains only the static website and its generated
  specification page.

Open [`site/index.html`](site/index.html) to view the website locally.

## Validate the examples

```sh
python3 scripts/validate_feature_spec.py examples/feature-spec
python3 -m unittest discover -s tests
```

The validator uses only the Python standard library.

## Current status

Keystone is an early framework proposal. Its filename, inheritance, and
exception rules are usable now. The validator checks document names, headings,
removed sections, parent declarations, related references, and exception
sources.

## License

MIT License. See [LICENSE](LICENSE).
