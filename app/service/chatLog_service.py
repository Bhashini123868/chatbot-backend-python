from sqlalchemy.orm import Session
from datetime import datetime

from app.models.chatLog import ChatLog
from app.schemas.chatLog_schema import chatLogResponse
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from app.core.config import settings


prompt = PromptTemplate(
    input_variables=["message"],
    template="You are a helpful assistant. Answer the following question: {message}"
)

llm = ChatOpenAI(
    api_key=settings.OPEN_API_KEY,   
    model="gpt-3.5-turbo"
)


def generate_reply(message: str) -> str:
    """
    Use LangChain + OpenAI to generate a reply for given message
    """
    chain = prompt | llm   
    response = chain.invoke({"message": message})
    return response.content


def save_chat_log(db: Session, user_question: str, bot_answer: str) -> chatLogResponse:
    chat_entry = ChatLog(
        user_question=user_question,
        bot_answer=bot_answer,
        timestamp=datetime.utcnow()
    )
    db.add(chat_entry)
    db.commit()
    db.refresh(chat_entry)
    return chatLogResponse.from_orm(chat_entry)

def ask_and_log(db: Session, message: str) -> chatLogResponse:
    """
    Generate AI response for user question and save to DB.
    """
    bot_answer = generate_reply(message)
    return save_chat_log(db, message, bot_answer)
