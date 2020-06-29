from bson import ObjectId

import scripts.bd_connection as mongo
import uuid


if __name__ == "__main__":
    mongoDB = mongo.MongoConecction()

    # mongoDB.crearClinico("Jose", 'Con')
    # mongoDB.validarClinico("ASH", 'Con')
    
    #mongoDB.crearPaciente("5ee89b39b137fff8ad355a8c",{"Nombre": "Antonio", "Edad":22 })
    #mongoDB.crearPacienteCSV("5ee89b39b137fff8ad355a8c","../Data/Base_datos_final_Melanoma.csv", "../Data/Base_datos_final_Melanoma.json")

    # mongoDB.verAllPacientes("5ee89b39b137fff8ad355a8c")
    # mongoDB.verPaciente("5ee89b39b137fff8ad355a8c","3857043aafba11ea9b1c30e37a8119b4")
    #mongoDB.eliminarPaciente("5ee89b39b137fff8ad355a8c", "3857043aafba11ea9b1c30e37a8119b4")
    mongoDB.editarPaciente("5ee89b39b137fff8ad355a8c","3857043bafba11eaa20f30e37a8119b4",{"Sujeto":2, "Num": "2"})