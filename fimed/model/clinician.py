import uuid
from datetime import datetime
from typing import List
import pandas as pd
import json
import os
from cryptography.fernet import Fernet
import base64

from fimed.logger import logger
from fimed.database import get_connection
from fimed.model.patient import Patient
from fimed.model.user import User
from fimed.model.form import Form, Row
from fimed.config import settings


class Doctor(User):

    def encrypt_data(self, patient_data):
        f = Fernet(settings.KEY)
        for i in patient_data:
            patient_data[i] = f.encrypt(json.dumps(patient_data[i]).encode('utf-8'))
        return patient_data

    def decrypt_data(self, patient_data):
        f = Fernet(settings.KEY)
        for i in patient_data:
            patient_data[i]["value"] = bytes(patient_data[i]["value"].replace("'", '"')[2:-1], 'utf-8')
            patient_data[i]["value"] = f.decrypt(patient_data[i]["value"]).decode('utf-8').replace('"', "")
            print(patient_data[i])
        return patient_data

    def encrypt_csv(self, csv_data, temp_file):
        f = Fernet(settings.KEY)
        csv_data.to_json(temp_file, orient="records", date_format="epoch", double_precision=10,
                         force_ascii=True, date_unit="ms", default_handler=None)

        with open(temp_file) as data_file:
            data = json.load(data_file)
            for d in data:
                for j in d:
                    d[j] = {"value": str(f.encrypt(json.dumps(d[j]).encode('utf-8'))), "type": str(type(d[j]))}

        with open(temp_file, 'w') as outfile:
            json.dump(data, outfile)

    def new_patient(self, patient_data: dict) -> Patient:
        """
        Creates a new patient.
        """

        database = get_connection()
        data_encrypted = self.encrypt_data(patient_data)
        patient = Patient(id=str(uuid.uuid4()), created_at=datetime.now(), clinical_information=data_encrypted)
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
            patient["clinical_information"] = self.decrypt_data(patient["clinical_information"])
            patient_model = Patient(**patient)
            patients_in_db.append(patient_model)

        return patients_in_db

    def search_by_id(self, id_patient: str) -> Patient:
        """
            Search Patients by id
        """
        database = get_connection()
        patients = None
        clinician: dict = database.users.find_one({"username": self.username})
        for patient in clinician["patients"]:
            if patient["id"] == id_patient:
                patient["clinical_information"] = self.decrypt_data(patient["clinical_information"])
                patients = Patient(**patient)
        return patients

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

    def update_patient(self, id_patient: str, patient_data: dict) -> Patient:
        database = get_connection()
        patients = Patient(id=id_patient, clinical_information=patient_data)
        patients.clinical_information = self.encrypt_data(patients.clinical_information)

        database.users.update(
            {
                "username": self.username,
                "patients.id": id_patient
            },
            {
                "$set": {
                    "patients.$.clinical_information": patients.clinical_information
                }
            }
        )

        return patients

    def create_form(self, data_structure: Form) -> Form:
        database = get_connection()

        database.users.update(
            {"username": self.username}, {"$set": {"form_structure": data_structure.dict(exclude_unset=True)}},
            upsert=True,
        )

    def get_data_structure(self) -> list:
        database = get_connection()
        clinician: dict = database.users.find_one({"username": self.username})
        data_structure = []
        if clinician["form_structure"] != {}:
            for structure in clinician["form_structure"]["rows"]:
                # print(structure)
                # row_s = Row(**structure)
                # print(row_s)
                data_structure.append(structure)
        return data_structure

    def create_by_csv(self, file):
        print(file)

    # database = get_connection()
    # col = database.users
    # temp_file = "data/data.json"
    # csv_file = pd.DataFrame(pd.read_csv(file, sep=";", header=0, index_col=False))
    # self.encrypt_csv(csv_file, temp_file)
    #
    # with open(temp_file) as data_file:
    #     data = json.load(data_file)
    #     for d in data:
    #         col.update(
    #             {
    #                 "username": self.username
    #             },
    #             {
    #                 "$push": {
    #                     "patients": {
    #                         "id": str(uuid.uuid4()),
    #                         "clinical_information": d,
    #                         "created_at": datetime.now()
    #                     }
    #                 }
    #             }
    #         )
    # os.remove(temp_file)
