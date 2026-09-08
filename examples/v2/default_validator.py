"""Original free sample: validate the explicit default before field type validation."""
from pydantic import BaseModel, Field, field_validator


class Profile(BaseModel):
    display_name: str = Field(default=" guest ", validate_default=True)

    @field_validator("display_name", mode="before")
    @classmethod
    def normalize_name(cls, value):
        if value is None:
            return "anonymous"
        if isinstance(value, str):
            return value.strip() or "anonymous"
        return value
