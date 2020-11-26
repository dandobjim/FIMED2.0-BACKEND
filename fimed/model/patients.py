import uuid
from datetime import datetime
from typing import Optional, List

from pydantic import validator, BaseModel
from fimed.database import get_connection


class PatientCreateRequest(BaseModel):
    name: str


    @validator("name")
    def username_alphanumeric(cls, v):
        assert v.isalpha(), "must be alphanumeric"
        return v


class Patients(BaseModel):
    id_secondary:str
    clinical_information: dict
    sex: bool = None
    @staticmethod
    def save(patients: PatientCreateRequest):
        """
        Saves user to database.
        """
        patients_dict = patients.dict()
        patients_dict["samples"] = []
        database = get_connection()
        database.patients.insert_one(patients_dict)

        return patients_dict
