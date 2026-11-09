from pydantic import BaseModel, Field
import datetime


class ClinicalDataCreate(BaseModel):
    patient_name: str = Field(..., min_length=1)
    age: int = Field(..., ge=0, le=120)
    diagnosis: str = Field(..., min_length=1)

    # Three additional patient fields
    patient_id: str = Field(..., min_length=1)
    blood_type: str = Field(..., min_length=1)
    treatment: str = Field(..., min_length=1)


class ClinicalDataRead(ClinicalDataCreate):
    id: int
    recorded_at: datetime.datetime
