from dataclasses import dataclass
from typing import List
from re import finditer
from snowday.exceptions import InvalidPrivilegeException
from snowday.objects.global_objects import (
    Database,
    Role,
    ResourceMonitor,
    Schema,
    Warehouse,
)
from snowday.types.schema_objects import Table


IMPORTED_PRIVILEGES = "imported privileges"


def _get_resource_type(instantiated_grant):
    matches = finditer(
        ".+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)",
        instantiated_grant.__class__.__name__,
    )
    case_delineated_words = [m.group(0).lower() for m in matches]
    return " ".join(case_delineated_words[:-1])


def _get_available_privileges(instantiated_grant):
    object_name = instantiated_grant.__class__.__name__.split("Grant")[0]
    return OBJECT_PRIVILEGES[object_name]


@dataclass
class Grant:

    privileges: List[str]
    grantee: Role

    def __post_init__(self):
        for privilege in self.privileges:
            if privilege not in self.available_privileges:
                raise InvalidPrivilegeException(
                    f"'{privilege}' not valid privilege for {self.__class__.__name__}. "
                    f"Privilege choices include: {self.available_privileges}"
                )

    @property
    def available_privileges(self):
        return _get_available_privileges(self)

    @property
    def sql(self):
        privileges_string = ", ".join(self.privileges)
        resource_type = _get_resource_type(self)
        if hasattr(self.subject, "fq_name"):
            subject_name = self.subject.fq_name
        else:
            subject_name = self.subject.name
        if "Global" not in self.__class__.__name__:
            on = f"on {resource_type} {subject_name} "
        return f"grant {privileges_string} " f"{on}" f"to role {self.grantee.name}"


@dataclass
class GlobalGrant(Grant):
    def __post_init__(self):
        raise NotImplementedError


@dataclass
class UserRoleGrant(Grant):
    def __post_init__(self):
        raise NotImplementedError


@dataclass
class ResourceMonitorGrant(Grant):
    resource_monitor: ResourceMonitor

    @property
    def subject(self):
        return self.resource_monitor


@dataclass
class WarehouseGrant(Grant):
    warehouse: Warehouse

    @property
    def subject(self):
        return self.warehouse


@dataclass
class IntegrationPrivilege:
    def __post_init__(self):
        raise NotImplementedError


@dataclass
class DatabaseGrant(Grant):
    database: Database

    @property
    def subject(self):
        return self.database


@dataclass
class SchemaGrant(Grant):
    schema: Schema

    @property
    def subject(self):
        return self.schema


@dataclass
class TableGrant(Grant):
    table: Table

    @property
    def subject(self):
        return self.table


@dataclass
class ExternalTablePrivilege:
    pass


@dataclass
class ViewPrivilege:
    pass


@dataclass
class ExternalStagePrivilege:
    pass


@dataclass
class InternalStagePrivilege:
    pass


@dataclass
class FileFormatPrivilege:
    pass


@dataclass
class PipePrivilege:
    pass


@dataclass
class StreamPrivilege:
    pass


@dataclass
class TaskPrivilege:
    pass


@dataclass
class SequencePrivilege:
    pass


@dataclass
class UDFPrivilege:
    pass
