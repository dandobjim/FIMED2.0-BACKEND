from passlib.context import CryptContext
from pydantic import BaseModel, validator

from fimed.database import get_connection


# security


class Token(BaseModel):
    access_token: str
    token_type: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# patients


class PatientBase(BaseModel):
    fullname: str
    age: int
    email: str = None

class PatientCreateRequest(PatientBase):

    @validator("fullname")
    def name_must_contain_spaces(cls, v):
         if ' ' not in v:
            raise ValueError('fullname must contain a space between name and surname')
        return v.title()

    @validator("age")
    def age_must_be_numeric(cls,v):
        if type(v) != int:
            raise ValueError('age must be numeric')

    @validator("email")
    def email_is_valid(cls, v):
        assert "@" in v, "email is not valid"
        return v


class Patient(PatientBase):
    disabled: bool = False

    @staticmethod
    def create(fullname: str, age:int, email:str, id_clinico:str):
        """
        Create a new patient.
        """
        database = get_connection()
        db = mongo_client.FIMED
        col = db.Clinicians

        objeto = col.find_one({
            "_id": ObjectId(id_clinico)
        })
        col.update(
            {
                "_id": ObjectId(id_clinico)
            },
            {
                "$push": {
                    "pacientes": {
                        "_id": uuid.uuid1().hex,
                        "data": datos_paciente
                    }
                }
            }
        )
    
    @staticmethod
    def create_by_csv(id_clinico:str, file, tempfile):
        """
            Create patients usign csv file
        """

        database = get_connection()
        db = mongo_client.FIMED
        col = db.Clinicians

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
                            "pacientes": {
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
        db = mongo_client.FIMED
        col = db.Clinicians
        
        objeto = col.find_one({
            "_id": ObjectId(id_clinico)
        })
        for obj in objeto["pacientes"]:
            return (obj["data"])
    
    @staticmethod
    def search_by_id(id_clinico, id_paciente):
        """
            Search Patients by id
        """
        database = get_connection()
        db = mongo_client.FIMED
        col = db.Clinicians

        objeto = col.find_one({
            "_id": ObjectId(id_clinico)
        })

        for obj in objeto["pacientes"]:
            if (obj["_id"] == id_paciente):
                return obj["data"]
        print("No existe paciente")

    @staticmethod
    def delete(id_clinico, id_paciente):
        """
            Delete patients by id
        """
        database = get_connection()
        db = mongo_client.FIMED
        col = db.Clinicians

        objeto = col.find_one({
            "_id": ObjectId(id_clinico)
        })
        col.update(
            {
                "_id": ObjectId(id_clinico)
            },
            {
                "$pull": {
                    "pacientes": {
                        "_id": id_paciente
                    }
                }
            }
        )
    
    @staticmethod
    def update(id_clinico, id_paciente, updated_data):

        database = get_connection()
        db = mongo_client.FIMED
        col = db.Clinicians

        col.update(
            {
                "_id": ObjectId(id_clinico),
                "pacientes._id": id_paciente
            },
            {
                "$set": {
                    "pacientes.$.data": updated_data
                }
            }
        )