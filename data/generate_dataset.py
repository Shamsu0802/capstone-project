import random
import pandas as pd

random.seed(42)

NUM_PATIENTS = 2000

patients = []

SCENARIOS = {
    "common_cold": 250,
    "viral_fever": 250,
    "pneumonia": 180,
    "asthma_attack": 150,
    "heart_attack": 150,
    "stroke": 120,
    "trauma": 180,
    "food_poisoning": 180,
    "allergic_reaction": 120,
    "uti": 150,
    "pregnancy_emergency": 80,
    "mental_health": 170
}

COLUMNS = [
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

    "urgency"
]
def base_patient():

    age = random.randint(18,90)

    gender = random.choice(["Male","Female"])

    patient = {

        "age":age,
        "gender":gender,

        "fever":0,
        "cough":0,
        "sore_throat":0,
        "body_ache":0,

        "chest_pain":0,
        "chest_tightness":0,
        "shortness_of_breath":0,
        "wheezing":0,

        "dizziness":0,
        "confusion":0,
        "seizure":0,
        "loss_of_consciousness":0,

        "slurred_speech":0,
        "facial_drooping":0,
        "limb_weakness":0,

        "severe_headache":0,

        "abdominal_pain":0,
        "nausea":0,
        "vomiting":0,
        "diarrhea":0,

        "blood_in_stool":0,
        "blood_in_urine":0,

        "severe_bleeding":0,

        "rash":0,
        "swollen_tongue":0,
        "swollen_throat":0,

        "burns":0,
        "fracture":0,

        "pregnancy":0,
        "pregnancy_bleeding":0,

        "suicidal_thoughts":0,

        "diabetes":0,
        "hypertension":0,
        "asthma":0,
        "copd":0,
        "heart_disease":0,
        "kidney_disease":0,
        "stroke_history":0,

        "heart_rate":random.randint(65,95),
        "systolic_bp":random.randint(110,130),
        "oxygen_level":random.randint(96,100),
        "temperature":round(random.uniform(97.2,99.1),1),
        "respiratory_rate":random.randint(14,20),

        "symptom_duration_hours":random.randint(2,48),

        "urgency":"Low"

    }

    return patient

# ============================================================
# COMMON COLD
# ============================================================

def generate_common_cold():

    p = base_patient()

    p["fever"] = random.choices([0,1],[70,30])[0]
    p["cough"] = 1
    p["sore_throat"] = 1

    p["temperature"] = round(random.uniform(98.5,100.2),1)
    p["heart_rate"] = random.randint(70,95)
    p["oxygen_level"] = random.randint(97,100)

    p["symptom_duration_hours"] = random.randint(24,96)

    p["urgency"] = "Low"

    return p


# ============================================================
# VIRAL FEVER
# ============================================================

def generate_viral_fever():

    p = base_patient()

    p["fever"] = 1
    p["cough"] = random.choice([0,1])
    p["sore_throat"] = random.choice([0,1])

    p["body_ache"] = 1 if random.random() < 0.8 else 0

    p["temperature"] = round(random.uniform(100.0,103.5),1)

    p["heart_rate"] = random.randint(80,110)

    p["oxygen_level"] = random.randint(95,99)

    p["symptom_duration_hours"] = random.randint(12,72)

    if p["temperature"] >= 103:
        p["urgency"] = "Medium"
    else:
        p["urgency"] = "Low"

    return p


# ============================================================
# PNEUMONIA
# ============================================================

def generate_pneumonia():

    p = base_patient()

    p["age"] = random.randint(45,90)

    p["fever"] = 1
    p["cough"] = 1
    p["shortness_of_breath"] = 1

    p["heart_rate"] = random.randint(95,125)

    p["oxygen_level"] = random.randint(88,95)

    p["temperature"] = round(random.uniform(101,104),1)

    p["respiratory_rate"] = random.randint(22,32)

    if random.random() < 0.5:
        p["copd"] = 1

    if p["oxygen_level"] < 90:
        p["urgency"] = "High"
    else:
        p["urgency"] = "Medium"

    return p


# ============================================================
# ASTHMA ATTACK
# ============================================================

def generate_asthma_attack():

    p = base_patient()

    p["age"] = random.randint(18,60)

    p["asthma"] = 1

    p["shortness_of_breath"] = 1
    p["wheezing"] = 1

    p["heart_rate"] = random.randint(90,125)

    p["oxygen_level"] = random.randint(89,97)

    p["respiratory_rate"] = random.randint(22,34)

    if random.random() < 0.35:
        p["chest_tightness"] = 1

    if p["oxygen_level"] < 91:
        p["urgency"] = "High"
    else:
        p["urgency"] = "Medium"

    return p
# ============================================================
# HEART ATTACK
# ============================================================

def generate_heart_attack():

    p = base_patient()

    p["age"] = random.randint(45, 90)

    p["heart_disease"] = random.choices([0,1],[30,70])[0]
    p["hypertension"] = random.choices([0,1],[40,60])[0]
    p["diabetes"] = random.choices([0,1],[50,50])[0]

    p["chest_pain"] = 1
    p["chest_tightness"] = 1
    p["shortness_of_breath"] = 1

    p["dizziness"] = random.choice([0,1])

    p["heart_rate"] = random.randint(100,140)
    p["systolic_bp"] = random.randint(140,190)
    p["oxygen_level"] = random.randint(84,95)

    p["respiratory_rate"] = random.randint(22,30)

    p["symptom_duration_hours"] = random.randint(1,6)

    p["urgency"] = "Critical"

    return p


# ============================================================
# STROKE
# ============================================================

