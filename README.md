# Keystone

**Define your product beside the code.**

**Current version: 0.2.0 (draft).** Keystone is usable now, but the framework
contract can still change before `1.0.0`. See
[Versioning Keystone](VERSIONING.md) and the [changelog](CHANGELOG.md).

Keystone turns product intent into structured Markdown that people and coding
agents can follow. A project can define an entire product or only the features
that need a durable contract. Anything else remains undocumented by design.

Keystone keeps two kinds of documents together:

- active specifications describe implemented behavior that must remain true;
- `TODO.*.md` documents describe intended behavior that has not been built.

Tests show whether code behaves as expected. Keystone shows whether the code
matches the product that was defined.

## Getting started

Give [`agent-prompt.md`](agent-prompt.md) to a coding agent. It drafts the
product context, adds `KEYSTONE.md`, updates existing agent guidance, asks
before creating `AGENTS.md`, and proposes a focused set of active and TODO
documents for approval.

The setup adds:

```text
your-project/
├── KEYSTONE.md
├── AGENTS.md  (existing or approved)
└── feature-spec/
    ├── Leash.Settings.md
    ├── Leash.Owners.md
    ├── Leash.Walkers.md
    └── TODO.Leash.Walkers.Scheduling.md
```

## Define as much of the product as needed

`KEYSTONE.md` explains what is being built, distinguishes relevant surfaces,
and maps them to feature namespaces. Normative product behavior belongs in the
Markdown files under `feature-spec/`.

A product can define broad guarantees at a namespace root and add detail in
descendants. For example, `Leash.md` can define product-wide behavior inherited
by `Leash.Owners.md` and `Leash.Walkers.md`. A monorepo can instead use separate
roots such as `Desktop`, `Server`, and `Shared`.

Keystone does not require complete coverage. A project can define one important
feature, every product surface, or anything in between.

## Distinguish current behavior from intended behavior

An unprefixed file is an active Keystone specification:

```text
feature-spec/Leash.Walkers.md
```

Its requirements describe implemented, supported behavior. Applicable
implementation and tests must conform to it.

A file prefixed with `TODO.` defines behavior that has not been implemented:

```text
feature-spec/TODO.Leash.Walkers.Scheduling.md
```

The prefix is not part of the target feature name, so its first heading remains:

```markdown
# Leash.Walkers.Scheduling
```

TODO documents are product definitions, not backlog items. They do not assign,
prioritize, schedule, or authorize work. When someone chooses to implement one,
its requirements define what the completed feature must do. After the behavior
is implemented and verified, reconcile it with any matching active
specification and remove the `TODO.` prefix.

An active specification and TODO document may target the same feature:

```text
feature-spec/Leash.Walkers.md
feature-spec/TODO.Leash.Walkers.md
```

The active file governs the current product. The TODO file defines its intended
replacement or expansion. They must be reconciled when the TODO behavior ships.

## Write product requirements, not implementation instructions

Describe what a feature must do, not how its code is built:

```markdown
# Leash.Walkers

## Requirements

- Every walker profile MUST identify the walker and their service area.
- An unavailable walker MUST NOT be assigned a new walk.
- Updating one walker profile MUST NOT change another walker profile.
```

Need something more specific? Add another dot-separated segment.
`Leash.Walkers.Availability.md` inherits active requirements from
`Leash.Walkers.md`.

Read the [full specification](SPEC.md), the
[active example](examples/feature-spec/Leash.Walkers.md), or the
[TODO example](examples/feature-spec/TODO.Leash.Walkers.Scheduling.md).

## Repository map

- Root Markdown files define Keystone and explain how to adopt it.
- [`examples/`](examples/) contains a small example Keystone collection.
- [`scripts/`](scripts/) contains the validator and website renderer.
- [`tests/`](tests/) contains validator and version tests.
- [`site/`](site/) contains the static website and generated specification page.

## Validate the examples

```sh
python3 scripts/validate_feature_spec.py examples/feature-spec
python3 -m unittest discover -s tests
```

The validator uses only the Python standard library.

## Current status

Keystone `0.2.0` is an early framework release. Its active specifications,
TODO documents, filename, inheritance, exception, and reference rules are
usable now, but the contract is not final.

## License

MIT License. See [LICENSE](LICENSE).
