from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.core.config import APP_NAME, APP_VERSION, validate_config


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown."""
    # Startup
    print(f"\n{'='*50}")
    print(f"{APP_NAME} v{APP_VERSION}")
    print(f"{'='*50}")
    
    config = validate_config()
    if not config["valid"]:
        print(f"WARNING: Missing required config: {config['missing_required']}")
    if config.get("missing_optional"):
        print(f"Optional config not set: {config['missing_optional']}")
    
    print("Server started - API docs: http://localhost:8000/docs")
    print(f"{'='*50}\n")
    
    yield
    
    # Shutdown
    print("Server shutting down...")


# Initialize FastAPI app with lifespan
app = FastAPI(
    title=APP_NAME,
    description="AI-powered mental health support system",
    version=APP_VERSION,
    docs_url="/docs",
    lifespan=lifespan
)

# CORS middleware for frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
