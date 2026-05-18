# fbpro98-profile — Architecture

Library that owns the FbPro '98 `.prf` coaching profile binary file format. Read-only at this stage.

## Module layout

```
src/fbpro98_profile/
├── __init__.py    # public API re-exports
├── model.py       # Profile, Situation, SubstitutionSettings, SubstitutionPair, ProfileType
├── reader.py      # parse_profile, read_profile, InvalidProfileError, UnsupportedProfileError
└── schema.py      # struct format strings for F95/I95 blocks
```

`specs/fbpro98-prf.hexpat` and `specs/prf.md` document the on-disk byte layout.

## What this package does

- Parses `.prf` files into a typed in-memory model
- Validates structural correctness (block magics, sizes, redundant F95/I95 fields agree, trailer length and bytes, file-size parity)
- Exposes a frozen, type-safe model for downstream consumers
- Exposes `Profile.stop_clock_situations` for retrieving situations with the Stop-Clock bit set

## What this package does NOT do

- Write profiles (write API deferred)
- Handle the older "stock" on-disk layout — `F95.size` ∈ {`0x3F69`, `0x4509`} → `UnsupportedProfileError`
- Handle profiles saved with embedded game plans — `I95.num_game_plan_blocks ≠ 0` or G95/J95/S98 magic after I95 → `UnsupportedProfileError`

## Validation

`InvalidProfileError`:
- Bad block magics or sizes
- F95/I95 disagree on `field_goal_range` or `use_audibles`
- `field_goal_range` outside [5, 50]; `use_audibles` not in {0, 1}
- Substitution pair violates `0 ≤ out ≤ in ≤ 100`
- Situation `weight` outside [0, 10] (after masking off Stop-Clock bit on weight1)
- Situation `play_category` outside [0x00, 0x1A]
- Trailer not exactly 1 byte (offense) / 2 bytes (defense), or any trailer byte not in {0x00, 0x69}
- File-size parity wrong for profile type

`UnsupportedProfileError`: stock-layout files; profiles with embedded game plans.

## Testing

- `tests/test_profile_model.py` — model invariants on synthesized instances
- `tests/test_profile_reader.py` — real-fixture parsing pinned against expected metadata, plus structural-error paths

The fixture `.prf` files in `tests/data/` are game-produced — authoritative for any wire-format question.
