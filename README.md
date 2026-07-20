# Feature Spec

Feature Spec is a Markdown-native framework for documenting selected essential
behavior that a project currently supports and intends to preserve. It gives
maintainers and software agents a durable source of truth for those feature
requirements without requiring arbitrary IDs or a second machine-readable
catalog. It does not need to describe everything the project can do.

Specifications use flat, dot-separated namespaces:

```text
feature-spec/
  Settings.md
  Settings.Accounts.md
  Settings.Accounts.Removal.md
```

Each document inherits the normative requirements of its existing namespace
parents. `Settings.Accounts.Removal`, for example, inherits `Settings` and
`Settings.Accounts`. A child can add or strengthen requirements but cannot
silently weaken them.

Root `KEYSTONE.md` also records the feature context needed to choose those
namespaces: what is being built, which surfaces or runtimes are distinct, and
which behavior they share. It can stand alone in a new project while remaining
compatible with `README.md` as the human-facing overview and `AGENTS.md` as
repository-wide working guidance.

## Why Feature Spec

Implementation tests can pass after an agent removes both a feature and its
tests. Feature Spec keeps essential feature contracts outside the implementation
so a green test suite cannot redefine specified behavior by omission. Planned
work and retired behavior stay outside the active specification.

The format is designed to be:

- readable and editable as ordinary Markdown;
- predictable for agents to resolve and navigate;
- portable across repositories and operating systems;
- composable through namespace inheritance;
- verifiable without duplicating content into YAML or JSON; and
- suitable for generated coverage and documentation tooling.

## Start here

- [Keystone agent guidance](KEYSTONE.md)
- [Framework specification](SPEC.md)
- [Worked example](examples/feature-spec/Settings.Accounts.md)
- [Contributing](CONTRIBUTING.md)

## Repository map

- Root Markdown files define Keystone and explain how to adopt it.
- [`examples/`](examples/) contains a small example feature specification set.
- [`scripts/`](scripts/) contains the validator and website renderer.
- [`tests/`](tests/) contains validator tests.
- [`site/`](site/) contains only the static website and its generated
  specification page.

Open [`site/index.html`](site/index.html) to view the website locally.

Validate the included example repository:

```sh
python3 scripts/validate_feature_spec.py examples/feature-spec
```

The validator uses only the Python standard library.

## Current status

Feature Spec is an early framework proposal. Its namespace, inheritance, and
exception rules are usable now. The initial validator checks document names,
headings, removed sections, parent declarations, related-spec references, and
exception sources. Test-coverage discovery and effective-spec rendering are
planned next.

## License

MIT License. See [LICENSE](LICENSE).
