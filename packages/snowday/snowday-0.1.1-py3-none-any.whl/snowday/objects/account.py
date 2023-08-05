from dataclasses import dataclass, field
from typing import List

from snowday.objects.base import BaseSnowflakeObject
from snowday.privileges import (
    ACCOUNT_PRIVILEGES,
    RESOURCE_MONITOR_PRIVILEGES,
    WAREHOUSE_PRIVILEGES,
)
from snowday.exceptions import (
    InvalidParamsException,
    InvalidWhitespaceException,
    UnsupportedFeatureException,
)


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
class AccountObject(BaseSnowflakeObject):
    def __post_init__(self):
        self._available_privileges = []
        if " " in self.name:
            raise InvalidWhitespaceException(
                f"Invalid whitespace in name: {self.name}\n\nPlease make it {self.name.replace(' ', '')} instead."
            )

    @property
    def available_privileges(self):
        return self._available_privileges


@dataclass
class AwsApiIntegration(AccountObject):
    api_aws_role_arn: str = ""  # Figure out a cleaner way to do this
    api_provider: str = "aws_api_gateway"
    api_allowed_prefixes: List[str] = field(default_factory=list)
    api_blocked_prefixes: List[str] = field(default_factory=list)
    comment: str = ""
    enabled: bool = True  # enabled by default

    @property
    def resource_type(self):
        return "api integration"


@dataclass
class NetworkPolicy(AccountObject):
    allowed_ips: List[str] = field(default_factory=list)
    blocked_ips: List[str] = field(default_factory=list)
    comment: str = ""


@dataclass
class ResourceMonitorTrigger:
    on_percent: int
    do: str

    @property
    def sql(self):
        return f"on {self.on_percent} do {self.do}"


@dataclass
class ResourceMonitor(AccountObject):
    triggers: List[ResourceMonitorTrigger]
    credit_quota: int = 1
    frequency: str = "never"  # Off by default -> restrict this to available freqs
    start_timestamp: str = "immediately"  # Use strings because.... timestamp | "IMMEDIATELY"
    end_timestamp: str = None  # String whyyy

    def __post_init__(self):
        self._available_privileges = RESOURCE_MONITOR_PRIVILEGES

    @property
    def _settings_str(self):
        return (
            f"with credit quota={self.credit_quota} "
            f"frequency={self.frequency} "
            f"start_timestamp={self.start_timestamp} "
            f"triggers ({self._format_triggers()})"
        )

    @property
    def available_privileges(self):
        return self._available_privileges

    def _format_triggers(self):
        return " ".join([trigger.sql for trigger in self.triggers])

    @property
    def create_if_not_exists(self):
        raise UnsupportedFeatureException(
            "Create if not exists for snowflake resource monitors is unsupported."
        )


@dataclass
class Share(AccountObject):
    comment: str = ""


@dataclass
class Warehouse(AccountObject):
    warehouse_size: str = "xsmall"  # enum this
    min_cluster_count: int = 1
    max_cluster_count: int = 1
    scaling_policy: str = None  # enum this
    auto_suspend: int = 60
    auto_resume: bool = True
    initially_suspended: bool = True
    max_concurrency_level: int = 10
    statement_queued_timeout_in_seconds: int = 600
    statement_timeout_in_seconds: int = 6000
    resource_monitor: ResourceMonitor = None
    comment: str = ""

    def __post_init__(self):
        self._available_privileges = WAREHOUSE_PRIVILEGES

    @property
    def available_privileges(self):
        return self._available_privileges


@dataclass
class Role(AccountObject):
    comment: str = ""


@dataclass
class User(BaseSnowflakeObject):
    email: str = None
    password: str = None
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
    default_warehouse: Warehouse = None
    default_role: Role = None  # only accept a Role object
    default_namespace: str = None
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
    comment: str = ""


@dataclass
class AzureNotificationIntegration(AccountObject):
    azure_storage_queue_primary_uri: str
    azure_tenant_id: str
    enabled: bool = True
    type: str = "queue"
    notification_provider: str = "azure_storage_queue"
    comment: str = ""

    @property
    def resource_type(self):
        return "notification integration"


@dataclass
class SecurityIntegrationOAuth(AccountObject):
    external_oauth_type: str  # okta, azure, ping_federate, custom
    external_oauth_issuer: str
    external_oauth_token_user_mapping_claim: str
    external_oauth_snowflake_user_mapping_attribute: str  # login_name or email
    enabled: bool = True
    external_oauth_jws_keys_url: str = None  # optional
    external_oauth_rsa_public_key: str = None  # optional pk1
    external_oauth_rsa_public_key_2: str = None  # optional pk2
    external_oauth_audience_list: str = None  # optional
    type: str = "external_oauth"

    @property
    def resource_type(self):
        return "security integration"


@dataclass
class SecurityIntegrationOAuthPartnerApp(AccountObject):
    def __post_init__(self):
        raise NotImplementedError(
            "Snowflake Integration for OAuth Partner Apps not implemented. If you'd like to contribute this functionality, it would be wholly welcomed."
        )

    @property
    def resource_type(self):
        return "security integration"


@dataclass
class SecurityIntegrationOAuthCustom(AccountObject):
    def __post_init__(self):
        raise NotImplementedError(
            "Snowflake Integration for custom OAuth not implemented. If you'd like to contribute this functionality, it would be wholly welcomed."
        )

    @property
    def resource_type(self):
        return "security integration"


@dataclass
class SecurityIntegrationSAML2(AccountObject):
    saml2_issuer: str
    saml2_sso_url: str
    saml2_provider: str
    saml2_x509_cert: str
    enabled: bool = True
    saml2_sp_initiated_login_page_label: str = None
    saml2_enable_sp_initiated: str = None
    saml2_snowflake_x509_cert: str = None
    saml2_sign_request: str = None
    saml2_requested_nameid_format: str = None
    type: str = "saml2"

    @property
    def resource_type(self):
        return "security integration"


@dataclass
class SecurityIntegrationSCIM(AccountObject):
    scim_client: str  # okta, azure, or custom
    run_as_role: str  # okta_provisioner, aad_provisioner, generic_scim_provisioner
    network_policy: str = None
    type: str = "saml2"

    @property
    def resource_type(self):
        return "security integration"


@dataclass
class BaseStorageIntegration(AccountObject):

    storage_allowed_locations: List[str]  # required
    storage_blocked_locations: List[str] = default_factory(list)
    comment: str = ""
    enabled: bool = True
    type: str = "external_stage"

    @property
    def resource_type(self):
        return "storage integration"


@dataclass
class StorageIntegrationS3(BaseStorageIntegration):
    storage_aws_role_arn: str
    storage_provider: str = "s3"


@dataclass
class StorageIntegrationGCS(BaseStorageIntegration):
    storage_provider: str = "gcs"


@dataclass
class StorageIntegrationAzure(BaseStorageIntegration):
    azure_tenant_id: str
    storage_provider: str = "azure"
