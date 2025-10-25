import traceback

from app.agent.agent_state import AgentState
from app.agent.tools.sql_query_tool import sql_query_tool

def tool_caller_node(state: AgentState) -> AgentState:
    try:
        decision = state.get("reply", "").strip().lower()
        query = state.get("user_query")

        if decision == "database_query_tool":
            result = sql_query_tool(query)

            if decision == "database_query_tool":
                result = sql_query_tool(query)
                state["reply"] = result
            else:
                state["reply"] = "Unknown tool decison."

    except Exception as e:
        print(traceback.format_exc())

    return state

