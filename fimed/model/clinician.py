import uuid
from datetime import datetime
from typing import List

import joblib
import pandas as pd
import json
import os
from cryptography.fernet import Fernet

from fimed.logger import logger
from fimed.database import get_connection
from fimed.minio_file import minio_connection
from fimed.model.patients import Patients
from fimed.model.user import User
from fimed.model.form import Form, Row
from fimed.config import settings
from bson.objectid import ObjectId

#Analysis
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, accuracy_score
from joblib import dump, load
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier


class Doctor(User):

    def encrypt_data(self, patient_data, key):
        f = Fernet(key)
        for i in patient_data:

            patient_data[i] = {"value": f.encrypt(json.dumps(patient_data[i]["value"]).encode('utf-8')),
                               "type": str(type(i))}
        return patient_data

    def encrypt_csv(self, csv_data, temp_file, key):
        f = Fernet(key)
        csv_data.to_json(temp_file, orient="records", date_format="epoch", double_precision=10,
                         force_ascii=True, date_unit="ms", default_handler=None)
        with open(temp_file) as data_file:
            data = json.load(data_file)
            for d in data:
                for j in d:
                    d[j] = {"value": str(f.encrypt(json.dumps(d[j]).encode('utf-8'))), "type": str(type(d[j]))}
        with open(temp_file, 'w') as outfile:
            json.dump(data, outfile)

    def decrypt_data(self, patient_data, key):
        f = Fernet(key)
        for i in patient_data:
            patient_data[i]["value"] = f.decrypt(patient_data[i]["value"]).decode('utf-8').strip('"')
        return patient_data

    def decrypt_csv(self, patient_data, key):
        f = Fernet(key)
        for i in patient_data:
            patient_data[i]["value"] = bytes(patient_data[i]["value"].strip("b'"), 'utf-8')
            patient_data[i]["value"] = f.decrypt(patient_data[i]["value"]).decode('utf-8').strip('"')
        return patient_data

    def new_patient(self, patient_data: dict, user) -> Patients:
        """
        Creates a new patient.
        """
        database = get_connection()
        user_id = database.users.find_one({"username": user["username"]})
        key = user_id["encryption_key"]

        data_encrypted = self.encrypt_data(patient_data, key)
        secondary_id = str(uuid.uuid4())
        database.patients.insert(
            {
                "user_id": user_id["_id"],
                "id_secondary": secondary_id,
                "clinical_information": data_encrypted
            }
        )
        database.users.update(
            {"username": self.username}, {"$push": {"patients": secondary_id}}, upsert=True,
        )


    def all_patients(self) -> List[Patients]:
        """
        Search patients by username.
        """
        database = get_connection()
        clinician: dict = database.users.find_one({"username": self.username})
        clinician_id = clinician["_id"]
        key = clinician["encryption_key"]
        patients_in_db = []
        for patient in database.patients.find({"user_id": clinician_id}):
            try:
                patient["clinical_information"] = self.decrypt_data(patient["clinical_information"],key)
            except:
                patient["clinical_information"] = self.decrypt_csv(patient["clinical_information"],key)
            patient_model = Patients(**patient)
            patients_in_db.append(patient_model)
        return patients_in_db

    def search_by_id(self, id_patient) -> Patients:
        """
            Search Patients by id
        """
        database = get_connection()
        user_id = database.users.find_one({"username": self.username})
        key = user_id["encryption_key"]
        patient = database.patients.find_one({"id_secondary": id_patient})
        try:
            patient["clinical_information"] = self.decrypt_data(patient["clinical_information"], key)
        except:
            patient["clinical_information"] = self.decrypt_csv(patient["clinical_information"], key)
        patients = Patients(**patient)
        return patients

    def delete(self, id_patient: str):
        """
            Delete patients by id
        """
        database = get_connection()
        database.patients.delete_one({"id_secondary": id_patient})
        database.users.update(
            {
                "username": self.username
            },
            {
                "$pull": {
                    "patients": id_patient
                }
            }
        )

    def update_patient(self, id_patient: str, patient_data: dict) -> Patients:
        database = get_connection()
        patients = Patients(id_secondary=id_patient, clinical_information=patient_data)
        user_id = database.users.find_one({"username": self.username})
        key = user_id["encryption_key"]
        patients.clinical_information = self.encrypt_data(patients.clinical_information, key)
        database.patients.update(
            {
                "id_secondary": id_patient
            },
            {
                "$set": {
                    "clinical_information": patients.clinical_information
                }
            }
        )

        return patients

    def create_form(self, data_structure: Form) -> Form:
        database = get_connection()

        database.users.update(
            {"username": self.username}, {"$set": {"general_form": data_structure.dict(exclude_unset=True)}},
            upsert=True,
        )

    def create_form_by_csv(self, file):
        database = get_connection()
        cols = []
        for col in file.columns.values:
            cols.append({"name": col, "rtype": "<class " + str(file.dtypes[col]) + ">"})

        form_structure = {"rows": cols}

        database.users.update(
            {"username": self.username}, {"$set": {"general_form": form_structure}},
            upsert=True,
        )

    def get_data_structure(self) -> list:
        database = get_connection()
        clinician: dict = database.users.find_one({"username": self.username})
        data_structure = []
        if clinician["general_form"] != {}:
            for structure in clinician["general_form"]["rows"]:
                # row_s = Row(**structure)
                data_structure.append(structure)
        return data_structure

    def create_by_csv(self, file):
        database = get_connection()
        col = database.users
        user_data = col.find_one({"username": self.username})
        secondary_id = str(uuid.uuid4())

        temp_file = "data/data.json"
        csv_file = pd.DataFrame(pd.read_csv(file.file, sep=";", header=0, index_col=False))
        self.create_form_by_csv(csv_file)
        self.encrypt_csv(csv_file, temp_file, user_data["encryption_key"])

        with open(temp_file) as data_file:
            data = json.load(data_file)
            for d in data:
                database.patients.insert(
                    {
                        "user_id": user_data["_id"],
                        "id_secondary": secondary_id,
                        "clinical_information": d,
                        "created_at": datetime.now()
                    }
                )
                database.users.update(
                    {"username": self.username}, {"$push": {"patients": secondary_id}}, upsert=True,
                )
        os.remove(temp_file)

    def upload_file_minio(self,file):
        database = get_connection()
        col = database.users
        user_data = col.find_one({"username": self.username})
        minio = minio_connection()
        found = minio.bucket_exists(str(user_data["_id"]))
        if not found:
            minio.make_bucket(str(user_data["_id"]))
        else:
            print("Bucket 'asiatrip' already exists")

        result = minio.put_object(
            str(user_data["_id"]),str(user_data["_id"])+"_anlaysis", file.file, length=-1, part_size=10 * 1024 * 1024,
        )
        print(
            "created {0} object; etag: {1}, version-id: {2}".format(
                result.object_name, result.etag, result.version_id,
            ),
        )

    def create_model(self,file):
        data = pd.read_csv(file.file, sep=";")
        print(data.shape)
        ncolumns = data.columns.size
        X = data.iloc[:, 0:ncolumns - 1].values
        Y = data.iloc[:, ncolumns - 1].values
        labelencoder_Y = LabelEncoder()
        Y = labelencoder_Y.fit_transform(Y)
        sc = StandardScaler()
        X = sc.fit_transform(X)
        classifier = RandomForestClassifier(n_estimators=10, criterion='entropy', random_state=0)
        classifier.fit(X, Y)
        dump(classifier, 'randomForest.joblib')
        #database
        database = get_connection()
        col = database.users
        user_data = col.find_one({"username": self.username})
        #minio
        minio = minio_connection()
        found = minio.bucket_exists(str(user_data["_id"]))
        if not found:
            minio.make_bucket(str(user_data["_id"]))
        else:
            print("Bucket 'asiatrip' already exists")

        with open('randomForest.joblib', 'rb') as file_data:
            result = minio.put_object(str(user_data["_id"]), 'model', file_data,
                                   length=-1, part_size=10 * 1024 * 1024)
        print(
            "created {0} object; etag: {1}, version-id: {2}".format(
                result.object_name, result.etag, result.version_id,
            ),
        )
        os.remove('randomForest.joblib')

    def prediction(self, file):
        #Minio
        database = get_connection()
        col = database.users
        user_data = col.find_one({"username": self.username})
        minio = minio_connection()
        minio.fget_object(str(user_data["_id"]), "model", "model.joblib")
        filename = 'model.joblib'
        loaded_model = joblib.load(filename)
        #Read data
        data = pd.read_csv(file.file, sep=";")
        sc = StandardScaler()
        X = sc.fit_transform(data)
        pred = loaded_model.predict(X)
        os.remove('model.joblib')
        return pred