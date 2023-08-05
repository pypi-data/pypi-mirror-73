from dataclasses import dataclass, field
from typing import List
from snowday.exceptions import InvalidParamsException
from snowday.privileges import DATABASE_PRIVILEGES, SCHEMA_PRIVILEGES
from snowday.types.account import AccountObject
from snowday.util import get_resource_type, settings_str_from


# https://docs.snowflake.com/en/sql-reference/sql/create.html


def get_fqn(db_schema_or_string):
    if isinstance(db_schema_or_string, str):
        return db_schema_or_string
    else:
        return db_schema_or_string.fq_name


@dataclass
class Database(AccountObject):
    comment: str = ""
    data_retention_time_in_days: int = 1
    transient: bool = False
    if_not_exists: bool = False

    def __post_init__(self):
        self._available_privileges = DATABASE_PRIVILEGES

    @property
    def available_privileges(self):
        return self._available_privileges

    @property
    def create_sql(self):
        settings_str = settings_str_from(self)
        return f"{self.create_sql_base} " f"{settings_str};"


@dataclass
class Schema:
    database: Database
    name: str
    comment: str
    transient: bool = False
    with_managed_access: bool = False
    data_retention_time_in_days: int = None

    def __post_init__(self):
        self._available_privileges = SCHEMA_PRIVILEGES

    @property
    def available_privileges(self):
        return self._available_privileges

    @property
    def resource_type(self):
        return get_resource_type(self)

    @property
    def fq_name(self):
        return f"{self.database.name}.{self.name}"

    @property
    def describe_sql(self):
        return f"describe {self.resource_type} {self.fq_name};"

    @property
    def drop_sql(self):
        return f"drop {self.resource_type} {self.fq_name};"

    @property
    def create_sql(self):
        transient = "transient " if getattr(self, "transient", None) else ""
        settings_str = settings_str_from(self)
        return (
            f"create {transient}{self.resource_type} {self.fq_name} " f"{settings_str};"
        )


@dataclass
class SchemaObject:
    database: Database
    schema: Schema
    name: str
    comment: str
    or_replace: bool = False
    if_not_exists: bool = False

    def __post_init__(self):
        if self.or_replace and self.if_not_exists:
            raise InvalidParamsException(
                "or_replace and if_not_exists are mutually exclusive, per "
                "https://docs.snowflake.net/manuals/sql-reference/sql/create.html.\n"
                "Please specify one of the other, but not both."
            )

    @property
    def resource_type(self):
        return get_resource_type(self)

    @property
    def fq_name(self):
        return f"{self.schema.fq_name}.{self.name}"

    @property
    def describe_sql(self):
        return f"describe {self.resource_type} {self.fq_name};"

    @property
    def drop_sql(self):
        return f"drop {self.resource_type} {self.fq_name};"

    @property
    def create_sql_base(self):
        return (
            f"create {'or replace ' if self.or_replace else ''}"
            f"{self.resource_type} "
            f"{'if not exists ' if self.if_not_exists else ''}"
            f"{self.fq_name}"
        )


@dataclass
class Column:
    name: str
    data_type: str  # this needs much better support for autoinc, numeric precision/scale, etc columns
    column_default: str = None
    is_nullable: str = None
    comment: str = None
    character_maximum_length: int = None
    character_octet_length: int = None
    datetime_precision: int = None
    numeric_precision: int = None
    numeric_scale: int = None
    interval_type: str = None
    interval_precision: int = None
    is_identity: bool = None
    identity_start: int = None
    identity_increment: int = None
    identity_maximum: int = None
    identity_minimum: int = None
    identity_cycle: int = None

    @property
    def sql(self):
        return f"{self.name} {self.data_type} " f"default {self.column_default}"


@dataclass
class Table(SchemaObject):
    columns: List[Column] = None
    cluster_keys: List[str] = field(default_factory=list)

    @property
    def create_sql(self):
        col_sql = ", ".join([c.sql for c in self.columns])
        cluster_sql = (
            f" cluster by ({','.join(self.cluster_keys)})" if self.cluster_keys else ""
        )
        return (
            f"{self.create_sql_base} "
            f"{col_sql}{cluster_sql} "
            f"comment = '{self.comment}';"
        )


# TO DO: Incorporate TableAsSelect
# @dataclass
# class TableAsSelect(SchemaObject):

# TO DO: Incorporate TableLike
# @dataclass
# class TableLike(SchemaObject):


@dataclass
class View(SchemaObject):
    select_sql: str = None
    copy_grants: bool = False

    @property
    def create_sql(self):
        return (
            f"{self.create_sql_base} "
            f"{'copy grants ' if self.copy_grants else ''}"
            f"comment = '{self.comment}' "
            f"as {self.select_sql};"
        )


@dataclass
class MaterializedView(
    SchemaObject
):  # Materialized views should be able to handle cluster keys
    select_sql: str = None
    cluster_keys: List[str] = field(default_factory=list)

    @property
    def create_sql(self):
        return (
            f"{self.create_sql_base} "
            f"comment = '{self.comment}' "
            f"as {self.select_sql};"
        )


@dataclass
class FileFormatTypeOptions:
    pass


@dataclass
class FileFormat(SchemaObject):
    config: dict = None


@dataclass
class InternalStage(SchemaObject):
    config: dict = None


@dataclass
class ExternalStage(SchemaObject):
    config: dict = None


@dataclass
class Pipe(SchemaObject):
    copy_sql: str = None
    integration: str = None
    auto_ingest: bool = False

    @property
    def create_sql(self):
        integration_str = (
            f"integration = '{self.integration}' " if self.integration else ""
        )
        return (
            f"{self.create_sql_base} "
            f"auto_ingest = {self.auto_ingest} "
            f"{integration_str}"
            f"comment = '{self.comment}' "
            f"as {self.copy_sql};"
        )


@dataclass
class Stream(SchemaObject):
    pass


# TO DO: incorporate function creation (javascript)
# @dataclass
# class Function(SchemaObject):
#     pass


# TO DO: incorporate stored procedure creation (javascript)
# @dataclass
# class Procedure(SchemaObject):
#     pass


@dataclass
class Sequence(SchemaObject):
    start: int = 1
    increment: int = 1

    @property
    def create_sql(self):
        return (
            f"{self.create_sql_base} "
            f"start = {self.start} "
            f"increment = {self.increment} "
            f"comment = '{self.comment}';"
        )
