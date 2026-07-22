# Keystone

**Keep essential feature requirements beside the code.**

**Current version: 0.1.0 (draft).** Keystone is usable now, but the framework
contract can still change before `1.0.0`. See [Versioning Keystone](VERSIONING.md).

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
    ├── Leash.Settings.md
    ├── Leash.Owners.md
    └── Leash.Walkers.md
```

## `KEYSTONE.md` explains the project and guides agents

This root-level file can explain what is being built, distinguish relevant
surfaces, and map them to feature names. It stays compatible with `README.md`
as the human-facing overview and `AGENTS.md` as repository-wide working
guidance. Its project-specific context is descriptive; essential behavior
belongs in normative requirements under `feature-spec/`.

For example, a fictional dog-walking app called Leash could explain that:

```text
Leash.Settings.*  describes shared app settings and safety rules.
Leash.Owners.*    describes the dog-owner experience.
Leash.Walkers.*   describes the dog-walker experience.
```

Read the full [Keystone agent guidance](KEYSTONE.md).

## Put shared requirements at the namespace root

A top-level specification holds requirements shared by every descendant in its
namespace. A single-product project can use a product-named root such as
`Leash.md` for product-wide guarantees inherited by `Leash.Owners` and
`Leash.Walkers`. `KEYSTONE.md` describes the product and maps those
namespaces; `Leash.md` defines the behavior they must preserve.

Not every repository needs one project-wide root. A monorepo can use separate
top-level namespaces such as `Desktop`, `Server`, and `Shared` when those are
the natural requirement boundaries.

When an agent adds behavior that is not covered by an existing specification,
it should ask whether the new feature belongs in Keystone's scope. If it does,
the agent proposes and gets confirmation for the smallest suitable
specification before writing it. If it does not, the behavior can remain
undocumented by design.

## Describe the features that must stay

You do not need to document every feature. For each one you want to protect,
create a Markdown file named after the feature. Describe what it must do, not
how the code is built.

```markdown
# Leash.Walkers

## Requirements

- Every walker profile MUST identify the walker and their service area.
- An unavailable walker MUST NOT be assigned a new walk.
- Updating one walker profile MUST NOT change another walker profile.
```

Need to describe something more specific? Add another part to the filename,
separated by a dot. `Leash.Walkers.Availability.md` includes the requirements
from `Leash.Walkers.md` because its name starts with that name. The new file
only needs the added requirements for showing walker availability.

Read the [full specification](SPEC.md) or the
[worked example](examples/feature-spec/Leash.Walkers.md).

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

Keystone `0.1.0` is an early framework release. Its filename, inheritance, and
exception rules are usable now, but the contract is not final. The validator
checks document names, headings, removed sections, parent declarations, related
references, and exception sources.

## License

MIT License. See [LICENSE](LICENSE).
