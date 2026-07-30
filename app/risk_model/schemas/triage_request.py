from pydantic import BaseModel


class TriageRequest(BaseModel):
    patient_text: str