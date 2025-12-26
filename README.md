# AI Therapist

An AI-powered mental health support system providing therapeutic conversations, crisis detection, therapist location services, and persistent conversation history.

---

## Features

| Feature | Description |
|---------|-------------|
| Therapeutic Conversations | Evidence-based responses using CBT, DBT, and person-centered therapy |
| Conversation History | MongoDB-backed chat persistence with unique user sessions |
| Find Therapists | Locate mental health professionals via Psychology Today directory |
| Emergency Calling | Crisis detection with automatic emergency call via Twilio (with voice message) |
| Simple UI | Clean Streamlit chat interface |

---

## Architecture

```
User Input --> Streamlit Frontend --> FastAPI Backend --> LangGraph Agent
                    |                       |                    |
               [UUID Session]          [MongoDB]    +------------+------------+
                                                    |            |            |
                                              Therapy Tool  Location Tool  Emergency Tool
                                              (Groq API)   (Psychology Today)  (Twilio)
```

---

## Project Structure

```
ai-therapist/
├── .env                          # Environment variables
├── README.md                     # This documentation
├── requirements.txt              # Python dependencies
├── pyproject.toml               # Project metadata
│
├── backend/
│   ├── main.py                  # FastAPI entry point
│   └── app/
│       ├── api/
│       │   ├── routes.py        # API endpoints (/ask, /health)
│       │   └── schemas.py       # Pydantic request/response models
│       ├── core/
│       │   ├── agent.py         # LangGraph ReAct agent with tools
│       │   ├── config.py        # Environment variables and settings
│       │   └── prompts.py       # System prompts for AI models
│       └── services/
│           ├── database.py      # MongoDB chat history storage
│           ├── therapy.py       # Groq API therapeutic responses
│           ├── emergency.py     # Twilio emergency calling with TwiML
│           └── location.py      # Psychology Today therapist search
│
└── frontend/
    └── frontend.py              # Streamlit chat interface
```

---

## Installation

### Prerequisites
- Python 3.13+
- Groq API Key (free at https://console.groq.com/keys)
- MongoDB Atlas account (free tier available)

### Setup

1. Clone and navigate to project:
```bash
cd "ai therapist"
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables in `.env`:
```env
# Required
GROQ_API_KEY=your_groq_api_key_here

# MongoDB (Required)
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
MONGO_DB_NAME=ai_therapist
MONGO_CHAT_COLLECTION=chats

# Optional - Twilio for emergency calling
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_FROM_NUMBER=+1234567890
EMERGENCY_CONTACT=+1234567890

# Optional - Model settings
THERAPEUTIC_MODEL=llama-3.3-70b-versatile
THERAPEUTIC_TEMPERATURE=0.7
```

---

## Running the Application

### Start Backend Server
```bash
cd backend
uvicorn main:app --reload
# Server runs at http://localhost:8000
# API docs at http://localhost:8000/docs
```

### Start Frontend (new terminal)
```bash
cd frontend
streamlit run frontend.py
# UI opens at http://localhost:8501
```

---

## API Reference

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message and API info |
| GET | `/health` | Health check and config validation |
| POST | `/ask` | Main therapeutic conversation |
| GET | `/docs` | Interactive API documentation |

### Request Example
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"message": "I have been feeling anxious about work", "user_id": "your-unique-uuid"}'
```

### Response Example
```json
{
  "response": "I hear that work has been causing you anxiety...",
  "tool_called": "ask_mental_health_specialist",
  "status": "success"
}
```

---

## AI Agent Tools

The LangGraph agent has access to three tools:

### 1. ask_mental_health_specialist
- Primary tool for all emotional/psychological queries
- Uses Groq API with therapeutic system prompt
- Integrates CBT, DBT, and person-centered therapy approaches

### 2. find_nearby_therapists_by_location
- Generates Psychology Today search link for the specified location
- Users can browse verified therapists with credentials, specialties, and contact info
- Free to use, no API key required

### 3. emergency_call_tool
- Triggered for crisis situations (suicidal ideation, self-harm)
- Places emergency call to configured contact via Twilio
- Speaks urgent message when call is answered using TwiML
- Falls back to crisis helpline numbers if Twilio not configured

---

## Conversation History

Each user session gets a unique UUID that persists during the browser session. All messages are stored in MongoDB with:

- `user_id` - Unique session identifier
- `human` - User's message
- `assistant` - AI's response
- `timestamp` - When the message was sent

The agent receives previous conversation context to maintain continuity.

---

## Therapeutic Approach

The AI therapist (Dr. Emily) follows evidence-based practices:

**Response Guidelines:**
1. Acknowledge and validate feelings first
2. Normalize the experience when appropriate
3. Ask open-ended questions to explore root causes
4. Offer evidence-based coping strategies
5. Highlight strengths and resilience

**Safety Principles:**
- Never diagnoses conditions or recommends medications
- Encourages professional help for serious concerns
- Takes self-harm/suicidal ideation seriously
- Maintains warm, professional boundaries

---

## Crisis Resources

| Country | Helpline | Number |
|---------|----------|--------|
| USA | Suicide & Crisis Lifeline | 988 |
| UK | Samaritans | 116 123 |
| India | iCall | 9152987821 |
| Australia | Lifeline | 13 11 14 |
| Canada | Crisis Services | 1-833-456-4566 |

---

## Disclaimer

This is an AI support tool and does not replace professional mental health care. The AI:
- Does not diagnose mental health conditions
- Does not provide medical advice or medication recommendations
- Should not be used as a substitute for licensed therapy

For serious mental health concerns, please consult a licensed professional. If you are in crisis, contact emergency services immediately.

---

## License

For educational and personal use only. Please use responsibly.
