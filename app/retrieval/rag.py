from pathlib import Path
import logging
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from app.retrieval.generator import generate_recommendation


BASE_DIR = Path(__file__).resolve().parent
VECTOR_STORE_PATH = BASE_DIR / "vector_store"

# ------------------------------------------
# Logger
# ------------------------------------------
logger = logging.getLogger(__name__)

# ------------------------------------------
# Similarity Threshold
#
# Lower score = Better match
#
# Tune this value after testing.
# ------------------------------------------
SIMILARITY_THRESHOLD = 1.0


# Load embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load FAISS vector database
vector_db = FAISS.load_local(
    str(VECTOR_STORE_PATH),
    embeddings,
    allow_dangerous_deserialization=True
)


def build_search_query(features: dict, urgency: str) -> str:
    """
    Build a semantic search query using only meaningful features.
    """

    query = []

    symptom_names = {
        "fever": "fever",
        "cough": "cough",
        "sore_throat": "sore throat",
        "body_ache": "body ache",
        "chest_pain": "chest pain",
        "chest_tightness": "chest tightness",
        "shortness_of_breath": "shortness of breath",
        "wheezing": "wheezing",
        "dizziness": "dizziness",
        "confusion": "confusion",
        "seizure": "seizure",
        "loss_of_consciousness": "loss of consciousness",
        "slurred_speech": "slurred speech",
        "facial_drooping": "facial drooping",
        "limb_weakness": "limb weakness",
        "severe_headache": "severe headache",
        "abdominal_pain": "abdominal pain",
        "nausea": "nausea",
        "vomiting": "vomiting",
        "diarrhea": "diarrhea",
        "blood_in_stool": "blood in stool",
        "blood_in_urine": "blood in urine",
        "severe_bleeding": "severe bleeding",
        "rash": "rash",
        "swollen_tongue": "swollen tongue",
        "swollen_throat": "swollen throat",
        "burns": "burns",
        "fracture": "fracture",
        "pregnancy_bleeding": "pregnancy bleeding",
        "suicidal_thoughts": "suicidal thoughts",
        "asthma": "asthma",
        "copd": "COPD",
        "heart_disease": "heart disease",
        "kidney_disease": "kidney disease",
        "stroke_history": "stroke history"
    }

    for feature, text in symptom_names.items():
        if features.get(feature) == 1:
            query.append(text)

    oxygen = features.get("oxygen_level", 98)
    if oxygen < 90:
        query.append("low oxygen")

    temperature = features.get("temperature", 37)

    if temperature >= 39:
        query.append("high fever")

    query.append(f"{urgency} urgency")

    return " ".join(query)


def parse_guideline(document: str):
    """
    Extract guideline text and source from the retrieved document.
    """

    lines = [
        line.strip()
        for line in document.splitlines()
        if line.strip()
    ]

    guideline_parts = []
    source = "Unknown"

    for line in lines:

        if line.startswith("SOURCE:"):
            source = line.replace("SOURCE:", "").strip()

        elif line.startswith("TITLE:"):
            continue

        elif line.startswith("CATEGORY:"):
            continue

        elif line.isupper():
            continue

        else:
            guideline_parts.append(line)

    guideline = " ".join(guideline_parts).strip()

    return guideline, source


def generic_recommendation(urgency: str):
    """
    Return a safe fallback recommendation when
    no sufficiently similar guideline is found.
    """

    if urgency in ["Critical", "High"]:
        recommendation = (
            "We could not find a closely matching medical guideline for your symptoms. "
            "Based on the predicted urgency level, you should seek immediate medical attention "
            "or visit the nearest emergency department."
        )

    elif urgency == "Medium":
        recommendation = (
            "We could not find a closely matching medical guideline for your symptoms. "
            "Please consult a healthcare professional as soon as possible for further evaluation."
        )

    else:
        recommendation = (
            "We could not find a closely matching medical guideline for your symptoms. "
            "Monitor your symptoms and consult a healthcare professional if they worsen or persist."
        )

    return {
        "recommendation": recommendation,
        "source": "General Medical Guidance",
        "retrieved_guideline": ""
    }


def retrieve_recommendation(features: dict, urgency: str):
    """
    Retrieve the most relevant medical guideline.
    If the similarity score is poor, skip the LLM
    and return a generic recommendation.
    """

    logger.info("Starting guideline retrieval.")

    try:

        search_query = build_search_query(features, urgency)

        logger.info(f"Search query: {search_query}")

        results = vector_db.similarity_search_with_score(
            search_query,
            k=1
        )

        if not results:
            logger.warning("No matching guideline found.")
            return generic_recommendation(urgency)

        document, score = results[0]

        logger.info(f"Similarity score: {score:.4f}")

        # ------------------------------------------
        # Reject weak matches
        # ------------------------------------------
        if score > SIMILARITY_THRESHOLD:

            logger.warning(
                "Low similarity score detected. "
                "Returning generic recommendation."
            )

            return generic_recommendation(urgency)

        guideline, source = parse_guideline(document.page_content)

        logger.info(f"Retrieved guideline source: {source}")

        recommendation = generate_recommendation(
            symptoms=features,
            urgency=urgency,
            guideline=guideline
        )

        logger.info("Recommendation generated successfully.")
        logger.info(
    f"Using generic recommendation for urgency: {urgency}"
)

        return {
            "recommendation": recommendation,
            "source": source,
            "retrieved_guideline": guideline
        }

    except Exception:
        logger.exception("Guideline retrieval failed.")
        raise