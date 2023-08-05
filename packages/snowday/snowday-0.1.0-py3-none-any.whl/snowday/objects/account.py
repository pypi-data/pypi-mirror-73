from dataclasses import dataclass, field
from typing import List

# from snowday.privileges import (
#     ACCOUNT_PRIVILEGES,
#     RESOURCE_MONITOR_PRIVILEGES,
#     WAREHOUSE_PRIVILEGES,
# )
from snowday.exceptions import InvalidParamsException, InvalidWhitespaceException
from snowday.util import get_resource_type, settings_str_from


# https://docs.snowflake.com/en/sql-reference/sql/create.html


@dataclass
class Account:
    name: str

    def __post_init__(self):
        self._available_privileges = ACCOUNT_PRIVILEGES

    @property
    def available_privileges(self):
        return self._available_privileges


@dataclass
class AccountObject:
    name: str
    or_replace: bool = False

    def __post_init__(self):
        self._available_privileges = []
        # Check for name with whitespace, or mutually-exclusive (if not exists + create or replace, etc)
        if self.or_replace and self.if_not_exists:
            raise InvalidParamsException(
                "or_replace and if_not_exists are mutually exclusive per "
                "https://docs.snowflake.net/manuals/sql-reference/sql/create.html.\n\n"
                "Please specify one of the other, but not both."
            )
        if " " in self.name:
            raise InvalidWhitespaceException(
                f"Invalid whitespace in name: {self.name}\n\nPlease make it {self.name.replace(' ', '')} instead."
            )

    @property
    def available_privileges(self):
        return self._available_privileges

    @property
    def resource_type(self):
        return get_resource_type(self)

    @property
    def fq_name(self):
        return self.name

    @property
    def describe(self):
        return f"describe {self.resource_type} {self.fq_name};"

    @property
    def drop(self):
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
class AwsApiIntegration(AccountObject):
    api_aws_role_arn: str = ""  # Figure out a cleaner way to do this
    api_provider: str = "aws_api_gateway"
    enabled: bool = True  # enabled by default
    api_allowed_prefixes: List[str] = field(default_factory=list)
    api_blocked_prefixes: List[str] = field(default_factory=list)
    comment: str = ""
    if_not_exists: bool = False

    @property
    def resource_type(self):
        return "api integration"

    @property
    def create(self):
        settings = settings_str_from(self)
        return (
            f"{self.create_sql_base} "
            f"api_aws_role_arn={self.api_aws_role_arn} "
            f"api_provider={self.api_provider} "
            f""
        )


@dataclass
class NetworkPolicy(AccountObject):
    comment: str = ""
    allowed_ips: List[str] = field(default_factory=list)
    blocked_ips: List[str] = field(default_factory=list)

    @property
    def create_sql(self):
        quoted_allowed_ips = [f"'{ip}'" for ip in self.allowed_ips]
        quoted_blocked_ips = [f"'{ip}'" for ip in self.blocked_ips]
        return (
            f"{self.create_sql_base} "
            f"allowed_ip_list = ({', '.join(quoted_allowed_ips)}) "
            f"blocked_ip_list = ({', '.join(quoted_blocked_ips)}) "
            f"comment = '{self.comment}';"
        )


@dataclass
class ResourceMonitor(AccountObject):
    triggers: List[dict] = field(default_factory=dict)
    credit_quota: int = 1
    frequency: str = "never"  # Off by default -> restrict this to available freqs
    start_timestamp: str = "immediately"

    def __post_init__(self):
        self._available_privileges = RESOURCE_MONITOR_PRIVILEGES

    @property
    def available_privileges(self):
        return self._available_privileges

    def _format_triggers(self):
        triggers_sql_string = " ".join(
            [
                f"on {trigger['on_percent']} percent do {trigger['do']}"
                for trigger in self.triggers
            ]
        )
        return f"triggers {triggers_sql_string}"

    @property
    def create_sql(self):
        triggers = self._format_triggers()
        return (
            f"{self.create_sql_base} with "
            f"credit quota {self.credit_quota} "
            f"frequency {self.frequency} "
            f"start_timestamp {self.start_timestamp} "
            f"{triggers};"
        )


@dataclass
class Share(AccountObject):
    comment: str = ""

    @property
    def create_sql(self):
        settings_str = settings_str_from(self)
        return f"create {self.resource_type} {self.name} {settings_str};"


@dataclass
class Role(AccountObject):
    comment: str = ""
    if_not_exists: bool = False

    @property
    def create_sql(self):
        return f"{self.create_sql_base} " f"comment='{self.comment}';"


@dataclass
class User(AccountObject):
    email: str = None
    password: str = None
    comment: str = ""
    login_name: str = None
    display_name: str = None
    first_name: str = None
    middle_name: str = None
    last_name: str = None
    must_change_password: bool = True
    disabled: bool = False
    snowflake_support: bool = False
    days_to_expiry: int = None
    mins_to_unlock: int = None
    default_warehouse: str = None  # accept either string or Warehouse object
    default_namespace: str = None  # accept either string or Database object
    default_role: str = None  # accept either string or Role object
    # ext_authn_duo: bool = False # NOTE! CANNOT BE SET DIRECTLY
    # ext_authn_uid: str = None # # NOTE! CANNOT BE SET DIRECTLY
    min_to_bypass_mfa: int = None
    disable_mfa: bool = None
    rsa_public_key: str = None
    rsa_public_key_2: str = None
    abort_detached_query: bool = True
    autocommit: bool = False
    date_input_format: str = None
    date_output_format: str = None
    error_on_nondeterministic_merge: bool = None
    error_on_nondeterministic_update: bool = None
    lock_timeout: int = None
    query_tag: str = None
    rows_per_resultset: int = None
    statement_timeout_in_seconds: int = None
    timestamp_day_is_always_24h: bool = None
    timestamp_input_format: str = None
    timestamp_ltz_output_format: str = None
    timestamp_ntz_output_format: str = None
    timestamp_output_format: str = None
    timestamp_type_mapping: str = None
    timestamp_tz_output_format: str = None
    timezone: str = None  # restrict to list of valid timestamps
    time_input_format: str = None
    time_output_format: str = None
    transaction_default_isolation_level: str = None
    two_digit_century_start: int = None
    unsupported_ddl_action: str = None
    use_cached_result: bool = None
    if_not_exists: bool = False

    @property
    def create_sql(self):
        settings_str = settings_str_from(self)
        return f"{self.create_sql_base} " f"{settings_str};"


@dataclass
class Warehouse(AccountObject):
    comment: str = ""
    warehouse_size: str = "xsmall"  # restrict this to list of available sizes
    min_cluster_count: int = 1
    max_cluster_count: int = 1
    scaling_policy: str = None
    auto_suspend: int = 60
    auto_resume: bool = True
    initially_suspended: bool = True
    resource_monitor: str = None  # TODO: INCLUDE THIS FUNCTIONALITY
    max_concurrency_level: int = 10
    statement_queued_timeout_in_seconds: int = 600
    statement_timeout_in_seconds: int = 6000
    if_not_exists: bool = False

    def __post_init__(self):
        self._available_privileges = WAREHOUSE_PRIVILEGES

    @property
    def available_privileges(self):
        return self._available_privileges

    @property
    def create_sql(self):
        settings_str = settings_str_from(self)
        return f"{self.create_sql_base} " f"with {settings_str};"


@dataclass
class AzureNotificationIntegration(AccountObject):
    if_not_exists: bool = False


@dataclass
class SecurityIntegration(AccountObject):
    if_not_exists: bool = False


@dataclass
class StorageIntegration(AccountObject):
    if_not_exists: bool = False
