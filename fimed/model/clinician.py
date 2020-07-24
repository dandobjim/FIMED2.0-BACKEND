import uuid
from datetime import datetime
from typing import List
import pandas as pd
import json
import os

from fimed.database import get_connection
from fimed.model.patient import Patient
from fimed.model.user import User
from fimed.model.form import Form


class Doctor(User):

    def new_patient(self, patient_data: dict) -> Patient:
        """
        Creates a new patient.
        """
        patient = Patient(id=str(uuid.uuid4()), created_at=datetime.now(), clinical_information=patient_data)

        database = get_connection()
        database.users.update(
            {"username": self.username}, {"$push": {"patients": patient.dict(exclude_unset=True)}}, upsert=True,
        )

        return patient

    def all_patients(self) -> List[Patient]:
        """
        Search patients by username.
        """
        database = get_connection()
        clinician: dict = database.users.find_one({"username": self.username})
        patients_in_db = []

        for patient in clinician["patients"]:
            patient_model = Patient(**patient)
            patients_in_db.append(patient_model)

        return patients_in_db

    def search_by_id(self, id_patient: str) -> Patient:
        """
            Search Patients by id
        """
        database = get_connection()
        patient = None

        clinician: dict = database.users.find_one({"username": self.username})
        print(clinician)

        for patient in clinician["patients"]:
            if patient["id"] == id_patient:
                patient = Patient(**patient)
                print(patient.clinical_information)

        return patient

    def create_by_csv(self, file, temp_file):
        """
            Create patients using csv file
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
                        "username": self.username
                    },
                    {
                        "$push": {
                            "patients": {
                                "id": str(uuid.uuid4()),
                                "clinical_information": d,
                                "created_at": datetime.now()
                            }
                        }
                    }
                )
        os.remove(temp_file)

    def delete(self, id_patient: str):
        """
            Delete patients by id
        """
        database = get_connection()
        col = database.users

        col.update(
            {
                "username": self.username
            },
            {
                "$pull": {
                    "patients": {
                        "id": id_patient
                    }
                }
            }
        )

    def update_patient(self, id_patient:str, patient_data:dict) -> Patient:

        database = get_connection()

        patient = Patient(id=id_patient, clinical_information=patient_data)

        database.users.update(
            {
                "username": self.username,
                "patients.id": id_patient
            },
            {
                "$set": {
                    "patients.$.clinical_information": patient.clinical_information
                }
            }
        )

        return patient

    def create_form(self, data_structure:Form) -> Form:
        database = get_connection()

        database.users.update(
            {"username": self.username}, {"$push": {"form_structure": data_structure.dict(exclude_unset=True)}}, upsert=True,
        )

    def get_data_structure(self) -> Form:
        database = get_connection()
        clinician: dict = database.users.find_one({"username": self.username})
        data_structure = {}

        for structure in clinician["form_structure"]:
            data_structure = Form(**structure)
            # print(data_structure)
        return data_structure

