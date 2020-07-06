from datetime import datetime
from typing import Optional

from pydantic import validator, BaseModel


class PatientCreateRequest(BaseModel):
    name: str

    @validator("name")
    def username_alphanumeric(cls, v):
        assert v.isalpha(), "must be alphanumeric"
        return v


<<<<<<< HEAD
class Patient(BaseModel):
    id: str
    name: str
    created_at: Optional[datetime] = None
=======

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PatientModel(BaseModel):
    clinical_information: dict


class Patient:
    disabled: bool = False

    @staticmethod
    def create(patient_data: PatientModel, id_clinician: str):
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
                        "clinical_information": patient_data.clinical_information
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
                                "clinical_information": d
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

        print(clinician)

        for obj in clinician["patients"]:
            if obj["_id"] == id_patient:
                return obj["clinical_information"]

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
                    "patients.$.clinical_information": updated_data
                }
            }
        )
>>>>>>> 94bba846af767aa5e26a1a474e68499bd5d1614d
