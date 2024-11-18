from sqlalchemy import types, DateTime
from datetime import timezone


# method to save all datetimes in UTC, and return them in UTC
class UTCDateTime(types.TypeDecorator):
    impl = DateTime
    # to ensure datetime inserted includes time zone info
    def process_bind_param(self, value, dialect):
        if value is not None:
            if not value.tzinfo:
                raise TypeError("tzinfo is required")
            value = value.astimezone(timezone.utc).replace(tzinfo=None)
        return value
    # to return datetime info ending in Z indicating UTC
    def process_result_value(self, value, dialect):
        if value is not None:
            value = f"{value}Z"
        return value