def generate_stroke():

    p = base_patient()

    p["age"] = random.randint(50,90)

    p["stroke_history"] = random.choice([0,1])

    p["hypertension"] = 1

    p["slurred_speech"] = 1
    p["facial_drooping"] = 1
    p["limb_weakness"] = 1

    p["confusion"] = random.choice([0,1])

    p["heart_rate"] = random.randint(85,120)
    p["systolic_bp"] = random.randint(160,200)

    p["oxygen_level"] = random.randint(90,98)

    p["symptom_duration_hours"] = random.randint(1,5)

    p["urgency"] = "Critical"

    return p


# ============================================================
# TRAUMA
# ============================================================

def generate_trauma():

    p = base_patient()

    p["age"] = random.randint(18,70)

    p["fracture"] = random.choice([0,1])

    p["burns"] = random.choice([0,1])

    p["severe_bleeding"] = random.choices([0,1],[60,40])[0]

    p["heart_rate"] = random.randint(90,130)

    p["oxygen_level"] = random.randint(90,99)

    if p["severe_bleeding"]:

        p["urgency"] = "Critical"

    elif p["fracture"]:

        p["urgency"] = "High"

    elif p["burns"]:

        p["urgency"] = "High"

    else:

        p["urgency"] = "Medium"

    return p


# ============================================================
# SEVERE ALLERGIC REACTION
# ============================================================

def generate_allergic_reaction():

    p = base_patient()

    p["rash"] = 1

    p["swollen_tongue"] = random.choice([0,1])

    p["swollen_throat"] = random.choice([0,1])

    if p["swollen_throat"]:

        p["shortness_of_breath"] = 1

    p["oxygen_level"] = random.randint(86,98)

    p["heart_rate"] = random.randint(85,125)

    p["respiratory_rate"] = random.randint(18,32)

    if p["swollen_throat"]:

        p["urgency"] = "Critical"

    else:

        p["urgency"] = "Medium"

    return p

# ============================================================
# FOOD POISONING
# ============================================================

def generate_food_poisoning():

    p = base_patient()

    p["age"] = random.randint(18,70)

    p["abdominal_pain"] = 1
    p["nausea"] = 1
    p["vomiting"] = 1
    p["diarrhea"] = random.choice([0,1])

    p["temperature"] = round(random.uniform(98.6,101.2),1)

    p["heart_rate"] = random.randint(75,110)

    p["oxygen_level"] = random.randint(96,100)

    p["symptom_duration_hours"] = random.randint(4,48)

    if p["vomiting"] and p["diarrhea"]:
        p["urgency"] = "Medium"
    else:
        p["urgency"] = "Low"

    return p


# ============================================================
# URINARY TRACT INFECTION
# ============================================================

def generate_uti():

    p = base_patient()

    p["age"] = random.randint(18,85)

    if p["gender"] == "Male":
        p["gender"] = random.choices(["Female","Male"], [80,20])[0]

    p["fever"] = random.choice([0,1])

    p["blood_in_urine"] = random.choices([0,1],[70,30])[0]

    p["temperature"] = round(random.uniform(98.2,102.5),1)

    p["heart_rate"] = random.randint(70,105)

    p["oxygen_level"] = random.randint(96,100)

    if p["fever"] and p["blood_in_urine"]:
        p["urgency"] = "Medium"
    else:
        p["urgency"] = "Low"

    return p


# ============================================================
# PREGNANCY EMERGENCY
# ============================================================

def generate_pregnancy_emergency():

    p = base_patient()

    p["gender"] = "Female"

    p["age"] = random.randint(20,40)

    p["pregnancy"] = 1
    p["pregnancy_bleeding"] = 1

    p["abdominal_pain"] = 1

    p["heart_rate"] = random.randint(90,125)

    p["systolic_bp"] = random.randint(90,150)

    p["oxygen_level"] = random.randint(93,100)

    p["urgency"] = "Critical"

    return p


# ============================================================
# MENTAL HEALTH CRISIS
# ============================================================

def generate_mental_health():

    p = base_patient()

    p["age"] = random.randint(18,70)

    p["suicidal_thoughts"] = random.choices([0,1],[50,50])[0]

    p["confusion"] = random.choice([0,1])

    p["heart_rate"] = random.randint(80,120)

    p["oxygen_level"] = random.randint(96,100)

    if p["suicidal_thoughts"]:
        p["urgency"] = "Critical"
    else:
        p["urgency"] = "Medium"

    return p

# ============================================================
# SCENARIO MAP
# ============================================================

scenario_functions = {

    "common_cold": generate_common_cold,
    "viral_fever": generate_viral_fever,
    "pneumonia": generate_pneumonia,
    "asthma_attack": generate_asthma_attack,

    "heart_attack": generate_heart_attack,
    "stroke": generate_stroke,
    "trauma": generate_trauma,
    "allergic_reaction": generate_allergic_reaction,

    "food_poisoning": generate_food_poisoning,
    "uti": generate_uti,
    "pregnancy_emergency": generate_pregnancy_emergency,
    "mental_health": generate_mental_health
}


# ============================================================
# GENERATE DATASET
# ============================================================

for scenario, count in SCENARIOS.items():

    generator = scenario_functions[scenario]

    for _ in range(count):

        patients.append(generator())


# ============================================================
# CREATE DATAFRAME
# ============================================================

df = pd.DataFrame(patients)

df = df[COLUMNS]

df = df.sample(frac=1, random_state=42).reset_index(drop=True)

df.to_csv("data/simulated_patients.csv", index=False)

print("="*60)
print("DATASET CREATED")
print("="*60)

print(df.head())

print("\nShape:", df.shape)

print("\nUrgency Distribution\n")

print(df["urgency"].value_counts())

print("\nPercentage Distribution\n")

print((df["urgency"].value_counts(normalize=True)*100).round(2))