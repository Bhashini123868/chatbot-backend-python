# app/agent/tools/sql_query_tool.py
import re
import traceback
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
from app.agent.llm_manager import get_llm
from sqlalchemy import text
from app.core.database import SessionLocal

# adjust this schema description to match real column names
DB_SCHEMA_DESCRIPTION = """
Database schema (relevant tables):
- chat_log(chat_log_id, session_id, sender, content, message_metadata, created_at)
- customer_log(customer_id, customer_name, ... )  # adjust columns if different
- item_log(item_id, item_name, unit_price, quantity_in_stock, ...)
- order_detail(order_detail_id, order_id, item_id, qty, price, ...)
- sessions(session_id, ip_address, user_agent, created_at)
"""

# simple function to extract a plausible SQL query from LLM output
def extract_sql_from_text(text: str) -> str | None:
    # try to find the first block that looks like a SQL statement
    # match lines that start with SELECT/INSERT/UPDATE/DELETE (case-insensitive)
    m = re.search(r"(?i)(select|insert|update|delete)\b.*", text, re.DOTALL)
    if not m:
        return None
    sql = text[m.start():].strip()
    # remove any trailing explanation after a semicolon if present (keep only first statement)
    if ";" in sql:
        sql = sql.split(";")[0] + ";"
    # basic sanitation: disallow dangerous statements like DROP, ALTER
    if re.search(r"(?i)\b(drop|alter|truncate|create)\b", sql):
        return None
    return sql

@tool
def sql_query_tool(user_query: str) -> str:
    """
    Generate and execute a SQL query from user natural-language query.
    Returns a plain-text friendly answer (not raw SQL) or an error message.
    """
    # Step 1: ask LLM to generate SQL
    try:
        system_message = (
            "You are an expert SQL generator for this application's database.\n"
            "Given the user's natural language request, output ONLY a single valid SQL query (MySQL syntax) "
            "that answers the request. Do NOT include explanations or any surrounding text — only the SQL.\n\n"
            f"{DB_SCHEMA_DESCRIPTION}\n\n"
            "Rules:\n"
            "- Use the exact table and column names from the schema above.\n"
            "- Output only one SQL statement (ideally a SELECT for read requests).\n"
            "- Never output DDL or destructive statements (DROP/ALTER/TRUNCATE).\n"
            "- If the request cannot be answered with the data available, respond with exactly: NO_SQL_POSSIBLE\n"
        )

        llm = get_llm(temperature=0)
        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=user_query)
        ]
        response = llm.invoke(messages)
        generated_text = response.content.strip()
        print("LLM raw output:\n", generated_text)
        sql_query = extract_sql_from_text(generated_text)

        if not sql_query:
            # maybe LLM followed instruction but added extra text — check for NO_SQL_POSSIBLE token
            if "NO_SQL_POSSIBLE" in generated_text:
                return "No relevant data available to answer that question from the database."
            return "The LLM did not produce a valid SELECT/INSERT/UPDATE/DELETE SQL statement."

    except Exception as e:
        print("Error generating SQL:", traceback.format_exc())
        return f"Error generating query: {e}"

    # Step 2: execute the SQL safely
    session = SessionLocal()
    try:
        print("Executing SQL:", sql_query)
        result = session.execute(text(sql_query))

        if sql_query.strip().lower().startswith("select"):
            rows = result.fetchall()
            keys = result.keys()
            data = [dict(zip(keys, row)) for row in rows]
            print("Query returned rows:", len(data))

            if not data:
                return "No data found 😕"

            # simple pretty text conversion (CSV-like or bullet list)
            lines = []
            # show up to e.g. 10 rows to avoid huge responses
            for row in data[:10]:
                parts = [f"{k}: {row[k]}" for k in row.keys()]
                lines.append(" | ".join(parts))
            if len(data) > 10:
                lines.append(f"...and {len(data)-10} more rows.")

            plain_result = "\n".join(lines)

            # Optional: ask LLM to format the result as user-friendly answer (commented out if you don't want second LLM call)
            try:
                # second LLM to create a friendly answer
                system_message2 = (
                    "You are a friendly assistant. Given the user question and SQL results (as JSON-like list), "
                    "produce a concise, user-friendly answer (3-8 bullets). Use emojis and short notes for low stock/high balance.\n"
                    "If numeric thresholds are needed, treat quantity_in_stock <= 20 as low stock."
                )
                llm2 = get_llm(temperature=0.7)
                messages2 = [
                    SystemMessage(content=system_message2),
                    HumanMessage(content=f"User question: {user_query}\n\nSQL result: {data}")
                ]
                response2 = llm2.invoke(messages2)
                return response2.content
            except Exception as e:
                # if second LLM call fails, fallback to plain text
                print("Second LLM formatting failed:", traceback.format_exc())
                return plain_result

        else:
            # non-SELECT (insert/update/delete) - commit
            session.commit()
            return "Query executed successfully."

    except Exception as e:
        session.rollback()
        print("SQL execution error:", traceback.format_exc())
        return f"Error executing query: {e}"

    finally:
        session.close()
