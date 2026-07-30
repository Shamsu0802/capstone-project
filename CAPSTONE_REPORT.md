# Problem Statement

## Overview

Hospitals and telehealth platforms receive a large number of patient requests every day. Before consulting a doctor, patients typically describe their symptoms using free-text messages through online consultation systems or telemedicine platforms. These messages vary in length and detail, making it difficult for healthcare professionals to quickly identify patients who require immediate medical attention.

In the traditional workflow, every patient enters the same waiting queue regardless of the severity of their condition. As a result, patients experiencing life-threatening emergencies such as heart attacks or strokes may have to wait alongside patients with minor illnesses like the common cold. This manual triage process can delay treatment, increase the workload of healthcare professionals, and reduce the overall efficiency of the healthcare system.

The objective of this project is to develop an AI-powered Patient Triage and Risk Assessment Assistant capable of automatically analyzing patient information, estimating the urgency level, and providing supporting medical recommendations. The system is intended to assist healthcare professionals in prioritizing patient cases rather than replacing clinical decision-making.

### Project Objectives

The primary objectives of this project are:

- Develop an intelligent triage system that can analyze patient symptoms.
- Predict the urgency level of a patient's condition.
- Prioritize patients based on the severity of their symptoms.
- Support both structured patient information and natural language symptom descriptions.
- Assist healthcare professionals by providing guideline-based recommendations.
- Improve the efficiency of the patient screening process.

---

# Proposed Solution

To address the limitations of manual patient triage, an AI-based Patient Triage and Risk Assessment Assistant was developed. The proposed solution combines machine learning, large language models, rule-based medical guardrails, and retrieval-based recommendations into a single intelligent system.

The system accepts patient information in two different formats:

1. Structured patient information through a web form.
2. Free-text symptom descriptions written in natural language.

For structured inputs, the patient information is directly processed by the trained Random Forest model to predict the urgency level.

For free-text inputs, the system first validates the input to prevent invalid or malicious requests. The validated text is then processed using the Groq Llama-3.1-8B-Instant large language model, which extracts structured medical features such as symptoms, age, gender, and symptom duration. Since the machine learning model requires all input features, a preprocessing step fills any missing values using predefined default values.

The completed feature vector is then passed to the Random Forest model, which predicts one of four urgency levels:

- Low
- Medium
- High
- Critical

After prediction, deterministic medical guardrails check for emergency conditions such as suspected heart attacks, strokes, severe bleeding, or airway obstruction. These rules override the machine learning prediction whenever necessary to improve patient safety.

Finally, the system retrieves the most relevant medical guideline from a knowledge base and generates a recommendation that is returned together with the predicted urgency level.

---

# Dataset Generation Approach

One of the biggest challenges encountered during the development of this project was the lack of a suitable public dataset. Existing healthcare datasets generally contain only partial information, such as symptoms, diagnoses, or medical history, but none contained all the information required for this project.

The machine learning model required patient demographics, symptoms, medical history, vital signs, symptom duration, and urgency labels within a single dataset. Since such a dataset was not publicly available, a custom synthetic dataset was created.

Initially, patient records were generated using completely random values. However, this approach produced unrealistic combinations of symptoms and vital signs. For example, patients with mild symptoms frequently had critically abnormal vital signs, causing most records to be labeled as **Critical**. This resulted in severe class imbalance and poor-quality training data.

To overcome this problem, the dataset generation strategy was redesigned using a scenario-based approach. Instead of randomly assigning symptoms, each synthetic patient was generated from a predefined medical scenario representing a realistic clinical condition.

Examples of scenarios include:

- Common Cold
- Viral Fever
- Asthma Attack
- COPD Exacerbation
- Heart Attack
- Stroke
- Kidney Disease
- Food Poisoning
- Pregnancy Emergency

Each scenario contains realistic combinations of symptoms, medical history, vital signs, and urgency labels. This approach significantly improved the realism and consistency of the dataset while producing a more balanced distribution of urgency classes.

---

# Dataset Details

The final synthetic dataset contains **1,980 patient records** with **47 columns**. Among these columns, **46 are input features**, while the remaining column represents the target urgency level.

The dataset includes the following categories of information.

## Patient Demographics

- Age
- Gender

## Symptoms

Thirty-one symptom-related features were included, such as:

- Fever
- Cough
- Sore throat
- Chest pain
- Shortness of breath
- Wheezing
- Vomiting
- Abdominal pain
- Confusion
- Severe bleeding
- Blood in urine
- Blood in stool
- Seizure
- Loss of consciousness
- Pregnancy bleeding

## Medical History

The patient's existing medical conditions were also included:

