from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    sessionId: Optional[str] = None

class ChatLogOut(BaseModel):
    id: int
    user_question: str
    bot_answer: str
    additional_info: Optional[str]
    timestamp: datetime

class Config:
    orm_mode = True

class ChatResponse(BaseModel):
    reply: str
    saved: bool = False
    message: Optional[ChatLogOut] = None