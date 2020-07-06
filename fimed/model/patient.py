from datetime import datetime
from typing import Optional

from pydantic import validator, BaseModel


class PatientCreateRequest(BaseModel):
    name: str

    @validator("name")
    def username_alphanumeric(cls, v):
        assert v.isalpha(), "must be alphanumeric"
        return v


class Patient(BaseModel):
    id: str
    clinical_information: dict
    created_at: Optional[datetime] = None
