from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError


from fimed.auth import get_current_active_user
from fimed.logger import logger
from fimed.model.clinician import Doctor
from fimed.model.patient import Patient
from fimed.model.user import UserInDB

router = APIRouter()


@router.post("/create", name="Create patient and assign to self", tags=["patient"])
async def register(patient: dict, current_doctor: UserInDB = Depends(get_current_active_user)) -> Patient:
    try:
        patient = Doctor(**current_doctor.dict()).new_patient(patient)
        logger.debug(patient)
    except ValidationError as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=f"Patient could not be created")
    except Exception as e:
        logger.exception(e)

    return patient


@router.post("/create_by_csv", name="Insert patient by csv file", tags=["patient"])
async def register_patient_using_csv(file_path: str, temp_file_path: str,
                                     current_doctor: UserInDB = Depends(get_current_active_user)):
    try:
        Doctor(**current_doctor.dict()).create_by_csv(file_path, temp_file_path)
    except ValidationError as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=f"Patient could not be created")
    except Exception as e:
        logger.exception(e)


@router.get("/all", name="Get patients of current clinician", tags=["patient"])
async def patients(current_doctor: UserInDB = Depends(get_current_active_user)) -> List[Patient]:
    # print("Devuelvo todos los pacientes")
    patients = []
    try:
        patients = Doctor(**current_doctor.dict()).all_patients()

    except Exception as e:
        logger.exception(e)

    # if not patients:
        # raise HTTPException(status_code=404, detail=f"No patients found for current user")

    return patients


@router.get("/search_by_patient_id", name="Get patient of current clinician by id patient", tags=["patient"])
async def patients(id_patient: str, current_doctor: UserInDB = Depends(get_current_active_user)) :
    patient = None
    # print(id_patient)
    try:
        patient = Doctor(**current_doctor.dict()).search_by_id(id_patient)
    except Exception as e:
        logger.exception(e)

    if not patient:
        raise HTTPException(status_code=404, detail=f"No patients found for current user")

    return patient.clinical_information


@router.delete(
    "/delete/{id_patient}", name="Delete patient by patient_id and clinic_id", tags=["patient"]
)
async def delete_patient(id_patient:str, current_doctor: UserInDB = Depends(get_current_active_user)):
    print(id_patient)
    try:
        patient = Doctor(**current_doctor.dict()).delete(id_patient)
        logger.debug(patient)
    except ValidationError as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=f"Patient could not be deleted")
    except Exception as e:
        logger.exception(e)


@router.post(
    "/update/{id_patient}", name="Update patient", tags=["patient"]
)
def update_patient(id_patient: str, patient: dict, current_doctor: UserInDB = Depends(get_current_active_user)) -> Patient:
    try:
        patient = Doctor(**current_doctor.dict()).update_patient(id_patient, patient)
        logger.debug(patient)
    except ValidationError as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=f"Patient could not be updated")
    except Exception as e:
        logger.exception(e)

    return patient

