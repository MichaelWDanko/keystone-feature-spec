# Search.IndexManagement

Defines requirements for understanding and recovering a local search index.

## Requirements

- Users MUST be able to determine whether the index is ready, updating, or in
  need of attention.
- Users MUST be able to rebuild the index.
- Rebuilding an index MUST preserve source records.
- Rebuilding an index MUST restore equivalent searchable records.
- An index maintenance failure MUST leave the index in a recoverable state.
- Rebuilding one index scope MUST NOT modify another scope.
- Index maintenance MUST NOT prevent unrelated project use.

## Related specifications

- `Settings.Accounts`
