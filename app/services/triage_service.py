import logging

from app.extraction.extractor import extract_patient_features
from app.guardrails.validator import validate_patient_text
from app.retrieval.rag import retrieve_recommendation
from app.risk_model.predictor import predict

# -----------------------------------------
# Logger
# -----------------------------------------
logger = logging.getLogger(__name__)

# Default values required by the Random Forest model
DEFAULT_FEATURES = {
    "age": 0,
    "gender": 0,
    "fever": 0,
    "cough": 0,
    "sore_throat": 0,
    "body_ache": 0,
    "chest_pain": 0,
    "chest_tightness": 0,
    "shortness_of_breath": 0,
    "wheezing": 0,
    "dizziness": 0,
    "confusion": 0,
    "seizure": 0,
    "loss_of_consciousness": 0,
    "slurred_speech": 0,
    "facial_drooping": 0,
    "limb_weakness": 0,
    "severe_headache": 0,
    "abdominal_pain": 0,
    "nausea": 0,
    "vomiting": 0,
    "diarrhea": 0,
    "blood_in_stool": 0,
    "blood_in_urine": 0,
    "severe_bleeding": 0,
    "rash": 0,
    "swollen_tongue": 0,
    "swollen_throat": 0,
    "burns": 0,
    "fracture": 0,
    "pregnancy": 0,
    "pregnancy_bleeding": 0,
    "suicidal_thoughts": 0,
    "diabetes": 0,
    "hypertension": 0,
    "asthma": 0,
    "copd": 0,
    "heart_disease": 0,
    "kidney_disease": 0,
    "stroke_history": 0,
    "heart_rate": 80,
    "systolic_bp": 120,
    "oxygen_level": 98,
    "temperature": 37.0,
    "respiratory_rate": 18,
    "symptom_duration_hours": 0
}


def prepare_features(extracted_features: dict) -> dict:
    """
    Fill missing features so the Random Forest model
    always receives all required features.
    """
    features = DEFAULT_FEATURES.copy()
    features.update(extracted_features)
    return features
def apply_guardrail_override(features: dict, predicted_urgency: str):
    """
    Deterministic medical guardrail.

    Life-threatening conditions always override the ML prediction.
    High-risk conditions are upgraded to High.
    Otherwise, the ML prediction is returned.
    """

    # ==========================================================
    # CRITICAL CONDITIONS
    # ==========================================================

    # Heart attack
    if (
        features.get("chest_pain", 0)
        and features.get("shortness_of_breath", 0)
    ):
        logger.warning("Emergency Guardrail: Suspected Heart Attack")
        return "Critical"

    # Stroke
    if (
        features.get("slurred_speech", 0)
        or (
            features.get("facial_drooping", 0)
            and features.get("limb_weakness", 0)
        )
    ):
        logger.warning("Emergency Guardrail: Suspected Stroke")
        return "Critical"

    # Loss of consciousness
    if features.get("loss_of_consciousness", 0):
        logger.warning("Emergency Guardrail: Loss of Consciousness")
        return "Critical"

    # Seizure
    if features.get("seizure", 0):
        logger.warning("Emergency Guardrail: Seizure")
        return "Critical"

    # Severe bleeding
    if features.get("severe_bleeding", 0):
        logger.warning("Emergency Guardrail: Severe Bleeding")
        return "Critical"

    # Airway obstruction
    if (
        features.get("swollen_tongue", 0)
        or features.get("swollen_throat", 0)
    ):
        logger.warning("Emergency Guardrail: Airway Obstruction")
        return "Critical"

    # Pregnancy emergency
    if features.get("pregnancy_bleeding", 0):
        logger.warning("Emergency Guardrail: Pregnancy Emergency")
        return "Critical"

    # Mental health emergency
    if features.get("suicidal_thoughts", 0):
        logger.warning("Emergency Guardrail: Suicidal Thoughts")
        return "Critical"

    # Very low oxygen
    oxygen = features.get("oxygen_level")
    if oxygen is not None and oxygen <= 90:
        logger.warning("Emergency Guardrail: Critically Low Oxygen")
        return "Critical"

    # ==========================================================
    # HIGH-RISK CONDITIONS
    # ==========================================================

    # Kidney infection / kidney emergency
    if (
        features.get("kidney_disease", 0)
        and features.get("blood_in_urine", 0)
        and (
            features.get("fever", 0)
            or features.get("abdominal_pain", 0)
        )
    ):
        logger.warning("Guardrail: Kidney Emergency")
        return "High"

    # Asthma attack
    if (
        features.get("asthma", 0)
        and (
            features.get("shortness_of_breath", 0)
            or features.get("wheezing", 0)
        )
    ):
        logger.warning("Guardrail: Asthma Exacerbation")
        return "High"

    # COPD exacerbation
    if (
        features.get("copd", 0)
        and features.get("shortness_of_breath", 0)
    ):
        logger.warning("Guardrail: COPD Exacerbation")
        return "High"

    # Elderly patient with confusion
    if (
        features.get("age", 0) >= 65
        and features.get("confusion", 0)
    ):
        logger.warning("Guardrail: Elderly Patient with Confusion")
        return "High"

    # Fever with breathing difficulty
    if (
        features.get("fever", 0)
        and features.get("shortness_of_breath", 0)
    ):
        logger.warning("Guardrail: Respiratory Infection")
        return "High"

    # Blood in stool
    if features.get("blood_in_stool", 0):
        logger.warning("Guardrail: Blood in Stool")
        return "High"

    # Blood in urine without kidney disease
    if features.get("blood_in_urine", 0):
        logger.warning("Guardrail: Blood in Urine")
        return "High"

    # Burns
    if features.get("burns", 0):
        logger.warning("Guardrail: Burns")
        return "High"

    # Fracture
    if features.get("fracture", 0):
        logger.warning("Guardrail: Suspected Fracture")
        return "High"

    # Low oxygen
    if oxygen is not None and 90 < oxygen <= 94:
        logger.warning("Guardrail: Low Oxygen")
        return "High"

    # High heart rate
    heart_rate = features.get("heart_rate")
    if heart_rate is not None and heart_rate >= 120:
        logger.warning("Guardrail: High Heart Rate")
        return "High"

    # Fast breathing
    respiratory_rate = features.get("respiratory_rate")
    if respiratory_rate is not None and respiratory_rate >= 28:
        logger.warning("Guardrail: Fast Breathing")
        return "High"

    # ==========================================================
    # Otherwise, keep the ML prediction
    # ==========================================================

    return predicted_urgency
