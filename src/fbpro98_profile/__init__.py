"""Library for parsing and editing a Front Page Sports Football Pro '98 coaching profile (.prf).

The write/update API is not yet exposed while the shape of mutation operations
is being designed.
"""

from fbpro98_profile.model import (
    DEFENSE_DISPLAY_CATEGORIES,
    OFFENSE_DISPLAY_CATEGORIES,
    CategoryWeights,
    Profile,
    ProfileType,
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
    "CategoryWeights",
    "InvalidProfileError",
    "Profile",
    "ProfileType",
    "SubstitutionPair",
    "SubstitutionSettings",
    "UnsupportedProfileError",
    "parse_profile",
    "read_profile",
]
