from langchain_openai import ChatOpenAI
from app.core.config import settings

def get_llm():
    return ChatOpenAI(
        openai_api_key=settings.OPENAI_API_KEY,
        model_name="gpt-3.5-turbo",
        temperature=0,
    )