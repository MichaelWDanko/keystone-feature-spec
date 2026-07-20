# Search.IndexManagement

Defines requirements for understanding and recovering a local search index.

## Status

Implemented

## Requirements

- Users MUST be able to determine whether the index is ready, updating, or in
  need of attention.
- Users MUST be able to rebuild the index.
- Rebuilding an index MUST preserve source records.
- Index maintenance MUST NOT prevent unrelated product use.

## Verification

- Rebuilding restores equivalent searchable records.
- Failure presents a recoverable state.
- Rebuilding one scope does not modify another scope.

## Related specifications

- `Settings.Accounts`
