# fbpro98-profile — Test Status

**Test Status: Tests Complete**

## Covered by automated tests

- Model invariants — `SubstitutionPair`, `SubstitutionSettings`, `CategoryWeights`, `Situation`, `PatSituation`, and `Profile` construction and validation rules on synthesized instances.
- Situation index decoding — `Situation.from_index(0)` and `from_index(2519)` pinned against expected bucket dimensions; full round-trip property (`index_from_dimensions(*dimensions_from_index(i)) == i`) verified for all 2520 valid indices. Equivalent coverage for `PatSituation` across all 60 valid indices.
- Situation structural invariants — invalid combos (`SIX_TO_TEN` / `OVER_TEN` from `INSIDE_DEF_5`) raise on encode; out-of-range indices raise on decode; mismatched `situation_number` vs dimensions raises on direct construction.
- `stop_clock_situations` property — index/situation pairing, filtering of unflagged entries, and exclusion of PAT situations (which have no `stop_clock` concept).
- Real-fixture parsing — the four game-produced `DEN-*.prf` files pinned against expected metadata (profile type, field-goal range, substitutions, situations, PAT situations, stop-clock counts and indices). Reader output verified as `Situation` / `PatSituation` instances.
- Public API surface — `read_profile` / `parse_profile` equivalence and the error-class hierarchy.
- Structural error paths — bad block magics and sizes, out-of-range fields, F95/I95 mismatches, invalid trailers, file-size parity, and missing files.
- Unsupported-variant detection — stock-layout files and profiles with embedded game plans.

## Needs tests

- Nothing outstanding for the current scope.
