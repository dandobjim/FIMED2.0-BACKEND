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

class Patient():
    disabled: bool = False

    @staticmethod
    def create(patient_data: dict, id_clinico: str):
        """
        Create a new patient.
        """
        database = get_connection()
        col = database.users

        objeto = col.find_one({
            "_id": ObjectId(id_clinico)
        })
        col.update(
            {
                "_id": ObjectId(id_clinico)
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
    def create_by_csv(id_clinico: str, file, tempfile):
        """
            Create patients usign csv file
        """

        database = get_connection()
        col = database.users

        csv_file = pd.DataFrame(pd.read_csv(file, sep=";", header=0, index_col=False))
        csv_file.to_json(tempfile, orient="records", date_format="epoch", double_precision=10,
                         force_ascii=True, date_unit="ms", default_handler=None)

        with open(tempfile) as data_file:
            data = json.load(data_file)
            for d in data:
                col.update(
                    {
                        "_id": ObjectId(id_clinico)
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
        os.remove(tempfile)

    @staticmethod
    def see_all_by_clinic_id(id_clinico):
        """
            See all patients by clinic id.
        """

        database = get_connection()
        col = database.users

        objeto = col.find_one({
            "_id": ObjectId(id_clinico)
        })
        return objeto["patients"]

    @staticmethod
    def search_by_id(id_clinico, id_paciente):
        """
            Search Patients by id
        """
        database = get_connection()
        col = database.users

        objeto = col.find_one({
            "_id": ObjectId(id_clinico)
        })
        for obj in objeto["patients"]:
            if (obj["_id"] == id_paciente):
               return obj["data"]

    @staticmethod
    def delete(id_clinico, id_paciente):
        """
            Delete patients by id
        """
        database = get_connection()
        col = database.users

        objeto = col.find_one({
            "_id": ObjectId(id_clinico)
        })
        col.update(
            {
                "_id": ObjectId(id_clinico)
            },
            {
                "$pull": {
                    "patients": {
                        "_id": id_paciente
                    }
                }
            }
        )

    @staticmethod
    def update(id_clinico, id_paciente, updated_data):

        database = get_connection()
        col = database.users

        col.update(
            {
                "_id": ObjectId(id_clinico),
                "patients._id": id_paciente
            },
            {
                "$set": {
                    "patients.$.data": updated_data
                }
            }
        )
