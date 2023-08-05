# Fixed Point
NUMBER = "number"  # Up to 38 digits, with optional precision and scale
DECIMAL = "decimal"  # Synonymous with NUMBER
NUMERIC = "numeric"  # Synonymous with NUMBER
INT = "int"  # Synonymous with NUMBER, except precision and scale cannot be specified
INTEGER = (
    "integer"  # Synonymous with NUMBER, except precision and scale cannot be specified
)
BIGINT = (
    "bigint"  # Synonymous with NUMBER, except precision and scale cannot be specified
)
SMALLINT = (
    "smallint"  # Synonymous with NUMBER, except precision and scale cannot be specified
)
TINYINT = (
    "tinyint"  # Synonymous with NUMBER, except precision and scale cannot be specified
)
BYTEINT = (
    "byteint"  # Synonymous with NUMBER, except precision and scale cannot be specified
)


# Floating Point
FLOAT = "float"
FLOAT4 = "float4"
FLOAT8 = "float8"
DOUBLE = "double"  # Displayed as FLOAT but stored as DOUBLE
DOUBLE_PRECISION = "double precision"  # Displayed as FLOAT but stored as DOUBLE
REAL = "real"  # Displayed as FLOAT but stored as DOUBLE
