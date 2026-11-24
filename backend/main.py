
from fastapi import FastAPI

from backend.routers.auth import router as auth_router
from backend.routers.resume import router as resume_router
from backend.models.candidate import Candidate
from backend.database import Base, engine

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="HireMatrix API",
    description="AI-Driven Smart Hiring Platform with Candidate Matching Copilot",
    version="1.0.0"
)

# Register authentication endpoints
app.include_router(auth_router)
app.include_router(resume_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to HireMatrix!",
        "status": "Backend is running successfully"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "HireMatrix"
    }
