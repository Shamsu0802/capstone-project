import re


# Common prompt injection phrases
PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+previous",
    r"ignore\s+all",
    r"forget\s+previous",
    r"system\s+prompt",
    r"developer\s+message",
    r"act\s+as",
    r"pretend\s+to",
    r"always\s+return",
    r"bypass",
    r"override",
]


def validate_patient_text(patient_text: str):
    """
    Validate patient input before sending it to the LLM.

    Returns:
        (True, None) if valid
        (False, error_message) if invalid
    """

    if patient_text is None:
        return False, "Patient description is required."

    patient_text = patient_text.strip()

    # Empty input
    if len(patient_text) == 0:
        return False, "Patient description cannot be empty."

    # Very short input
    if len(patient_text) < 10:
        return False, "Patient description is too short."

    # Very long input
    if len(patient_text) > 3000:
        return False, "Patient description is too long."

    # Prompt injection detection
    text = patient_text.lower()

    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, text):
            return False, "Potential prompt injection detected."

    return True, None