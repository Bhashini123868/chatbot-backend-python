from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.core.database import Base


class ChatLog(Base):
    __tablename__ = "chat_log"

    id = Column(Integer, primary_key=True, index=True)
    user_role = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<ChatMessage {self.id} - {self.user_role}>"

