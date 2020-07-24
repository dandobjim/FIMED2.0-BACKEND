from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError

from fimed.auth import get_current_active_user
from fimed.logger import logger
from fimed.model.clinician import Doctor
from fimed.model.patient import Patient
from fimed.model.user import UserInDB

from fimed.model.form import Form


router = APIRouter()


@router.post("/create", name="Create a new form's structure", tags=["form"])
async def create_form(form: Form,
                    current_doctor: UserInDB = Depends(get_current_active_user)):
    try:
        Doctor(**current_doctor.dict()).create_form(form)
    except ValidationError as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=f"Form Structure could not be created")
    except Exception as e:
        logger.exception(e)


@router.get("/see_form", name="See form's structure", tags=["form"])
async def see_form(current_doctor: UserInDB = Depends(get_current_active_user)):
    form = None
    try:
        form = Doctor(**current_doctor.dict()).get_data_structure()
    except ValidationError as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=f"Form Structure doesn`t exist")
    except Exception as e:
        logger.exception(e)

    return form
