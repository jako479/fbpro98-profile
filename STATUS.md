# fbpro98-profile — Status

**Status: In Progress**

Library for reading and writing Front Page Sports Football Pro '98 coaching profile (`.prf`) files via a typed in-memory model.

## Implemented

- Parsing — reading a saved-layout `.prf` from disk or from a bytes buffer into a frozen, fully typed in-memory profile.
- Typed model — immutable profile, regular and PAT situations, category weights, substitution settings/pairs, and a profile-type (offense/defense) enum.
- Game-state enums — minutes remaining, down, yards-to-go, field position, and point spread for regular situations; PAT-specific minutes remaining and point spread.
- Situation-number ↔ game-state conversion — owned by the domain; situation numbers are 1-based and reconcile against the structural layout, with the invalid combination (inside the DEF 5 with 6-or-more yards to go) rejected.
- Profile data exposed — profile type, field-goal range, use-audibles flag, eight substitution position groups, 2520 regular situations (game state + stop-clock flag + weighted category picks), 60 PAT situations (game state + weighted category picks), and a stop-clock query that returns all situations with the flag set.
- Structural validation — block magics and sizes, agreement of redundant F95/I95 fields, field-range checks, trailer length and bytes, and file-size parity, with malformed bytes rejected. PAT records enforce a plain `weight1 ∈ [0, 10]` (no Stop-Clock bit on the PAT side).
- Unsupported-variant detection — stock-layout profiles and profiles saved with embedded game plans are rejected cleanly.

## Remaining

- Write/update API — bytes-out / mutation operations are not yet exposed.
- Support for the stock on-disk layout used by game-shipped profiles.
- Support for profiles saved with embedded game plans.
