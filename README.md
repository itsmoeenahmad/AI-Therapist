# AI Therapist

A mental health support chatbot built with FastAPI, LangGraph, and Groq. It provides therapeutic conversations, finds nearby therapists, and can trigger emergency calls when it detects crisis situations.

This is a learning project. The code is intentionally kept readable over being clever.

---

## What It Does

- Responds to mental health queries using a Groq-hosted LLM (Llama 3.3 70B)
- Remembers conversation history per session (stored in MongoDB)
- Finds therapists by generating Psychology Today search links
- Calls a configured phone number during crisis situations via Twilio

---

## How the Agent Works

The core of this project is a LangGraph ReAct agent. ReAct stands for "Reason and Act" - the LLM thinks about what to do, calls a tool if needed, then formulates a response.

Here is the execution flow:

```
User sends message
       |
       v
+------------------+
|   Agent Node     |  LLM reads the message + system prompt
|   (LLM thinks)   |  Decides: answer directly OR call a tool
+------------------+
       |
       v (if tool needed)
+------------------+
|   Tools Node     |  Executes the Python function
|   (runs code)    |  Returns result to agent
+------------------+
       |
       v
+------------------+
|   Agent Node     |  LLM reads tool output
|   (LLM responds) |  Generates final response for user
+------------------+
       |
       v
Response returned to API
```

The agent has access to three tools:

| Tool | What It Does |
|------|--------------|
| `ask_mental_health_specialist` | Calls Groq with a therapy-focused prompt |
| `find_nearby_therapists_by_location` | Returns a Psychology Today search link |
| `emergency_call_tool` | Triggers a Twilio call with a spoken message |

The LLM decides which tool to call based on the user input and system prompt. For normal queries, it uses the therapy tool. For location requests like "find a therapist in NYC", it uses the location tool. For crisis messages, it uses the emergency tool.

---

## Project Structure

```
ai-therapist/
├── .env.example              # Environment variables template
│
├── backend/
│   ├── Dockerfile            # For container deployment
│   ├── requirements.txt
│   ├── main.py               # FastAPI app entry point
│   └── app/
│       ├── api/
│       │   ├── routes.py     # POST /ask, GET /health
│       │   └── schemas.py    # Request/response models
│       ├── core/
│       │   ├── agent.py      # LangGraph agent setup
│       │   ├── config.py     # Loads env vars
│       │   └── prompts.py    # System prompts
│       └── services/
│           ├── database.py   # MongoDB read/write
│           ├── therapy.py    # Groq API call
│           ├── emergency.py  # Twilio call logic
│           └── location.py   # Psychology Today link
│
└── frontend/
    ├── requirements.txt
    └── frontend.py           # Streamlit chat UI
```

---

## Setup

### Requirements

- Python 3.12+
- Groq API key (free at console.groq.com)
- MongoDB Atlas cluster (free tier works)
- Twilio account (optional, for emergency calls)

### Install

```bash
git clone https://github.com/yourusername/ai-therapist.git
cd ai-therapist

# Copy and edit environment variables
cp .env.example .env

# Backend
cd backend
pip install -r requirements.txt

# Frontend (separate terminal)
cd ../frontend
pip install -r requirements.txt
```

### Environment Variables

```env
# Required
GROQ_API_KEY=gsk_xxxxx
MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net/
MONGO_DB_NAME=ai_therapist
MONGO_CHAT_COLLECTION=chats

# Optional (for emergency calling)
TWILIO_ACCOUNT_SID=ACxxxxx
TWILIO_AUTH_TOKEN=xxxxx
TWILIO_FROM_NUMBER=+1234567890
EMERGENCY_CONTACT=+1234567890

# Optional
THERAPEUTIC_MODEL=llama-3.3-70b-versatile
THERAPEUTIC_TEMPERATURE=0.7
```

---

## Running Locally

Terminal 1 (backend):
```bash
cd backend
uvicorn main:app --reload
# Runs on http://localhost:8000
```

Terminal 2 (frontend):
```bash
cd frontend
streamlit run frontend.py
# Opens http://localhost:8501
```

---

## API

### POST /ask

Send a message and get a response.

Request:
```json
{
  "message": "I've been feeling anxious lately",
  "user_id": "some-uuid"
}
```

Response:
```json
{
  "response": "I hear you. Anxiety can be really difficult...",
  "tool_called": "ask_mental_health_specialist",
  "status": "success"
}
```

### GET /health

Returns service status and config validation.

---

## Deployment

### Backend on Koyeb

1. Push to GitHub
2. Create app on koyeb.com
3. Select Dockerfile builder
4. Set:
   - Dockerfile location: `backend/Dockerfile`
   - Work directory: `backend`
   - Port: `8000`
5. Add environment variables
6. Deploy

### Frontend on Streamlit Cloud

1. Go to share.streamlit.io
2. Connect your repo
3. Set main file: `frontend/frontend.py`
4. Add secret: `BACKEND_URL = "https://your-app.koyeb.app/ask"`
5. Deploy

---

## How Conversation History Works

Each browser session gets a UUID (generated on first message). This ID is sent with every request.

On the backend:
1. `get_chat_history(user_id)` fetches last 20 messages from MongoDB
2. History is formatted and prepended to the current message
3. Agent processes with full context
4. Response is saved via `save_message(user_id, human, assistant)`

The agent sees something like:
```
Previous conversation:
User: I've been stressed
Assistant: I understand. What's been causing the stress?

Current message: It's work related
```

---

## The Agent Code Explained

In `backend/app/core/agent.py`:

```python
# Tools are regular Python functions with @tool decorator
@tool
def ask_mental_health_specialist(query: str) -> str:
    return query_therapeutic_model(query)

# LLM setup
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3, api_key=GROQ_API_KEY)

# Create the agent graph
graph = create_react_agent(llm, tools, prompt=AGENT_PROMPT)
```

The `run_agent()` function:
1. Builds the input with optional context
2. Streams execution through the graph
3. Captures which tool was called
4. Captures the final response text
5. Returns both to the API

Streaming lets us see each step (agent thinking, tool executing, agent responding).

---

## Limitations

- Not a real therapist. Cannot diagnose or prescribe.
- Context window is limited. Very long conversations may lose early context.
- Emergency detection relies on LLM judgment - not foolproof.
- Twilio free tier has limitations on call duration and numbers.

---

## Crisis Resources

If you or someone you know is in crisis:

| Country | Service | Number |
|---------|---------|--------|
| USA | Suicide & Crisis Lifeline | 988 |
| UK | Samaritans | 116 123 |
| India | iCall | 9152987821 |
| Australia | Lifeline | 13 11 14 |
| Canada | Crisis Services | 1-833-456-4566 |

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI |
| Agent | LangGraph (ReAct pattern) |
| LLM | Groq (Llama 3.3 70B) |
| Database | MongoDB Atlas |
| Frontend | Streamlit |
| Calls | Twilio |

---

## Disclaimer

This is an educational project. It is not a substitute for professional mental health care. The AI cannot diagnose conditions or provide medical advice. If you are struggling, please reach out to a licensed professional or crisis service.

---

## License

MIT. Use responsibly.
