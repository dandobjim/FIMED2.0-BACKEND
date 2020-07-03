from passlib.context import CryptContext
from pydantic import BaseModel, validator
from bson.objectid import ObjectId
import uuid
import pandas as pd
import json
import os

from fimed.database import get_connection


# security


class Token(BaseModel):
    access_token: str
    token_type: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# patients

class Patient:
    disabled: bool = False

    @staticmethod
    def create(patient_data: dict, id_clinician: str):
        """
        Create a new patient.
        """
        database = get_connection()
        col = database.users

        col.update(
            {
                "_id": ObjectId(id_clinician)
            },
            {
                "$push": {
                    "patients": {
                        "_id": uuid.uuid1().hex,
                        "data": patient_data
                    }
                }
            }
        )

    @staticmethod
    def create_by_csv(id_clinician: str, file, temp_file):
        """
            Create patients usign csv file
        """

        database = get_connection()
        col = database.users

        csv_file = pd.DataFrame(pd.read_csv(file, sep=";", header=0, index_col=False))
        csv_file.to_json(temp_file, orient="records", date_format="epoch", double_precision=10,
                         force_ascii=True, date_unit="ms", default_handler=None)

        with open(temp_file) as data_file:
            data = json.load(data_file)
            for d in data:
                col.update(
                    {
                        "_id": ObjectId(id_clinician)
                    },
                    {
                        "$push": {
                            "patients": {
                                "_id": uuid.uuid1().hex,
                                "data": d
                            }
                        }
                    }
                )
        os.remove(temp_file)

    @staticmethod
    def see_all_by_clinic_id(id_clinician):
        """
            See all patients by clinic id.
        """

        database = get_connection()
        col = database.users

        clinician = col.find_one({
            "_id": ObjectId(id_clinician)
        })
        return clinician["patients"]

    @staticmethod
    def search_by_id(id_clinician, id_patient):
        """
            Search Patients by id
        """
        database = get_connection()
        col = database.users

        clinician = col.find_one({
            "_id": ObjectId(id_clinician)
        })

        for obj in clinician["patients"]:
            if obj["_id"] == id_patient:
                return obj["data"]

    @staticmethod
    def delete(id_clinician, id_patient):
        """
            Delete patients by id
        """
        database = get_connection()
        col = database.users

        col.update(
            {
                "_id": ObjectId(id_clinician)
            },
            {
                "$pull": {
                    "patients": {
                        "_id": id_patient
                    }
                }
            }
        )

    @staticmethod
    def update(id_clinician, id_patient, updated_data):

        database = get_connection()
        col = database.users

        col.update(
            {
                "_id": ObjectId(id_clinician),
                "patients._id": id_patient
            },
            {
                "$set": {
                    "patients.$.data": updated_data
                }
            }
        )
