# TOOL_NAME = "Database"
# TOOL_DESCRIPTION = "Convert natural language to SQL and run it on PostgreSQL to get data from tables"

# import sys
# import json
# import os
# import psycopg2
# from openai import OpenAI
# from dotenv import load_dotenv

# load_dotenv()

# # DB credentials
# DB_HOST = os.getenv("PG_HOST")
# DB_PORT = os.getenv("PG_PORT")
# DB_NAME = os.getenv("PG_DB")
# DB_USER = os.getenv("PG_USER")
# DB_PASS = os.getenv("PG_PASSWORD")
# DB_SSLMODE = "require"

# llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ALLOWED_COMMANDS = ("SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "DROP", "ALTER", "TRUNCATE", "WITH")


# def execute(input_data):
#     question = input_data.get("text", "")

#     conn = psycopg2.connect(
#         host=DB_HOST,
#         port=DB_PORT,
#         dbname=DB_NAME,
#         user=DB_USER,
#         password=DB_PASS,
#         sslmode=DB_SSLMODE
#     )
#     cur = conn.cursor()

#     # get schema
#     cur.execute("""
#         SELECT table_name, column_name, data_type
#         FROM information_schema.columns
#         WHERE table_schema = 'public'
#         ORDER BY table_name, ordinal_position
#     """)
#     schema = "\n".join(f"{r[0]}.{r[1]} ({r[2]})" for r in cur.fetchall())

#     # nl -> sql
#     response = llm.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[{"role": "user", "content": f"""You are a PostgreSQL expert.
# Schema:
# {schema}

# Convert this request to a valid PostgreSQL query: {question}

# Allowed SQL commands: SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, TRUNCATE, WITH (CTEs).
# Return only the raw SQL query, nothing else."""}],
#         temperature=0
#     )
#     sql = response.choices[0].message.content.strip().replace("```sql", "").replace("```", "").strip()

#     # validate command is allowed
#     first_word = sql.split()[0].upper()
#     if first_word not in ALLOWED_COMMANDS:
#         conn.close()
#         return {"error": f"SQL command '{first_word}' is not allowed."}

#     # run query
#     cur.execute(sql)
#     conn.commit()

#     # fetch results if it's a SELECT or CTE
#     if first_word in ("SELECT", "WITH"):
#         rows = cur.fetchall()
#         cols = [d[0] for d in cur.description]
#         result = {"sql": sql, "columns": cols, "rows": [dict(zip(cols, r)) for r in rows]}
#     else:
#         result = {"sql": sql, "affected_rows": cur.rowcount, "status": "success"}

#     conn.close()
#     return result


# if __name__ == "__main__":
#     input_json = json.loads(sys.stdin.read())
#     print(json.dumps(execute(input_json), default=str))



# TOOL_NAME = "Database"
# TOOL_DESCRIPTION = "Convert natural language to SQL and run it on PostgreSQL. Pass the user's question as plain English in the 'text' field. Example: {'text': 'how many members are there'}"

# import sys
# import json
# import os
# import psycopg2
# from openai import OpenAI
# from dotenv import load_dotenv

# load_dotenv()

# DB_HOST = os.getenv("PG_HOST")
# DB_PORT = os.getenv("PG_PORT")
# DB_NAME = os.getenv("PG_DB")
# DB_USER = os.getenv("PG_USER")
# DB_PASS = os.getenv("PG_PASSWORD")
# DB_SSLMODE = "require"

# llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ALLOWED_COMMANDS = ("SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "DROP", "ALTER", "TRUNCATE", "WITH")


# def execute(input_data):
#     question = (
#         input_data.get("text") or
#         input_data.get("query") or
#         input_data.get("question") or ""
#     ).strip()

#     if not question:
#         return {"error": "No question provided."}

#     conn = psycopg2.connect(
#         host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
#         user=DB_USER, password=DB_PASS, sslmode=DB_SSLMODE
#     )
#     cur = conn.cursor()

#     # get only schema structure
#     cur.execute("""
#         SELECT table_name, column_name, data_type
#         FROM information_schema.columns
#         WHERE table_schema = 'public'
#         ORDER BY table_name, ordinal_position
#     """)
#     schema = "\n".join(f"{r[0]}.{r[1]} ({r[2]})" for r in cur.fetchall())

#     # nl -> sql
#     response = llm.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[{"role": "user", "content": f"""You are a PostgreSQL expert.
# Schema:
# {schema}

# Convert this to a valid PostgreSQL query: {question}

