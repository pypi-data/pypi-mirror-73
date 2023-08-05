from dataclasses import dataclass
from snowday.util import get_resource_type, settings_str_from


@dataclass
class BaseSnowflakeObject:

    name: str

    @property
    def _settings_str(self):
        return settings_str_from(self)

    @property
    def fq_name(self):
        return self.name

    @property
    def resource_type(self):
        return get_resource_type(self)

    @property
    def describe(self):
        return f"describe {self.resource_type} {self.fq_name};"

    @property
    def drop(self):
        return f"drop {self.resource_type} {self.fq_name};"

    @property
    def create(self):
        return (
            f"create {self.resource_type} " f"{self.fq_name} " f"{self._settings_str};"
        )

    @property
    def create_if_not_exists(self):
        return (
            f"create {self.resource_type} if not exists "
            f"{self.fq_name} "
            f"{self._settings_str};"
        )

    @property
    def create_or_replace(self):
        return (
            f"create or replace {self.resource_type} "
            f"{self.fq_name} "
            f"{self._settings_str};"
        )
