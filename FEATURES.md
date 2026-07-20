# Feature specifications

Projects adopting Feature Spec SHOULD place this document in the repository
root as the agent-facing contract and keep their specifications in
`feature-spec/`. The Markdown documents in that directory are the durable
source of truth for intended product behavior. Implementation and tests MUST
adhere to the applicable feature specifications. Missing implementation,
missing tests, or current behavior MUST NOT be treated as evidence that a
documented requirement is obsolete.

## Agent responsibilities

Before changing product behavior, an agent MUST:

1. identify the most specific affected specification;
2. read its existing namespace parents from least specific to most specific;
3. read the target specification and any specifications named in its
   `Related specifications` section;
4. identify the effective inherited requirements and any declared exceptions;
5. make the implementation and verification coverage conform to that effective
   specification; and
6. report any conflict between the requested work and the specifications rather
   than silently weakening, bypassing, or removing a requirement.

When a new feature is added, the corresponding documents in `feature-spec/`
MUST be added or updated so the product contract remains complete. Feature
specifications MUST be changed only when the user explicitly requests the
change or confirms a proposed specification change. A request to change
implementation alone does not authorize a specification change. If the work
requires one, the agent MUST describe the proposed specification change and
obtain confirmation before editing `feature-spec/`.

## Efficient navigation

Do not load every file in `feature-spec/` into the context window. The flat,
dot-separated filenames form a navigable namespace. For example:

```text
feature-spec/
  Settings.md
  Settings.Accounts.md
  Settings.Accounts.Removal.md
  Search.md
  Search.IndexManagement.md
```

For work on `Settings.Accounts.Removal`, inspect only:

1. `Settings.md` if it exists;
2. `Settings.Accounts.md` if it exists;
3. `Settings.Accounts.Removal.md`; and
4. the files referenced by the target document's `Related specifications`
   section.

Start with filenames rather than file contents:

```sh
find feature-spec -maxdepth 1 -type f -name '*.md' -print | sort
```

Narrow the candidates by namespace or product language before opening files:

```sh
find feature-spec -maxdepth 1 -type f -name 'Settings*.md' -print | sort
rg -n -i 'account removal|remove account' feature-spec
```

After selecting a target, derive its parent chain from its dot-separated name
and open only that chain. Search the selected files for `Related
specifications`, then open only the referenced documents that are relevant to
the change. Use targeted `rg` searches to discover cross-cutting requirements;
do not concatenate or ingest the whole directory as a default discovery step.

If no applicable specification exists, do not assume the feature is
unconstrained. For implementation of a new feature, propose the smallest
appropriate specification and wait for explicit user confirmation before
creating it.
