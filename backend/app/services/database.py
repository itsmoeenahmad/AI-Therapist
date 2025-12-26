from datetime import datetime
from typing import List, Dict
from pymongo import MongoClient, ASCENDING
from app.core.config import MONGODB_URL, MONGO_DB_NAME, MONGO_CHAT_COLLECTION

client = MongoClient(MONGODB_URL)
db = client[MONGO_DB_NAME]
chat_collection = db[MONGO_CHAT_COLLECTION]


def save_message(user_id: str, human: str, assistant: str) -> None:
    """Save a conversation message to MongoDB."""
    item = {
        "user_id": user_id,
        "human": human,
        "assistant": assistant,
        "timestamp": datetime.utcnow()
    }
    chat_collection.insert_one(item)
    print(f"[DB] Saved message for user: {user_id}")


def get_chat_history(user_id: str, limit: int = 20) -> List[Dict[str, str]]:
    """Retrieve chat history for a user from MongoDB."""
    cursor = chat_collection.find({"user_id": user_id}).sort("timestamp", ASCENDING).limit(limit)
    history = []
    for doc in cursor:
        history.append({"human": doc["human"], "assistant": doc["assistant"]})
    return history


def format_history_for_agent(history: List[Dict[str, str]]) -> str:
    """Format chat history as context string for the agent."""
    if not history:
        return ""
    
    formatted = "Previous conversation:\n"
    for msg in history:
        formatted += f"User: {msg['human']}\nAssistant: {msg['assistant']}\n\n"
    return formatted
