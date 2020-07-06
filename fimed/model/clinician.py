import uuid
from datetime import datetime
from typing import List

from bson import ObjectId

from fimed.database import get_connection
from fimed.model.patient import Patient
from fimed.model.user import User


class Doctor(User):
    def new_patient(self, patient_data: dict) -> Patient:
        """
        Creates a new patient.
        """
        patient = Patient(id=str(uuid.uuid4()), created_at=datetime.now(), **patient_data)

        database = get_connection()
        database.assingments.update(
            {"clinician": self.username}, {"$push": {"patients": patient.dict(exclude_unset=True)}}, upsert=True,
        )

        return patient

    def all_patients(self) -> List[Patient]:
        """
        Search patients by id.
        """
        database = get_connection()
        assignments: dict = database.assingments.find_one({"clinician": self.username})

        patients_in_db = []

        for patient in assignments["patients"]:
            patient_model = Patient(**patient)
            patients_in_db.append(patient_model)

        return patients_in_db
