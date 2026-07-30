import os

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

load_dotenv()


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.1,
)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an AI-powered Patient Triage Recommendation Assistant.

Your task is to generate a clear, safe, and patient-friendly recommendation
using ONLY the retrieved medical guideline.

You will receive:

1. Extracted patient symptoms
2. Predicted urgency level
3. Retrieved medical guideline

Instructions:

- Use ONLY the retrieved guideline.
- Do NOT add medical facts that are not present in the guideline.
- Never diagnose a disease.
- Explain the recommendation in simple English.
- Address the user as "you".
- Mention the urgency naturally.
- Keep the response between 2 and 4 sentences.
- If the urgency is Critical or High, encourage immediate medical attention.
- If the urgency is Medium, advise consultation within 24 hours.
- If the urgency is Low, advise monitoring symptoms and seeking care if they worsen.
- Do not mention AI, models, predictions, or algorithms.
- Do not repeat the guideline word-for-word.
- Be supportive, professional, and concise.
"""
        ),
        (
            "human",
            """
Patient Symptoms:
{symptoms}

Predicted Urgency:
{urgency}

Retrieved Medical Guideline:
{guideline}

Generate a patient-friendly recommendation.
"""
        ),
    ]
)


def generate_recommendation(
    symptoms: dict,
    urgency: str,
    guideline: str
):
    """
    Generate a patient-friendly recommendation
    using the retrieved medical guideline.
    """

    if not guideline.strip():
        return (
            "Based on the available information, please consult a healthcare "
            "professional for further evaluation."
        )

    messages = prompt.format_messages(
        symptoms=symptoms,
        urgency=urgency,
        guideline=guideline,
    )

    response = llm.invoke(messages)

    return response.content.strip()