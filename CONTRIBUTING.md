# Contributing

Feature Spec is being developed as a portable product-requirements framework.
Contributions should improve the format without making maintainers author the
same product intent in multiple representations.

## Principles

- Markdown is the authored source of truth.
- Canonical names come from filenames; contributors do not invent IDs.
- Parent inheritance is structural and deterministic.
- Requirements describe product intent rather than current implementation.
- Generated indexes and reports must never become additional authored sources.
- Tooling should remain language- and product-neutral.

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

1. Update `SPECIFICATION.md`.
2. Add or revise a minimal example demonstrating the behavior.
3. Update validation when the rule can be checked deterministically.
4. Add tests for validator behavior.
5. Update the roadmap if the change alters planned work.

## Proposals

For significant syntax or inheritance changes, open a proposal describing:

- the maintainer or agent problem;
- a concrete before-and-after example;
- inheritance and compatibility implications;
- deterministic validation opportunities; and
- why the change does not require duplicated product content.

## Public-repository safety

Examples must be fictional and contain no private customer information,
credentials, tokens, internal URLs, or proprietary product requirements copied
without permission.
