from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError

from fimed.auth import get_current_active_user
from fimed.logger import logger
from fimed.model.clinician import Doctor
from fimed.model.patient import Patient
from fimed.model.user import UserInDB


router = APIRouter()


@router.post("/create", name="Create a new form's structure", tags=["form"])
async def create_form(data_structure: dict,
                                     current_doctor: UserInDB = Depends(get_current_active_user)):
    try:
        Doctor(**current_doctor.dict()).create_form(data_structure)
    except ValidationError as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=f"Form Structure could not be created")
    except Exception as e:
        logger.exception(e)

