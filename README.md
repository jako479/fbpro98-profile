# fbpro98-profile

Library for reading and writing Front Page Sports Football Pro '98 coaching profile (`.prf`) files.

Parsing is implemented; the write/update API is not yet exposed.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e ".[dev]"
```

## Usage

```python
from fbpro98_profile import read_profile

profile = read_profile("DEN-OFF1.prf")

profile.profile_type           # ProfileType.OFFENSE / DEFENSE
profile.field_goal_range       # int, 5-50
profile.use_audibles           # bool
profile.substitutions          # SubstitutionSettings (8 position groups)
profile.category_weights       # tuple of 2520 CategoryWeights — one per situation
profile.pat_category_weights   # tuple of 60 CategoryWeights — one per PAT situation
profile.stop_clock_situations  # ((index, CategoryWeights), ...) — situations with Stop-Clock set
```

`parse_profile(buffer)` is the bytes-in entry point; `read_profile` wraps file I/O.

## Unsupported variants

Two structurally-valid `.prf` variants are rejected with `UnsupportedProfileError`:

- **Stock layout** — the older format used by game-shipped profiles (e.g. `OFF1.PRF`, `DEF1.PRF`). Detected via `F95.size` ∈ {`0x3F69`, `0x4509`}. Re-saving any stock profile in the game converts it to the readable saved layout (`0x3C9D`).
- **Embedded game plans** — a profile saved together with one or more game plans appended after I95. Detected via `I95.num_game_plan_blocks ≠ 0` or a `G95:` / `J95:` / `S98:` magic after I95.

`InvalidProfileError` is reserved for genuinely malformed bytes.

## Testing

```bash
pytest
```
