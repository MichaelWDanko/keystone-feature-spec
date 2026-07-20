# Lending.Loans

Defines requirements for borrowing and managing tool loans.

## Requirements

- Every active loan MUST identify the item, member, and due date.
- An unavailable item MUST NOT be checked out to another member.
- Users MUST be told why a checkout cannot be completed.
- Renewing one loan MUST NOT change another loan.
- Returning an item MUST make it available for future loans.

## Exceptions

### Reserved items cannot be renewed

Source: `Lending`

Exception: An active loan cannot be renewed when another member has reserved
the item.

Rationale: The reservation gives the next member a fair chance to borrow the
item.

## Related specifications

- `Catalog.Availability`