- Diabetes
- Hypertension
- Asthma
- COPD
- Heart disease
- Kidney disease
- Stroke history
- Pregnancy

## Vital Signs

Clinical measurements included:

- Heart rate
- Blood pressure
- Oxygen saturation
- Body temperature
- Respiratory rate

## Symptom Duration

The duration of symptoms was represented as the total number of hours since symptom onset.

## Target Variable

The output label is the patient's urgency level, which consists of four categories:

- Low
- Medium
- High
- Critical

---

# Model Training

Before training the machine learning model, several preprocessing steps were performed. Categorical features such as gender and urgency labels were encoded into numerical values to make them compatible with the learning algorithm.

The dataset was analyzed using Exploratory Data Analysis (EDA) to verify data quality. Missing values and duplicate records were checked, class distributions were examined, and correlations among numerical features were analyzed. Outliers were intentionally retained because extremely abnormal vital signs often represent genuinely severe medical conditions.

Several machine learning algorithms were considered during model development, including:

- Logistic Regression
- Decision Tree
- Random Forest
- XGBoost

Among these models, Random Forest was selected because it provides strong performance on structured tabular datasets, handles nonlinear relationships effectively, and is relatively robust to noisy synthetic data.

The dataset was divided into training and testing sets using an **80:20** split. The Random Forest classifier was trained using the following parameters:

- **Number of Trees (`n_estimators`)**: 200
- **Maximum Tree Depth (`max_depth`)**: 10
- **Minimum Samples Split (`min_samples_split`)**: 5
- **Minimum Samples Leaf (`min_samples_leaf`)**: 2

During training, the model learned relationships between patient symptoms, medical history, vital signs, and urgency levels.

---

# Model Evaluation

After training, the model was evaluated using the unseen testing dataset.

Several evaluation metrics were used to assess model performance:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion Matrix

**Accuracy** measures the overall percentage of correctly classified patient records.

**Precision** evaluates how many predicted urgency labels are correct.

**Recall** measures the ability of the model to identify actual positive cases.

The **F1-score** provides a balanced measure of precision and recall.

The **Confusion Matrix** offers detailed insight into how frequently each urgency class is correctly predicted or confused with other classes.

The trained Random Forest model achieved satisfactory performance for the synthetic dataset and demonstrated its ability to classify patient urgency based on structured medical features.

---

# Structured Patient Risk Prediction

Once the Random Forest model was successfully trained and evaluated, it was integrated into a FastAPI backend to provide real-time predictions.

A REST API endpoint named **`/predict`** was developed to accept structured patient information. The endpoint receives patient demographics, symptoms, medical history, and vital signs in JSON format. The incoming data is first validated using **Pydantic** schemas to ensure correctness and completeness.

The validated data is then passed to the prediction service, which loads the serialized Random Forest model and predicts one of the four urgency levels:

- Low
- Medium
- High
- Critical

The API returns the predicted urgency level as a JSON response, allowing external applications such as web interfaces to consume the prediction service efficiently.

This structured prediction module serves as the foundation for the subsequent free-text triage pipeline, where natural language symptom descriptions are converted into the structured features required by the trained machine learning model.

# Intelligent Text-Based Patient Triage Pipeline

After successfully implementing the structured prediction module, the system was extended to support free-text patient symptom descriptions. This enhancement enables patients to describe their symptoms naturally instead of manually selecting values for all input features.

The objective of this module is to automatically convert unstructured patient descriptions into structured medical features that can be processed by the trained Random Forest model. This significantly improves the usability of the system while maintaining compatibility with the existing machine learning pipeline.

The complete workflow consists of multiple stages including input validation, symptom extraction using a Large Language Model (LLM), feature preprocessing, urgency prediction, and response generation. This enables the system to perform end-to-end patient triage using natural language input.

---

# LLM-Based Feature Extraction

One of the major enhancements in the project is the integration of a Large Language Model (LLM) for extracting structured clinical information from patient descriptions.

The Groq API was integrated using the **Llama-3.1-8B-Instant** model. This model was selected because it provides fast inference while producing consistent outputs suitable for structured data extraction.

The LLM receives the patient's free-text description and converts it into a structured JSON object containing only the supported medical features required by the Random Forest model.

To ensure consistent outputs, the model was configured with a **temperature value of 0**. Using a deterministic temperature prevents the model from producing different outputs for the same patient description, thereby improving the reliability of the prediction pipeline.

### Example

If a patient enters:

> *"I am a 22-year-old female with cough and sore throat. I do not have fever. Symptoms started yesterday."*

The LLM extracts only the explicitly mentioned information:

