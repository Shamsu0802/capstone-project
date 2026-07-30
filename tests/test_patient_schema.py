from app.schemas.patient import Patient


def test_patient_schema():

    patient = Patient(
        age=45,
        gender=0,

        fever=1,
        cough=1,
        sore_throat=0,
        body_ache=1,

        chest_pain=0,
        chest_tightness=0,
        shortness_of_breath=0,
        wheezing=0,

        dizziness=0,
        confusion=0,
        seizure=0,
        loss_of_consciousness=0,
        slurred_speech=0,
        facial_drooping=0,
        limb_weakness=0,
        severe_headache=0,

        abdominal_pain=0,
        nausea=0,
        vomiting=0,
        diarrhea=0,
        blood_in_stool=0,
        blood_in_urine=0,
        severe_bleeding=0,

        rash=0,
        swollen_tongue=0,
        swollen_throat=0,

        burns=0,
        fracture=0,

        pregnancy=0,
        pregnancy_bleeding=0,

        suicidal_thoughts=0,

        diabetes=0,
        hypertension=0,
        asthma=0,
        copd=0,
        heart_disease=0,
        kidney_disease=0,
        stroke_history=0,

        heart_rate=80,
        systolic_bp=120,
        oxygen_level=98,
        temperature=37.0,
        respiratory_rate=18,
        symptom_duration_hours=24
    )

    assert patient.age == 45
    assert patient.fever == 1
    assert patient.heart_rate == 80