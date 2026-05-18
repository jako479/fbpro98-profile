"""Library for parsing and editing a Front Page Sports Football Pro '98 coaching profile (.prf).

Read-only at this stage. A write/update API is intentionally not yet exposed
while the shape of mutation operations is being designed.
"""

from fbpro98_profile.model import (
    DEFENSE_DISPLAY_CATEGORIES,
    OFFENSE_DISPLAY_CATEGORIES,
    Profile,
    ProfileType,
    Situation,
    SubstitutionPair,
    SubstitutionSettings,
)
from fbpro98_profile.reader import (
    InvalidProfileError,
    UnsupportedProfileError,
    parse_profile,
    read_profile,
)

__all__ = [
    "DEFENSE_DISPLAY_CATEGORIES",
    "OFFENSE_DISPLAY_CATEGORIES",
    "InvalidProfileError",
    "Profile",
    "ProfileType",
    "Situation",
    "SubstitutionPair",
    "SubstitutionSettings",
    "UnsupportedProfileError",
    "parse_profile",
    "read_profile",
]
