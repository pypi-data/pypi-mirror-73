DATE = "date"  # No time elements
TIME = "time"  # HH:MI:SS

TIMESTAMP_LTZ = "timestamp_ltz"  # UTC time with specified precision; operations performed in current session's tz
TIMESTAMP_NTZ = "timestamp_ntz"  # Wallclock time with specified precision; operations performed without taking any tz into account
TIMESTAMP_TZ = "timestamp_tz"  # UTC time with associated tz offset; session tz offset of no offset is provided


# Aliases
DATETIME = "datetime"  # Alias of TIMESTAMP_LTZ
TIMESTAMP = "timestamp"  # User-specific alias via TIMESTAMP_TYPE_MAPPING session param; TIMESTAMP_NTZ by default
