from pymongo import MongoClient
from bson.objectid import ObjectId
from passlib.context import CryptContext
import uuid
import pandas as pd
import json
import os


pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000
)


class MongoConecction:

    # Inicializacion de la BD Mongo

    def __init__(self):
        mongo_client = MongoClient(
            "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false")
        db = mongo_client.FIMED
        self.col = db.Clinicians

    # Metodos CRUD

    # Insertar Clinico
    def crearClinico(self, usuario, contraseña):
        if (usuario == '' or contraseña == ''):
            print("Todos los campos son obligatorios")
        else:
            hash_password = pwd_context.encrypt(contraseña)
            self.col.insert_one({
                "usuario": usuario,
                "contraseña": hash_password,
                "pacientes": []
            })

    # Leer clinico y validar si está en la BD

    def validarClinico(self, usuario, contraseña):
        # hash_password = pwd_context.encrypt(contraseña)
        objeto = self.col.find_one({
            "usuario": usuario,

        })
        correcto = False
        if (pwd_context.verify(contraseña, objeto['contraseña'])):
            correcto = True
            id = objeto['_id']
            return ({"correcto": correcto,
                     "id": id})
        else:
            return (print(
                "Usuario o contraseña incorrectos, por favor intentelo de nuevo, si el error persiste contacte con asistencia técnica"))
        correcto = False

    # Crear pacientes
    ## Insertar paciente uno a uno desde html
    def crearPaciente(self, id_clinico, datos_paciente):
        objeto = self.col.find_one({
            "_id": ObjectId(id_clinico)
        })
        self.col.update(
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

    # A traves de fichero CSV
    def crearPacienteCSV(self, id_clinico, file, tempfile):
        csv_file = pd.DataFrame(pd.read_csv(file, sep=";", header=0, index_col=False))
        csv_file.to_json(tempfile, orient="records", date_format="epoch", double_precision=10,
                         force_ascii=True, date_unit="ms", default_handler=None)

        with open(tempfile) as data_file:
            data = json.load(data_file)
            for d in data:
                self.col.update(
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

    # Ver todos los pacientes de un clínico
    def verAllPacientes(self, id_clinico):
        objeto = self.col.find_one({
            "_id": ObjectId(id_clinico)
        })
        for obj in objeto["pacientes"]:
            return (obj["data"])

    # Ver un paciente en concreto buscado por su ID
    def verPaciente(self, id_clinico, id_paciente):
        objeto = self.col.find_one({
            "_id": ObjectId(id_clinico)
        })

        for obj in objeto["pacientes"]:
            if (obj["_id"] == id_paciente):
                return obj["data"]
        print("No existe paciente")

    # Elimina paciente
    def eliminarPaciente(self, id_clinico, id_paciente):
        objeto = self.col.find_one({
            "_id": ObjectId(id_clinico)
        })
        self.col.update(
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

    # Editar paciente
    def editarPaciente(self, id_clinico, id_paciente, updated_data):
        self.col.update(
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
