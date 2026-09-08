"""Original free sample: omitted, None and empty-string inputs have distinct cases."""
from pydantic import BaseModel, validator


class Profile(BaseModel):
    display_name: str = " guest "

    @validator("display_name", pre=True, always=True)
    def normalize_name(cls, value):
        if value is None:
            return "anonymous"
        if isinstance(value, str):
            return value.strip() or "anonymous"
        return value
