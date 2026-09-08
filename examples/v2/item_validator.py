"""Original free sample: attach the check to the item, rather than the whole list."""
from typing import Annotated

from pydantic import AfterValidator, BaseModel


def clean_label(value: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError("label must contain visible text")
    return cleaned


CleanLabel = Annotated[str, AfterValidator(clean_label)]


class LabelSet(BaseModel):
    labels: list[CleanLabel]