def detect_text_emergency(patient_text: str) -> bool:
    """
    Emergency keyword detection used when the LLM is unavailable.
    """

    text = patient_text.lower()

    return (
        ("chest pain" in text and "shortness of breath" in text)
        or "loss of consciousness" in text
        or "seizure" in text
        or "slurred speech" in text
        or ("facial drooping" in text and "limb weakness" in text)
        or "severe bleeding" in text
        or ("swollen tongue" in text and "swollen throat" in text)
        or (
            ("pregnant" in text or "pregnancy" in text)
            and "bleeding" in text
        )
        or "suicidal" in text
    )

def run_triage(patient_data: dict):
    """
    Predict urgency from structured patient data.
    Used by the /predict endpoint.
    """

    logger.info("Received structured patient data for triage.")

    try:
        # -----------------------------------------
        # Step 1: Prepare Complete Feature Vector
        # -----------------------------------------
        model_features = prepare_features(patient_data)

        logger.info("Prepared feature vector for prediction.")

        # -----------------------------------------
        # Step 2: Predict Urgency
        # -----------------------------------------
        urgency = predict(model_features)

        logger.info(f"Predicted urgency before guardrail: {urgency}")

        # -----------------------------------------
        # Step 3: Apply Safety Guardrail
        # -----------------------------------------
        urgency = apply_guardrail_override(
            model_features,
            urgency
        )

        logger.info(f"Final urgency after guardrail: {urgency}")

        # -----------------------------------------
        # Step 4: Retrieve Recommendation
        # -----------------------------------------
        rag_result = retrieve_recommendation(
            model_features,
            urgency
        )

        logger.info("Recommendation retrieved successfully.")

        # -----------------------------------------
        # Step 5: Return Response
        # -----------------------------------------
        return {
    "status": "success",
    "urgency": urgency
}

    except Exception:
        logger.exception("Structured triage pipeline failed.")
        raise

def run_text_triage(patient_text: str):
    """
    Complete AI Triage Pipeline

    Patient Text
        ↓
    Guardrails
        ↓
    LLM Feature Extraction
        ↓
    Feature Preparation
        ↓
    Random Forest Prediction
        ↓
    Safety Guardrail Override
        ↓
    FAISS Retrieval
        ↓
    Groq Recommendation Generation
        ↓
    Final Response
    """

    logger.info("New patient triage request received.")

    try:

        # -----------------------------------------
        # Step 1: Validate Patient Input
        # -----------------------------------------
        valid, error = validate_patient_text(patient_text)

        if not valid:
            logger.warning(f"Input validation failed: {error}")
            return {
                "status": "failed",
                "error": error
            }

        logger.info("Patient input validation successful.")

        # -----------------------------------------
        # Step 2: Extract Features using Groq
        # -----------------------------------------
        try:
            extracted_features = extract_patient_features(patient_text)

            logger.info(
                f"Extracted {len(extracted_features)} feature(s)."
            )

        except Exception:

            logger.exception("LLM extraction failed.")

            if detect_text_emergency(patient_text):
                logger.warning(
                    "Emergency detected while LLM is unavailable."
                )

                return {
                    "status": "success",
                    "urgency": "Critical",
                    "features": {},
                    "recommendation":
                        "Potential emergency detected. Immediate human review required.",
                    "source": "Emergency Guardrail",
                    "retrieved_guideline": ""
                }

            return {
                "status": "failed",
                "error": "LLM extraction is temporarily unavailable."
            }

        # -----------------------------------------
        # Step 3: Prepare Feature Vector
        # -----------------------------------------
        model_features = prepare_features(extracted_features)

        logger.info("Feature vector prepared for Random Forest.")

        # -----------------------------------------
        # Step 4: Predict Urgency
        # -----------------------------------------
        urgency = predict(model_features)

        logger.info(f"Predicted urgency before guardrail: {urgency}")

        urgency = apply_guardrail_override(
            model_features,
            urgency
        )

        logger.info(f"Final urgency after guardrail: {urgency}")

        # -----------------------------------------
        # Step 5: Retrieve Recommendation
        # -----------------------------------------
        rag_result = retrieve_recommendation(
            model_features,
            urgency
        )

        logger.info(
            f"Recommendation source: {rag_result['source']}"
        )

        # -----------------------------------------
        # Step 6: Final Response
        # -----------------------------------------
        logger.info("Patient triage completed successfully.")

        return {
    "status": "success",
    "urgency": urgency,
    "features": extracted_features,
    "recommendation": rag_result["recommendation"],
    "source": rag_result["source"],
    "retrieved_guideline": rag_result.get(
        "retrieved_guideline", ""
    )
}

    except Exception:
        logger.exception("AI triage pipeline failed.")
        raise