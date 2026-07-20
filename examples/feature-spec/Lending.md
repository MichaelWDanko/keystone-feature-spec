# Lending

Defines requirements shared by borrowing workflows in the fictional community
tool library.

## Requirements

- A lending action MUST identify the member and item before completion.
- A completed lending action MUST communicate its outcome.
- A failed lending action MUST leave the member and item records unchanged.
- An active loan MUST offer renewal when no other member has reserved the item.
- Lending status MUST NOT rely on color alone.
