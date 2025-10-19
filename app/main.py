from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.chatRoutes import router as chat_router
from app.api.routes.session import router as session_router

from dotenv import load_dotenv

from app.core.config import settings

load_dotenv()
app = FastAPI(
    title="ChatBot Assistant Service",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include API routes
app.include_router(chat_router)
app.include_router(session_router)

@app.get("/")
def root():
    return {"status": "ok", "message": "Hello, World!"}
