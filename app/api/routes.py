import logging

from fastapi import APIRouter

from app.schemas.patient import Patient
from app.schemas.triage_request import TriageRequest

from app.services.triage_service import (
    run_triage,
    run_text_triage,
)

# -----------------------------------------
# Logger
# -----------------------------------------
logger = logging.getLogger(__name__)

router = APIRouter()


# -------------------------------------------------------
# Health Check
# -------------------------------------------------------
@router.get("/health")
def health():
    """
    Health check endpoint.
    """

    logger.info("Health check requested.")

    return {
        "status": "healthy",
        "service": "AI-Powered Patient Triage & Risk Assessment Assistant"
    }


# -------------------------------------------------------
# Structured Prediction Endpoint
# -------------------------------------------------------
@router.post("/predict")
def predict_patient(patient: Patient):
    """
    Predict urgency from structured patient data.

    Pipeline:
    Structured Features
        ↓
    Random Forest
        ↓
    Guardrail Override
        ↓
    Urgency Prediction
    """

    logger.info("Received request at /predict endpoint.")

    try:

        result = run_triage(patient.model_dump())

        logger.info("/predict completed successfully.")

        return result

    except Exception:

        logger.exception("Error while processing /predict request.")

        raise


# -------------------------------------------------------
# AI Intake Endpoint
# -------------------------------------------------------
@router.post("/intake")
def intake_patient(request: TriageRequest):
    """
    Complete AI Triage Pipeline

    Patient Text
        ↓
    Input Validation
        ↓
    LLM Feature Extraction
        ↓
    Feature Preparation
        ↓
    Random Forest Prediction
        ↓
    Emergency Guardrail
        ↓
    RAG Retrieval
        ↓
    Recommendation
    """

    logger.info("Received request at /intake endpoint.")

    try:

        result = run_text_triage(request.patient_text)

        logger.info("/intake completed successfully.")

        return result

    except Exception:

        logger.exception("Error while processing /intake request.")

        raise