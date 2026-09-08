"""Original free sample: V1 wraps both deliberate and accidental TypeError."""
from pydantic import BaseModel, validator


class WorkItem(BaseModel):
    priority: int

    @validator("priority")
    def check_priority(cls, value: int) -> int:
        if not 0 <= value <= 10:
            # Legacy deliberate input rejection, not an accidental coding error.
            raise TypeError("priority must be between 0 and 10")
        return value


class ProgrammingErrorExample(BaseModel):
    """Intentionally defective: demonstrates exception handling, not a migration target."""
    count: int

    @validator("count")
    def buggy_length(cls, value: int) -> int:
        return len(value)  # Deliberate programming bug: integers have no length.
