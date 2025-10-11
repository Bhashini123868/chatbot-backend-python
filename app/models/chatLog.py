from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.core.database import Base


class ChatLog(Base):
    __tablename__ = "chat_log"

    id = Column(Integer, primary_key=True, index=True)
    user_question = Column(Text, nullable=False)
    bot_answer = Column(Text, nullable=False)
    additional_info = Column(Text, nullable=True)
    timestamp = Column(DateTime, server_default=func.now(), nullable=False)
