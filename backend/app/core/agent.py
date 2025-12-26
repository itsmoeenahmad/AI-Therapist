from typing import Tuple, Optional
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

from app.core.config import GROQ_API_KEY
from app.core.prompts import AGENT_PROMPT
from app.services.therapy import query_therapeutic_model
from app.services.emergency import call_emergency
from app.services.location import find_therapists


@tool
def ask_mental_health_specialist(query: str) -> str:
    """Generate therapeutic response for mental health queries."""
    return query_therapeutic_model(query)


@tool
def emergency_call_tool() -> str:
    """Place emergency call for crisis situations only."""
    return call_emergency()


@tool
def find_nearby_therapists_by_location(location: str) -> str:
    """Find licensed therapists near the specified location."""
    return find_therapists(location)


# Initialize LLM and tools
tools = [ask_mental_health_specialist, emergency_call_tool, find_nearby_therapists_by_location]

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3,
    api_key=GROQ_API_KEY
)

# Create agent with system prompt
graph = create_react_agent(llm, tools, prompt=AGENT_PROMPT)


def run_agent(user_input: str, context: str = "") -> Tuple[str, Optional[str]]:
    """Run agent and return tool called and final response."""
    try:
        full_input = f"{context}Current message: {user_input}" if context else user_input
        inputs = {"messages": [("user", full_input)]}
        config = {"recursion_limit": 10}
        
        tool_called = "None"
        response = None
        
        for chunk in graph.stream(inputs, config=config, stream_mode="updates"):
            for node, updates in chunk.items():
                if node == "tools":
                    for msg in updates.get("messages", []):
                        if hasattr(msg, 'name'):
                            tool_called = msg.name
                elif node == "agent":
                    for msg in updates.get("messages", []):
                        if hasattr(msg, 'content') and msg.content:
                            response = msg.content
        
        return tool_called, response or "I'm here to help. Could you tell me more?"
    except Exception as e:
        print(f"[ERROR] Agent error: {e}")
        return "None", "I'm experiencing difficulties. Please try again."