# Rules:
# - Allowed: SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, TRUNCATE, WITH
# - Do NOT add LIMIT unless the user explicitly asks for a limited number of results (e.g. "top 5", "first 10")
# - For aggregates (COUNT, SUM, AVG, etc.) never add LIMIT
# - Return only raw SQL, nothing else"""}],
#         temperature=0
#     )
#     sql = response.choices[0].message.content.strip().replace("```sql", "").replace("```", "").strip()

#     first_word = sql.split()[0].upper()
#     if first_word not in ALLOWED_COMMANDS:
#         conn.close()
#         return {"error": f"SQL command '{first_word}' is not allowed."}

#     cur.execute(sql)
#     conn.commit()

#     if first_word in ("SELECT", "WITH"):
#         rows = cur.fetchall()
#         cols = [d[0] for d in cur.description]
#         result = {"sql": sql, "row_count": len(rows), "columns": cols, "rows": [dict(zip(cols, r)) for r in rows]}
#     else:
#         result = {"sql": sql, "affected_rows": cur.rowcount, "status": "success"}

#     conn.close()
#     return result


# if __name__ == "__main__":
#     input_json = json.loads(sys.stdin.read())
#     print(json.dumps(execute(input_json), default=str))


TOOL_NAME = "Database"
TOOL_DESCRIPTION = "Convert natural language to SQL and run it on PostgreSQL. Pass the user's question as plain English in the 'text' field. Example: {'text': 'how many members are there'}"

import sys
import json
import os
import psycopg2
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("PG_HOST")
DB_PORT = os.getenv("PG_PORT")
DB_NAME = os.getenv("PG_DB")
DB_USER = os.getenv("PG_USER")
DB_PASS = os.getenv("PG_PASSWORD")
DB_SSLMODE = "require"

llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ALLOWED_COMMANDS = ("SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "DROP", "ALTER", "TRUNCATE", "WITH")


def make_summary(question, sql, columns, rows):
    """Ask LLM to turn raw rows into a clean human-readable answer."""
    # for large results, only send a sample to the summariser
    sample = rows[:20] if len(rows) > 20 else rows
    response = llm.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"""The user asked: "{question}"
The SQL ran was: {sql}
Total rows returned: {len(rows)}
Columns: {columns}
Sample rows (first {len(sample)} of {len(rows)}): {json.dumps(sample)}

Write a clear, concise human-readable answer to the user's question.
- If it's a count or single value, state it directly.
- If it's a list, summarise it naturally (e.g. "There are 364 members under 25. Their IDs are: 24, 26, 31, 32 ... and 360 more.")
- If it's a small list (under 10 items), list all of them.
- Never return raw JSON. Always respond in plain English."""}],
        temperature=0
    )
    return response.choices[0].message.content.strip()


def execute(input_data):
    question = (
        input_data.get("text") or
        input_data.get("query") or
        input_data.get("question") or ""
    ).strip()

    if not question:
        return {"error": "No question provided."}

    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
        user=DB_USER, password=DB_PASS, sslmode=DB_SSLMODE
    )
    cur = conn.cursor()

    # get only schema structure
    cur.execute("""
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position
    """)
    schema = "\n".join(f"{r[0]}.{r[1]} ({r[2]})" for r in cur.fetchall())

    # nl -> sql
    response = llm.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"""You are a PostgreSQL expert.
Schema:
{schema}

Convert this to a valid PostgreSQL query: {question}

Rules:
- Allowed: SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, TRUNCATE, WITH
- Do NOT add LIMIT unless the user explicitly asks for a limited number (e.g. "top 5", "first 10")
- For aggregates (COUNT, SUM, AVG etc.) never add LIMIT
- Return only raw SQL, nothing else"""}],
        temperature=0
    )
    sql = response.choices[0].message.content.strip().replace("```sql", "").replace("```", "").strip()

    first_word = sql.split()[0].upper()
    if first_word not in ALLOWED_COMMANDS:
        conn.close()
        return {"error": f"SQL command '{first_word}' is not allowed."}

    cur.execute(sql)
    conn.commit()

    if first_word in ("SELECT", "WITH"):
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description]
        rows_as_dicts = [dict(zip(cols, r)) for r in rows]
        summary = make_summary(question, sql, cols, rows_as_dicts)
        result = {
            "answer": summary,
            "sql": sql,
            "row_count": len(rows_as_dicts),
            "rows": rows_as_dicts
        }
    else:
        result = {"sql": sql, "affected_rows": cur.rowcount, "status": "success"}

    conn.close()
    return result


if __name__ == "__main__":
    input_json = json.loads(sys.stdin.read())
    print(json.dumps(execute(input_json), default=str))