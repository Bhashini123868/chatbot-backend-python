from typing import TypedDict

from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    messages: list[BaseMessage]
    user_quary: str
    decision: str
    reply: str