from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session as DBSession
from app.core.database import get_db
from app.schemas.session import SessionCreate, SessionResponse
from app.service.session_service import SessionService, get_session_service

router = APIRouter(prefix="/api/session", tags=["Session"])

@router.post("/create", response_model=SessionResponse)
async def create_session(
        request: Request,
        db:DBSession = Depends(get_db)
):
    session_service = SessionService(db)

    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")


    new_session = session_service.create_session(ip_address,user_agent)

    return new_session