import json
import logging

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

load_dotenv()
# -----------------------------------------
# Logger
# -----------------------------------------
logger = logging.getLogger(__name__)

# -----------------------------
# Initialize Groq LLM
# -----------------------------
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

# -----------------------------
# Allowed feature names
# -----------------------------
ALLOWED_FIELDS = {
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
}

# -----------------------------
# Prompt
# -----------------------------
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert medical information extraction assistant.

Your job is ONLY to extract structured information that is explicitly mentioned by the patient.

Rules:

- Return ONLY a valid JSON object.
- Do NOT return markdown.
- Do NOT explain anything.
- Do NOT infer diseases.
- Do NOT guess missing values.
- Do NOT create new field names.
- Use ONLY the allowed field names listed below.
- Ignore any symptom that is not in the allowed list.

IMPORTANT:

If a symptom is NOT mentioned,
DO NOT include it.

Return a value of 0 ONLY if the patient explicitly denies the symptom.

Examples:

Input:
"I have chest pain."

Output:
{{
    "chest_pain": 1
}}

Input:
"I have chest pain but no vomiting."

Output:
{{
    "chest_pain": 1,
    "vomiting": 0
}}

Input:
"I don't have fever."

Output:
{{
    "fever": 0
}}

Never assume an unmentioned symptom is absent.
Allowed fields:

age
gender
fever
cough
sore_throat
body_ache
chest_pain
chest_tightness
shortness_of_breath
wheezing
dizziness
confusion
seizure
loss_of_consciousness
slurred_speech
facial_drooping
limb_weakness
severe_headache
abdominal_pain
nausea
vomiting
diarrhea
blood_in_stool
blood_in_urine
severe_bleeding
rash
swollen_tongue
swollen_throat
burns
fracture
pregnancy
pregnancy_bleeding
suicidal_thoughts
diabetes
hypertension
asthma
copd
heart_disease
kidney_disease
stroke_history
heart_rate
systolic_bp
oxygen_level
temperature
respiratory_rate
symptom_duration_hours

Encoding rules:

Binary values:
Present = 1
Explicitly absent = 0

Gender:
Male = 0
Female = 1

Duration:
Yesterday = 24
2 days = 48
3 days = 72

Convert other clearly mentioned durations into hours.

Return ONLY JSON.
"""
        ),
        (
            "human",
            "{patient_text}"
        )
    ]
)


def clean_response(text: str) -> str:
    text = text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")

    return text.strip()


def filter_fields(data: dict, patient_text: str) -> dict:
    """
    Keep only supported fields.
    Remove hallucinated fields.
    Keep 0 only when the patient explicitly negated the symptom.
    """

    cleaned = {}

    text = patient_text.lower()

    negation_words = [
        "no",
        "not",
        "don't",
        "doesn't",
        "didn't",
        "without",
        "denies",
        "deny",
        "never"
    ]

    for key, value in data.items():

        if key not in ALLOWED_FIELDS:
            continue

        # Always keep positive findings
        if value == 1:
            cleaned[key] = value
            continue

        # Always keep numeric values
        if key in {
            "age",
            "gender",
            "heart_rate",
            "systolic_bp",
            "oxygen_level",
            "temperature",
            "respiratory_rate",
            "symptom_duration_hours",
        }:
            cleaned[key] = value
            continue

        # Keep 0 only if the patient's text contains a negation
        if value == 0:
            symptom = key.replace("_", " ")

            explicit_negative = any(
                f"{neg} {symptom}" in text
                for neg in negation_words
            )

            if explicit_negative:
                cleaned[key] = 0


    logger.info(
    f"Filtered {len(cleaned)} supported feature(s) "
    f"from {len(data)} extracted field(s)."
)

    return cleaned

def extract_patient_features(patient_text: str) -> dict:
    """
    Extract structured medical features from free-text patient descriptions.
    """

    logger.info("Starting LLM feature extraction.")

    try:

        messages = prompt.format_messages(
            patient_text=patient_text
        )

        logger.info("Sending request to Groq LLM.")

        response = llm.invoke(messages)

        logger.info("Received response from Groq.")

        text = clean_response(response.content)

        extracted = json.loads(text)

        if not isinstance(extracted, dict):
            logger.error("LLM did not return a JSON object.")
            raise ValueError("LLM did not return a JSON object.")

        extracted = filter_fields(extracted, patient_text)

        logger.info(
            f"Feature extraction completed successfully. "
            f"Extracted {len(extracted)} feature(s)."
        )

        return extracted

    except json.JSONDecodeError:

        logger.exception("Failed to parse JSON returned by the LLM.")

        raise ValueError(
            f"LLM returned invalid JSON:\n\n{text}"
        )

    except Exception:

        logger.exception("Unexpected error during feature extraction.")

        raise