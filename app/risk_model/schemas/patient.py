from pydantic import BaseModel


class Patient(BaseModel):
    # Demographics
    age: int = 0
    gender: int = 0

    # Symptoms
    fever: int = 0
    cough: int = 0
    sore_throat: int = 0
    body_ache: int = 0

    chest_pain: int = 0
    chest_tightness: int = 0
    shortness_of_breath: int = 0
    wheezing: int = 0

    dizziness: int = 0
    confusion: int = 0
    seizure: int = 0
    loss_of_consciousness: int = 0
    slurred_speech: int = 0
    facial_drooping: int = 0
    limb_weakness: int = 0
    severe_headache: int = 0

    abdominal_pain: int = 0
    nausea: int = 0
    vomiting: int = 0
    diarrhea: int = 0
    blood_in_stool: int = 0
    blood_in_urine: int = 0
    severe_bleeding: int = 0

    rash: int = 0
    swollen_tongue: int = 0
    swollen_throat: int = 0

    burns: int = 0
    fracture: int = 0

    pregnancy: int = 0
    pregnancy_bleeding: int = 0

    suicidal_thoughts: int = 0

    # Medical History
    diabetes: int = 0
    hypertension: int = 0
    asthma: int = 0
    copd: int = 0
    heart_disease: int = 0
    kidney_disease: int = 0
    stroke_history: int = 0

    # Vitals
    heart_rate: int = 80
    systolic_bp: int = 120
    oxygen_level: int = 98
    temperature: float = 37.0
    respiratory_rate: int = 18

    # Duration
    symptom_duration_hours: int = 0