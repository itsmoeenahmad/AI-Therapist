from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """Request model for therapeutic conversation."""
    message: str = Field(..., min_length=1, max_length=5000)
    user_id: str = Field(..., min_length=1)


class TherapyResponse(BaseModel):
    """Response model for therapeutic conversation."""
    response: str
    tool_called: str
    status: str = "success"


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    status: str
    app_name: str
    version: str
    config_valid: bool
    missing_config: list
