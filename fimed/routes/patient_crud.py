from datetime import timedelta

from fastapi import HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED

from fimed.model.patient import Patient, PatientModel
router = APIRouter()


@router.post(
    "/create", name="Create patient ", tags=["patient"]
)
async def register_patient(clinical_information: PatientModel, clinic_id: str):
    patient_in_db = Patient.create(clinical_information, clinic_id)
    return patient_in_db


@router.post(
    "/csv", name = "Insert patient by csv file", tags=["patient"]
)
async def register_patient_using_csv(clinic_id: str, file_path: str, temp_file_path: str):
    csv_patients = Patient.create_by_csv(clinic_id, file_path, temp_file_path)
    return  csv_patients


@router.get(
    "/see_all_patients", name="See all patients by clinic id", tags=["patient"]
)
async def see_all_patients(clinic_id:str):
    patients = Patient.see_all_by_clinic_id(clinic_id)
    return patients


@router.get(
    "/search_by_patient_id", name="Search patient by patient's id", tags=["patient"]
)
async def see_patient(clinic_id:str, patient_id:str):
    patient = Patient.search_by_id(clinic_id,patient_id)
    return patient


@router.post(
    "/delete", name="Delete patient by patient_id and clinic_id", tags=["patient"]
)
async def delete_patient(clinic_id: str, patient_id: str):
    patient_deleted = Patient.delete(clinic_id, patient_id)
    return patient_deleted


@router.post(
    "/update", name="Update patient", tags=["patient"]
)
def update_patient(clinic_id: str, patient_id: str, new_data: dict):
    patient_updated = Patient.update(clinic_id, patient_id, new_data)
    return patient_updated

