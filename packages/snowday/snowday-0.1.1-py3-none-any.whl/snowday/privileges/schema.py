from snowday.privileges.common import (
    ALL,
    MODIFY,
    OWNERSHIP,
    USAGE,
)


CREATE_TABLE = "create table"
CREATE_EXTERNAL_TABLE = "create external table"
CREATE_VIEW = "create view"
CREATE_STAGE = "create stage"
CREATE_FILE_FORMAT = "create file format"
CREATE_SEQUENCE = "create sequence"
CREATE_FUNCTION = "create function"
CREATE_PIPE = "create pipe"
CREATE_STREAM = "create stream"
CREATE_TASK = "create task"
CREATE_PROCEDURE = "create procedure"


SCHEMA_PRIVILEGES = [
    ALL,
    CREATE_TABLE,
    CREATE_EXTERNAL_TABLE,
    CREATE_VIEW,
    CREATE_STAGE,
    CREATE_FILE_FORMAT,
    CREATE_SEQUENCE,
    CREATE_FUNCTION,
    CREATE_PIPE,
    CREATE_STREAM,
    CREATE_TASK,
    CREATE_PROCEDURE,
    MODIFY,
    OWNERSHIP,
    USAGE,
]
