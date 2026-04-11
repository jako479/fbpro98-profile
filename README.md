# fbpro98-profile
Library for reading and writing Front Page Sports Football Pro '98 coaching profile (`.prf`) files.
## Setup
```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e ".[dev]"
```
## Usage
```python
from fbpro98_profile import read_profile

profile = read_profile("DEN-OGP1.prf")
print(profile.is_offense, profile.profile_type)
```
## Testing
```bash
pytest
```