- Age
- Gender
- Cough
- Sore throat
- Fever
- Symptom duration

The extractor intentionally ignores information that is not explicitly mentioned, avoiding assumptions about symptoms, diseases, or vital signs.

---

# Prompt Engineering

To obtain reliable structured outputs from the LLM, a carefully designed system prompt was created. The prompt instructs the model to behave as a medical symptom extraction assistant rather than a conversational chatbot.

Several constraints were included within the prompt to improve consistency and compatibility with the machine learning model.

The prompt requires the LLM to:

- Return only JSON output.
- Avoid explanations or conversational responses.
- Avoid Markdown formatting.
- Extract only symptoms explicitly mentioned by the patient.
- Avoid assuming diseases or medical history.
- Avoid generating vital signs that are not provided.
- Return only feature names supported by the Random Forest model.

The prompt also defines the encoding rules expected by the machine learning model:

- Binary symptoms are represented using **1** for present and **0** for absent.
- Gender is encoded as **Male = 0** and **Female = 1**.
- Symptom duration is converted into hours.

These rules ensure that the extracted information matches the feature representation used during model training.

---

# Feature Preparation and Random Forest Integration

The Random Forest model was trained using **46 structured input features**. However, patients rarely mention every symptom or clinical parameter when describing their condition.

For example, a patient may simply state:

> *"I have cough."*

In this case, the LLM extracts only the cough feature. Since the Random Forest model requires all 46 features, the extracted information must be converted into a complete feature vector before prediction.

To solve this problem, a preprocessing function named **`prepare_features()`** was implemented.

The function performs three important tasks:

- Creates a copy of the default feature dictionary.
- Updates the dictionary with the values extracted by the LLM.
- Fills all remaining missing features with predefined default values.

A complete **DEFAULT_FEATURES** dictionary was created containing default values for every feature expected by the model. For example, default physiological values such as heart rate, oxygen saturation, temperature, and respiratory rate are assigned when the patient does not explicitly mention them.

This preprocessing step guarantees that every prediction is performed using a complete feature vector, ensuring compatibility with the trained Random Forest model.

After feature preparation, the completed feature vector is passed directly to the Random Forest classifier, which predicts one of four urgency levels:

- Low
- Medium
- High
- Critical

The predicted urgency, together with the extracted features, forms the initial output of the AI triage pipeline.

---

# API Development and Response Generation

To support free-text patient triage, a dedicated FastAPI endpoint was developed. Unlike the structured prediction endpoint, which requires all patient features, the new endpoint accepts only a single text field containing the patient's symptom description.

The endpoint internally performs the following operations:

1. Validate the patient input.
2. Send the validated text to the Groq LLM.
3. Extract structured medical features.
4. Prepare the complete feature vector.
5. Predict the urgency level using the Random Forest model.
6. Return the extracted clinical information along with the predicted urgency.

The API response provides both the urgency level and the structured features extracted from the patient's description. This improves transparency by allowing users to understand how the free-text input was interpreted before prediction.

---

# Guardrails and Input Validation

To improve the reliability and security of the AI system, an input validation layer was introduced before invoking the Large Language Model.

The purpose of this validation layer is to prevent invalid, incomplete, or malicious inputs from reaching the extraction model.

The implemented guardrails perform several validation checks, including:

- Rejecting empty patient descriptions.
- Rejecting extremely short inputs that do not provide meaningful clinical information.
- Rejecting excessively long inputs beyond the configured character limit.
- Detecting prompt injection attempts using regular expression matching.

The system specifically checks for malicious instructions such as:

- "Ignore previous instructions"
- "Always return Critical"
- "Override the system prompt"
- "Pretend to be another model"

If any of these patterns are detected, the request is rejected before reaching the LLM.

By introducing these guardrails, the free-text triage pipeline becomes more reliable, secure, and resistant to prompt injection attacks. The final workflow consists of patient input validation, LLM-based feature extraction, feature preparation, machine learning prediction, and structured response generation, forming a complete AI-powered patient triage pipeline.

# Retrieval-Augmented Generation (RAG) Integration

After completing the free-text patient triage pipeline, the system was further enhanced by integrating a **Retrieval-Augmented Generation (RAG)** module. The primary objective of this enhancement was to provide clinically relevant recommendations in addition to predicting the patient's urgency level. While the machine learning model estimates the urgency of the patient's condition, it does not explain what actions should be taken. The RAG module addresses this limitation by retrieving relevant medical guidelines from a predefined knowledge base.

