from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.schemas.chatLog_schema import ChatRequest, ChatResponse
from app.core.database import get_db
from app.models.chatLog import ChatLog
from app.service.chatLog_service import generate_reply

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/api/chat/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    print("1", ChatRequest)
    try:
        # user message save
        user_msg = ChatLog(content=request.message, user_role="user", timestamp=func.now())

        db.add(user_msg)
        db.commit()
        db.refresh(user_msg)

        print("1", user_msg)
        # generate bot reply
        reply_text = await generate_reply(request.message, session_id=request.sessionId)
        print("2", reply_text)
        # bot message save
        bot_msg = ChatLog(content=reply_text, user_role="bot", timestamp=func.now())
        db.add(bot_msg)
        db.commit()
        db.refresh(bot_msg)

        # return response
        return ChatResponse(reply=reply_text, saved=True)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
