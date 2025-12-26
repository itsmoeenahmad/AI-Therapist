from fastapi import APIRouter, HTTPException

from app.api.schemas import QueryRequest, TherapyResponse, HealthResponse
from app.core.config import APP_NAME, APP_VERSION, validate_config
from app.core.agent import run_agent
from app.services.database import save_message, get_chat_history, format_history_for_agent

router = APIRouter()


@router.get("/")
async def root():
    """Root endpoint with API info."""
    return {"message": f"Welcome to {APP_NAME}", "version": APP_VERSION, "docs": "/docs"}


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for monitoring."""
    config = validate_config()
    return HealthResponse(
        status="healthy",
        app_name=APP_NAME,
        version=APP_VERSION,
        config_valid=config["valid"],
        missing_config=config.get("missing_required", [])
    )


@router.post("/ask", response_model=TherapyResponse)
async def ask(query: QueryRequest):
    """Main therapeutic conversation endpoint."""
    try:
        history = get_chat_history(query.user_id)
        context = format_history_for_agent(history)
        
        tool_called, response = run_agent(query.message, context)
        
        if not response:
            response = "I'm here to listen. Could you tell me more about what's on your mind?"
        
        save_message(query.user_id, query.message, response)
        
        return TherapyResponse(response=response, tool_called=tool_called)
        
    except Exception as e:
        print(f"[ERROR] /ask: {e}")
        raise HTTPException(status_code=500, detail="Service temporarily unavailable. Please try again.")
