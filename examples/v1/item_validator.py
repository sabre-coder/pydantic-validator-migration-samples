"""Original free sample: validate and normalize each string after type validation."""
from pydantic import BaseModel, validator


class LabelSet(BaseModel):
    labels: list[str]

    @validator("labels", each_item=True)
    def clean_label(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("label must contain visible text")
        return cleaned
