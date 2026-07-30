import logging
from pathlib import Path

import joblib
import pandas as pd

# -----------------------------------------
# Logger
# -----------------------------------------
logger = logging.getLogger(__name__)

# -----------------------------------------
# Load Random Forest Model
# -----------------------------------------
MODEL_PATH = Path("models/random_forest_triage_model.pkl")

try:
    model = joblib.load(MODEL_PATH)
    logger.info(f"Random Forest model loaded successfully from {MODEL_PATH}")

except Exception:
    logger.exception("Failed to load Random Forest model.")
    raise

# -----------------------------------------
# Feature order used during training
# -----------------------------------------
FEATURES = [
    "age",
    "gender",
    "fever",
    "cough",
    "sore_throat",
    "body_ache",
    "chest_pain",
    "chest_tightness",
    "shortness_of_breath",
    "wheezing",
    "dizziness",
    "confusion",
    "seizure",
    "loss_of_consciousness",
    "slurred_speech",
    "facial_drooping",
    "limb_weakness",
    "severe_headache",
    "abdominal_pain",
    "nausea",
    "vomiting",
    "diarrhea",
    "blood_in_stool",
    "blood_in_urine",
    "severe_bleeding",
    "rash",
    "swollen_tongue",
    "swollen_throat",
    "burns",
    "fracture",
    "pregnancy",
    "pregnancy_bleeding",
    "suicidal_thoughts",
    "diabetes",
    "hypertension",
    "asthma",
    "copd",
    "heart_disease",
    "kidney_disease",
    "stroke_history",
    "heart_rate",
    "systolic_bp",
    "oxygen_level",
    "temperature",
    "respiratory_rate",
    "symptom_duration_hours",
]

LABELS = {
    0: "Low",
    1: "Medium",
    2: "High",
    3: "Critical"
}


def predict(features: dict):
    """
    Predict the urgency level using the trained Random Forest model.
    """

    logger.info("Starting urgency prediction.")

    try:
        # Convert input features into DataFrame
        df = pd.DataFrame([features])

        # Ensure the feature order matches the training data
        df = df[FEATURES]

        # Predict
        prediction = model.predict(df)[0]

        urgency = LABELS[prediction]

        logger.info(f"Predicted urgency: {urgency}")

        return urgency

    except Exception:
        logger.exception("Random Forest prediction failed.")
        raise