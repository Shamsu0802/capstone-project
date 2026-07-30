import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router

# -----------------------------------------
# Configure Logging
# -----------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)

logger.info("Starting AI Patient Triage & Risk Assessment API...")

# -----------------------------------------
# Create FastAPI App
# -----------------------------------------
app = FastAPI(
    title="AI Patient Triage & Risk Assessment API",
    version="1.0.0",
    description="""
AI-powered patient triage system.

Features:
- LLM-based symptom extraction
- Random Forest urgency prediction
- FastAPI backend
"""
)

# -----------------------------------------
# Enable CORS
# -----------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------
# Register Routes
# -----------------------------------------
app.include_router(router)

logger.info("API routes registered successfully.")

# -----------------------------------------
# Home Endpoint
# -----------------------------------------
@app.get("/")
def home():
    logger.info("Health check endpoint '/' accessed.")

    return {
        "message": "AI Patient Triage & Risk Assessment API is running successfully."
    }