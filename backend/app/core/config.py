import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root (parent of backend folder)
env_path = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(env_path)


# Twilio configuration for emergency calls
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER", "")
EMERGENCY_CONTACT = os.getenv("EMERGENCY_CONTACT", "")

# Groq API for LLM services
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
THERAPEUTIC_MODEL = os.getenv("THERAPEUTIC_MODEL", "llama-3.3-70b-versatile")
THERAPEUTIC_TEMPERATURE = float(os.getenv("THERAPEUTIC_TEMPERATURE", "0.7"))

# MongoDB configuration
MONGODB_URL = os.getenv("MONGODB_URL", "")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "ai_therapist")
MONGO_CHAT_COLLECTION = os.getenv("MONGO_CHAT_COLLECTION", "chats")

# App settings
APP_NAME = "AI Therapist"
APP_VERSION = "1.0.0"
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"

def validate_config() -> dict:
    """Check if required environment variables are set."""
    required = {"GROQ_API_KEY": GROQ_API_KEY}
    optional = {
        "TWILIO_ACCOUNT_SID": TWILIO_ACCOUNT_SID,
        "TWILIO_AUTH_TOKEN": TWILIO_AUTH_TOKEN,
        "TWILIO_FROM_NUMBER": TWILIO_FROM_NUMBER,
        "EMERGENCY_CONTACT": EMERGENCY_CONTACT,
    }
    
    missing_required = [k for k, v in required.items() if not v]
    missing_optional = [k for k, v in optional.items() if not v]
    
    return {
        "valid": len(missing_required) == 0,
        "missing_required": missing_required,
        "missing_optional": missing_optional
    }
