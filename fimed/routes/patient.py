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


@router.get("/all", name="Get patients of current clinician", tags=["patient"])
async def patients(current_doctor: UserInDB = Depends(get_current_active_user)) -> List[Patient]:
    patients = []

    try:
        patients = Doctor(**current_doctor.dict()).all_patients()
    except Exception as e:
        logger.exception(e)

    if not patients:
        raise HTTPException(status_code=404, detail=f"No patients found for current user")

    return patients
