# AI-Powered Patient Triage & Risk Assessment Assistant

An AI-powered healthcare triage system that analyzes patient symptoms, predicts medical urgency, applies deterministic medical guardrails, and retrieves evidence-based medical recommendations using Retrieval-Augmented Generation (RAG).

The system supports both **structured patient information** and **free-text symptom descriptions**, helping healthcare professionals prioritize patients more efficiently.

---

##  Features

- Structured patient risk prediction using Machine Learning
- Free-text symptom analysis using Groq Llama-3.1-8B-Instant
- Automatic clinical feature extraction
- Random Forest urgency prediction
- Deterministic medical guardrails for patient safety
- Retrieval-Augmented Generation (RAG) for guideline-based recommendations
- FastAPI backend with REST APIs
- Interactive frontend built with HTML, CSS, and JavaScript
- Input validation and prompt injection protection
- Unit testing using Pytest

---

# Project Overview

Hospitals and telehealth platforms receive thousands of patient symptom descriptions every day. Since every patient typically enters the same waiting queue, critically ill patients may experience delays in receiving medical attention.

This project develops an intelligent patient triage assistant capable of:

- Understanding natural language symptom descriptions
- Predicting patient urgency
- Prioritizing cases
- Applying medical safety rules
- Retrieving relevant clinical guidelines
- Providing evidence-based recommendations

The system is designed to **assist healthcare professionals** rather than replace clinical decision-making.

---

# Technology Stack

## Backend

- Python
- FastAPI
- Pydantic
- Scikit-learn
- LangChain
- FAISS
- HuggingFace Embeddings
- Groq API
- Llama-3.1-8B-Instant

## Machine Learning

- Random Forest Classifier
- Decision Tree (comparison model)

## Frontend

- HTML
- CSS
- JavaScript

## Database

- FAISS Vector Store

## Testing

- Pytest

---

# Project Structure

```text
Final-Mini-Project/
│
├── app/
│   ├── api/
│   ├── extraction/
│   ├── guardrails/
│   ├── retrieval/
│   ├── risk_model/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   └── main.py
│
├── data/
│
├── frontend/
│
├── models/
│
├── tests/
│
├── requirements.txt
└── README.md
```

---

# System Architecture

```
Patient Input
      │
      ▼
Input Validation
      │
      ▼
LLM Feature Extraction
(Groq Llama-3.1-8B)
      │
      ▼
Feature Preparation
      │
      ▼
Random Forest Model
      │
      ▼
Medical Guardrails
      │
      ▼
RAG Retrieval
      │
      ▼
Medical Recommendation
      │
      ▼
Frontend Display
```

---

# Machine Learning Model

The patient urgency prediction model was trained using a synthetic healthcare dataset.

### Dataset

- 1,980 patient records
- 46 input features
- 4 urgency classes

Urgency Levels:

- Low
- Medium
- High
- Critical

### Features Include

- Patient demographics
- Symptoms
- Medical history
- Vital signs
- Symptom duration

---

# AI Pipeline

The free-text triage pipeline consists of:

1. Input validation
2. Prompt injection detection
3. LLM-based feature extraction
4. Feature preprocessing
5. Random Forest prediction
6. Medical guardrail verification
7. RAG guideline retrieval
8. Recommendation generation

---

# Retrieval-Augmented Generation (RAG)

The system retrieves relevant medical guidelines from a FAISS vector database.

Workflow:

Medical Guidelines

↓

Embedding Generation

↓

FAISS Search

↓

Relevant Context Retrieval

↓

Recommendation Generation

---

# Medical Guardrails

To improve patient safety, deterministic medical rules override machine learning predictions whenever emergency conditions are detected.

Examples include:

- Heart attack
- Stroke
- Severe bleeding
- Airway obstruction
- Seizures
- Loss of consciousness
- Pregnancy emergencies
- Very low oxygen saturation

---

# REST API Endpoints

## Structured Prediction

```
POST /predict
```

Predicts urgency using structured patient information.

---

## AI Intake

```
POST /intake
```

Accepts free-text symptom descriptions and returns:

- Extracted clinical features
- Predicted urgency
- Medical recommendation
- Supporting guideline

---

# Frontend

The web application includes:

- Home page
- Structured prediction page
- AI intake page

Users can either:

- Enter structured patient information
- Describe symptoms in natural language

The frontend communicates with the FastAPI backend using the Fetch API.

---

# Running the Project

## 1. Clone Repository

```bash
git clone https://github.com/<your-username>/Final-Mini-Project.git
cd Final-Mini-Project
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```



## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_api_key
```

---

## 5. Build the Vector Store

```bash
python app/retrieval/build_vectorstore.py
```

---

## 6. Run the Backend

```bash
uvicorn app.main:app --reload
```

Backend:

```
http://127.0.0.1:8000
```

Swagger Documentation:

```
http://127.0.0.1:8000/docs
```

---

## 7. Launch the Frontend

Open the `frontend/index.html` file in your browser.

---



