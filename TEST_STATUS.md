# fbpro98-profile — Test Status

**Test Status: Tests Complete**

## Covered by automated tests

- Model invariants — substitution pairs/settings, category weights, situations, PAT situations, and the top-level profile all exercise construction and validation rules on synthesized instances.
- Situation-number ↔ game-state conversion — first/last pinned for both regular and PAT layouts; full round-trip for every valid situation number (2520 regular, 60 PAT); structural invalid combos rejected on encode; out-of-range numbers and mismatched game state rejected on construct.
- Stop-clock query — situation-number / situation pairing, filtering, exclusion of PAT.
- Real-fixture reader — the four `DEN-*.prf` fixtures pinned against expected metadata and the typed domain instances.
- Public API surface — path reader and buffer parser produce equivalent profiles; error-class hierarchy exercised.
- Structural error paths — bad magics/sizes, out-of-range fields, F95/I95 mismatches, invalid trailers, file-size parity, missing files.
- Unsupported-variant detection — synthetic stock-layout files, real game-shipped stock fixture, and synthetic embedded-game-plan files.
- Writer round-trip byte identity on all four baseline fixtures; mutation round-trips via `dataclasses.replace` for scalar and nested fields; F95/I95 redundancy implicitly verified; Stop-Clock bit packing/clearing on regular vs PAT records; in-place update and from-scratch construction workflows for both profile types.

## Needs tests

- Nothing outstanding for the current scope.
