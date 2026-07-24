# Contributing

Keystone is being developed as a portable product-definition framework.
Contributions should improve the format without making maintainers author the
same feature intent in multiple representations.

## Principles

- Markdown is the authored source of truth.
- Feature names come from filenames; contributors do not invent IDs.
- Parent inheritance is structural and deterministic.
- Active requirements describe implemented, supported behavior.
- `TODO.*.md` documents define intended behavior that has not been implemented.
- TODO documents define product behavior without becoming a backlog.
- Generated indexes and reports must never become additional authored sources.
- Tooling should remain language- and domain-neutral.

## Development

Run the validator against the examples:

```sh
python3 scripts/validate_feature_spec.py examples/feature-spec
```

Run its tests:

```sh
python3 -m unittest discover -s tests
```

When changing the framework:

1. Update `SPEC.md`.
2. Add or revise a minimal example demonstrating the behavior.
3. Update validation when the rule can be checked deterministically.
4. Add tests for validator behavior.
5. Update `CHANGELOG.md` when the change affects the published contract.

## Proposals

For significant syntax or inheritance changes, open a proposal describing:

- the maintainer or agent problem;
- a concrete before-and-after example;
- inheritance and compatibility implications;
- deterministic validation opportunities; and
- why the change does not require duplicated feature content.

## Public-repository safety

Examples must be fictional and contain no private customer information,
credentials, tokens, internal URLs, or proprietary feature requirements copied
without permission.
