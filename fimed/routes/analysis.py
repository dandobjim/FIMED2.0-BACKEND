from typing import List

from fastapi import APIRouter, Depends, HTTPException, FastAPI, UploadFile, File
from pydantic import ValidationError

from fimed.auth import get_current_active_user
from fimed.logger import logger
from fimed.model.clinician import Doctor
from fimed.model.patients import Patients
from fimed.model.user import UserInDB

import numpy as np

router = APIRouter()


@router.post("/upload_minio", name="Insert analysis files into minio", tags=["analysis"])
async def upload_minio(file: UploadFile = File(...), current_doctor: UserInDB = Depends(get_current_active_user)):
    try:
        Doctor(**current_doctor.dict()).upload_file_minio(file)
    except ValidationError as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=f"Patient could not be created")
    except Exception as e:
        logger.exception(e)


@router.post("/create_model", name="Create a new data analysis model", tags=["analysis"])
async def create_model(file: UploadFile = File(...), current_doctor:UserInDB = Depends(get_current_active_user)):
    try:
        Doctor(**current_doctor.dict()).create_model(file)
    except ValidationError as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=f"Model could not be created")
    except Exception as e:
        logger.exception(e)


@router.post("/prediction", name="Execute prediction's algorithm", tags=["analysis"])
async def prediction(file: UploadFile = File(...), current_doctor:UserInDB = Depends(get_current_active_user)) -> List[int]:
    try:
        prediction= Doctor(**current_doctor.dict()).prediction(file)
    except ValidationError as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=f"Alforithm could not be executed")
    except Exception as e:
        logger.exception(e)
    prediction_list: List[int] = prediction.tolist()
    return prediction_list