Once the patient's symptoms are extracted and the urgency level is predicted, the system searches the knowledge base for guidelines that match the predicted condition and clinical features. The retrieved information is then used to generate a recommendation that supports healthcare professionals in making informed decisions. This enhancement makes the system more useful by combining machine learning predictions with evidence-based medical guidance.

The updated workflow consists of the following stages:

1. Input validation
2. LLM-based feature extraction
3. Feature preparation
4. Random Forest prediction
5. Guardrail verification
6. Guideline retrieval
7. Recommendation generation
8. Returning the final response to the user

---

# Deterministic Medical Guardrails

Although the Random Forest model provides reliable predictions, machine learning models may occasionally underestimate the severity of certain medical conditions. To improve patient safety, a deterministic guardrail layer was introduced after the prediction stage.

The guardrail module contains predefined medical rules that automatically upgrade the predicted urgency whenever critical clinical conditions are detected. These rules are based on common emergency scenarios where immediate medical attention is required regardless of the machine learning prediction.

Critical conditions handled by the guardrails include:

- Suspected heart attacks
- Stroke symptoms
- Loss of consciousness
- Seizures
- Severe bleeding
- Airway obstruction
- Pregnancy-related bleeding
- Suicidal thoughts
- Dangerously low oxygen saturation levels

Similarly, high-risk situations such as the following are automatically upgraded to a **High** urgency level:

- Kidney disease with blood in the urine
- Asthma attacks
- COPD exacerbations
- Burns
- Fractures
- Fever with breathing difficulty
- Abnormal vital signs

By combining machine learning with deterministic medical rules, the system minimizes the possibility of underestimating severe patient conditions and improves the overall safety and reliability of the triage process.

---

# Frontend Development

To provide an interactive interface for users, a complete web application was developed using **HTML, CSS, and JavaScript**. A lightweight frontend was chosen instead of modern JavaScript frameworks to simplify deployment and reduce system complexity.

The application consists of three main pages:

- **Home Page** – Serves as the entry point and allows users to choose between structured patient prediction and AI-based free-text intake.
- **Structured Prediction Page** – Enables users to manually enter patient demographics, symptoms, medical history, and optional vital signs. A searchable symptom selector was implemented to improve usability and make symptom selection faster.
- **AI Intake Page** – Allows patients to describe their symptoms using natural language.

The entered text is sent directly to the backend, where it undergoes:

1. Input validation
2. Feature extraction
3. Urgency prediction
4. Guardrail verification
5. Recommendation generation

The final output displayed on the interface includes:

- Predicted urgency level
- Extracted clinical features
- Retrieved medical recommendation
- Supporting medical guideline
- Guideline source

This provides users with a transparent and easy-to-understand representation of the system's decision.

---

# Frontend–Backend Integration

The frontend communicates with the FastAPI backend through RESTful APIs using the JavaScript **Fetch API**. Two separate endpoints were developed to support different modes of operation.

### Structured Prediction Endpoint

The **`/predict`** endpoint accepts structured patient information collected through the prediction form and returns the predicted urgency level.

### AI Intake Endpoint

The **`/intake`** endpoint accepts free-text patient descriptions and performs the following operations:

1. LLM-based symptom extraction
2. Feature preparation
3. Random Forest prediction
4. Medical guardrail verification
5. Medical guideline retrieval
6. Recommendation generation

The endpoint returns the complete prediction result to the frontend.

During integration, **Cross-Origin Resource Sharing (CORS)** restrictions prevented the frontend from accessing the backend APIs. This issue was resolved by configuring FastAPI's **CORSMiddleware**, allowing secure communication between the frontend development server and the backend application.

After configuring CORS, both interfaces successfully communicated with the backend and displayed real-time prediction results.

---

# End-to-End System Workflow

The final AI-powered Patient Triage and Risk Assessment Assistant integrates machine learning, large language models, deterministic medical rules, retrieval-based recommendations, and a web interface into a single workflow.

The complete workflow is as follows:

1. The patient submits either structured information or a free-text symptom description.
2. The input passes through validation and security checks to prevent invalid or malicious requests.
3. For free-text inputs, the Groq LLM extracts structured medical features.
4. The feature preparation module completes the feature vector required by the Random Forest model.
5. The Random Forest classifier predicts the patient's urgency level.
6. The medical guardrail module verifies whether any emergency conditions require overriding the prediction.
7. The RAG module retrieves the most relevant medical guideline and generates a recommendation based on the patient's condition.
8. The final response, including the predicted urgency, extracted clinical features, recommendation, and supporting guideline, is returned to the frontend and displayed to the user.

This integrated workflow enables the system to automatically process patient descriptions, prioritize cases according to severity, provide guideline-based recommendations, and present the results through a simple and user-friendly web interface.