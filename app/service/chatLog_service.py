import sys

from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from app.agent.query_service import handle_sql_queries
from app.core.config import settings

prompt = PromptTemplate(
    input_variables=["message"],
    template="You are a helpful assistant. Answer the following question: {message}"
)

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.8,
    openai_api_key= settings.OPENAI_API_KEY,

)

async def generate_reply(message: str, session_id: str = None) -> str:
    print("1",message)
    try:
        keyword = ["data", "records", "show", "list", "how many", "count", "sum", "average"]

        if any(kw in message.lower() for kw in keyword):
            sql_response = await handle_sql_queries(message)
            print("2",sql_response)
            if "reply" in sql_response:
                return sql_response["reply"]
            else:
                return f"Error: {sql_response['error']}"

        chain = LLMChain(llm=llm, prompt=prompt)
        print("3",LLMChain)
        return chain.run(message)
    except:
        return f"Error: {sys.exc_info()[0]}"
