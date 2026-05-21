# fbpro98-profile — Test Status

**Test Status: Tests Complete**

## Covered by automated tests

- Model invariants — substitution pair/settings, category weights, regular situations, PAT situations, and the top-level profile all have construction and validation rules exercised on synthesized instances.
- Situation-number ↔ game-state conversion — first and last situation numbers pinned against expected game state for both regular and PAT layouts; full round-trip verified for every valid situation number (2520 regular, 60 PAT).
- Situation structural invariants — invalid combos (6-or-more yards to go from inside the DEF 5) are rejected on encode; out-of-range situation numbers are rejected on decode; a mismatch between situation number and game state is rejected on direct construction.
- Stop-clock query — situation-number / situation pairing, filtering of unflagged entries, and exclusion of PAT situations (which have no stop-clock concept).
- Real-fixture parsing — the four game-produced `DEN-*.prf` files pinned against expected metadata (profile type, field-goal range, substitutions, regular situations, PAT situations, stop-clock counts and indices). Reader output verified to be the typed domain instances.
- Public API surface — the path-based reader and the buffer-based parser produce equivalent profiles; error-class hierarchy is exercised.
- Structural error paths — bad block magics and sizes, out-of-range fields, F95/I95 mismatches, invalid trailers, file-size parity, and missing files.
- Unsupported-variant detection — stock-layout files and profiles with embedded game plans.

## Needs tests

- Nothing outstanding for the current scope.
