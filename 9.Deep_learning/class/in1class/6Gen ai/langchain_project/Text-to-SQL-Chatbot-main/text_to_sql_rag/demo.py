import os
import json
import re
import streamlit as st
import pandas as pd

from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect

from langchain_openai import ChatOpenAI

# ===========================
# Load Environment Variables
# ===========================

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# ===========================
# Streamlit Config
# ===========================

st.set_page_config(
    page_title="Text to SQL",
    page_icon="🗄️",
    layout="wide"
)

st.title("🗄️ Text-to-SQL Assistant")

# ===========================
# Database Connection
# ===========================

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)

# ===========================
# LLM
# ===========================

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# ===========================
# Extract Schema
# ===========================

@st.cache_data
def extract_schema():

    inspector = inspect(engine)

    schema = {
        "database": DB_NAME,
        "tables": []
    }

    for table in inspector.get_table_names():

        table_info = {
            "table_name": table,
            "columns": [],
            "primary_keys": [],
            "foreign_keys": []
        }

        for col in inspector.get_columns(table):

            table_info["columns"].append({

                "name": col["name"],
                "type": str(col["type"]),
                "nullable": col["nullable"]

            })

        pk = inspector.get_pk_constraint(table)

        table_info["primary_keys"] = pk.get(
            "constrained_columns",
            []
        )

        for fk in inspector.get_foreign_keys(table):

            table_info["foreign_keys"].append({

                "column": fk["constrained_columns"],

                "references_table": fk["referred_table"],

                "references_column": fk["referred_columns"]

            })

        schema["tables"].append(table_info)

    with open("schema.json", "w") as f:
        json.dump(schema, f, indent=4)

    return schema

# ===========================
# Clean SQL
# ===========================

def clean_sql(sql):

    sql = re.sub(r"```sql", "", sql, flags=re.I)
    sql = sql.replace("```", "")
    return sql.strip()

# ===========================
# SQL Validation
# ===========================

def validate_sql(sql):

    blocked = [

        "DROP",
        "DELETE",
        "UPDATE",
        "ALTER",
        "INSERT",
        "TRUNCATE",
        "CREATE"

    ]

    upper = sql.upper()

    for keyword in blocked:

        if keyword in upper:

            raise Exception(
                f"{keyword} is not allowed."
            )

# ===========================
# Load Schema
# ===========================

schema = extract_schema()

# ===========================
# Sidebar
# ===========================

with st.sidebar:

    st.header("Database")

    st.success(DB_NAME)

    if st.checkbox("Show Schema"):

        st.json(schema)

# ===========================
# User Question
# ===========================

question = st.text_input(
    "Ask your question",
    placeholder="Show top 10 trips"
)

if st.button("Generate SQL"):

    if question == "":

        st.warning("Please enter a question.")

        st.stop()

    schema_text = json.dumps(schema, indent=2)

    prompt = f"""
You are an expert MySQL developer.

Database Schema

{schema_text}

Rules

1. Generate ONLY SQL.
2. No explanation.
3. Use only existing tables.
4. Use only existing columns.
5. Return valid MySQL SQL.
6. Never wrap SQL inside markdown.
7. Never use ```sql```.
8. Output only SQL.

Question

{question}

SQL
"""

    with st.spinner("Generating SQL..."):

        response = llm.invoke(prompt)

        sql = clean_sql(response.content)

    validate_sql(sql)

    st.subheader("Generated SQL")

    st.code(sql, language="sql")

    with st.spinner("Executing Query..."):

        df = pd.read_sql(sql, engine)

    st.subheader("Query Result")

    st.dataframe(df, use_container_width=True)

    prompt = f"""
User Question

{question}

SQL Result

{df.to_markdown(index=False)}

Explain the answer in simple English.
"""

    answer = llm.invoke(prompt)

    st.subheader("Answer")

    st.write(answer.content)