from datetime import timedelta

from fastapi import HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED

from fimed.model.patient import PatientCreateRequest, Patient

router = APIRouter()

@router.post(
    "/create", name="Create patient ", tags=["patient"]
)
async def register_to_system(patient: PatientCreateRequest):
    patient_in_db = Patient.create(patient)
    return user_in_db
