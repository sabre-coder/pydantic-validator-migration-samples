"""Original free sample: reject invalid input while leaving programming errors visible."""
from pydantic import BaseModel, field_validator


class WorkItem(BaseModel):
    priority: int

    @field_validator("priority")
    @classmethod
    def check_priority(cls, value: int) -> int:
        if not 0 <= value <= 10:
            raise ValueError("priority must be between 0 and 10")
        return value


class ProgrammingErrorExample(BaseModel):
    """Intentionally defective: V2 should expose this bug as TypeError."""
    count: int

    @field_validator("count")
    @classmethod
    def buggy_length(cls, value: int) -> int:
        return len(value)  # Do not hide this bug with a broad TypeError handler.
