# Feature Spec

Feature Spec is a Markdown-native framework for documenting what a product is
intended to do. It gives maintainers and software agents one durable source of
truth for product requirements without requiring arbitrary feature IDs or a
second machine-readable catalog.

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

## Why Feature Spec

Implementation tests can pass after an agent removes both a feature and its
tests. Feature Spec keeps the product contract outside the implementation so a
green test suite cannot redefine intended behavior by omission.

The format is designed to be:

- readable and editable as ordinary Markdown;
- predictable for agents to resolve and navigate;
- portable across repositories and operating systems;
- composable through namespace inheritance;
- verifiable without duplicating content into YAML or JSON; and
- suitable for generated coverage and documentation tooling.

## Start here

- [Agent guidance for feature specifications](FEATURES.md)
- [Framework specification](SPECIFICATION.md)
- [Worked example](examples/feature-spec/Settings.Accounts.md)
- [Contributing](CONTRIBUTING.md)

Validate the included example repository:

```sh
python3 scripts/validate_feature_spec.py examples/feature-spec
```

The validator uses only the Python standard library.

## Current status

Feature Spec is an early framework proposal. The namespace, inheritance, and
exception rules are usable now. The initial validator checks document names,
headings, parent declarations, related-spec references, and exception sources.
Test-coverage discovery and effective-spec rendering are planned next.

## License

MIT License. See [LICENSE](LICENSE).
