import os
import json
import re
import streamlit as st
import pandas as pd

from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

# ===========================
# Load Environment Variables
# ===========================

load_dotenv()

# SQLite database file
DB_NAME = "uber.db"        # Change to your SQLite database filename

# ===========================
# Streamlit Config
# ===========================

st.set_page_config(
    page_title="Text-to-SQL Assistant",
    page_icon="🗄️",
    layout="wide"
)

st.title("🗄️ Text-to-SQL Assistant (SQLite)")

# ===========================
# Database Connection
# ===========================

DATABASE_URL = f"sqlite:///{DB_NAME}"

engine = create_engine(DATABASE_URL)

# ===========================
# Extract Database Schema
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

        # Columns
        for col in inspector.get_columns(table):

            table_info["columns"].append({
                "name": col["name"],
                "type": str(col["type"]),
                "nullable": col["nullable"]
            })

        # Primary Keys
        pk = inspector.get_pk_constraint(table)

        table_info["primary_keys"] = pk.get(
            "constrained_columns",
            []
        )

        # Foreign Keys
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

    sql = re.sub(r"```sql", "", sql, flags=re.IGNORECASE)
    sql = sql.replace("```", "")

    return sql.strip()


# ===========================
# SQL Validation
# ===========================

def validate_sql(sql):

    blocked_keywords = [

        "DROP",
        "DELETE",
        "UPDATE",
        "ALTER",
        "INSERT",
        "TRUNCATE",
        "CREATE"

    ]

    upper_sql = sql.upper()

    for keyword in blocked_keywords:

        if keyword in upper_sql:

            raise Exception(
                f"{keyword} statements are not allowed."
            )


def create_llm(provider, api_key, model_name):

    if provider == "Gemini":
        return ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=api_key,
            temperature=0
        )

    if provider == "Groq":
        return ChatOpenAI(
            model=model_name,
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
            temperature=0
        )

    return ChatOpenAI(
        model=model_name,
        api_key=api_key,
        temperature=0
    )


def validate_model_for_provider(provider, model_name):

    model_name = model_name.strip().lower()

    if provider == "Gemini" and not model_name.startswith("gemini-"):
        raise ValueError(
            "Gemini requires a Gemini model name, for example "
            "gemini-2.0-flash."
        )

    if provider == "Groq" and model_name.startswith(("gpt-", "gemini-")):
        raise ValueError(
            "Groq requires a Groq-supported model name, for example "
            "llama-3.3-70b-versatile."
        )

    if provider == "OpenAI" and not model_name.startswith(("gpt-", "o1", "o3", "o4")):
        raise ValueError(
            "OpenAI requires an OpenAI model name, for example gpt-4o-mini."
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

    st.success(f"SQLite Database\n\n{DB_NAME}")

    st.header("AI Provider")

    provider = st.selectbox(
        "Choose a provider",
        ["OpenAI", "Gemini", "Groq"],
        key="provider"
    )

    default_models = {
        "OpenAI": "gpt-4o-mini",
        "Gemini": "gemini-3.5-flash",
        "Groq": "llama-3.3-70b-versatile"
    }

    model_state_key = f"model_name_{provider.lower()}"

    if model_state_key not in st.session_state:
        st.session_state[model_state_key] = default_models[provider]

    settings_page = st.radio(
        "AI settings",
        ["Add AI Keys", "Model Name"],
        horizontal=True,
        label_visibility="collapsed"
    )

    if settings_page == "Add AI Keys":
        api_key_name = {
            "OpenAI": "OPENAI_API_KEY",
            "Gemini": "GOOGLE_API_KEY",
            "Groq": "GROQ_API_KEY"
        }[provider]

        api_key = st.text_input(
            f"{provider} API key",
            type="password",
            value=os.getenv(api_key_name, ""),
            key=f"api_key_{provider.lower()}",
            help="Your key is used for this Streamlit session and is not saved by the app."
        )
    else:
        model_name = st.text_input(
            "Model name",
            key=model_state_key,
            help=f"Default: {default_models[provider]}"
        )

    api_key = st.session_state.get(f"api_key_{provider.lower()}", "")
    model_name = st.session_state.get(model_state_key, default_models[provider])

    if st.checkbox("Show Schema"):

        st.json(schema)


# ===========================
# User Question
# ===========================

question = st.text_input(

    "Ask your question",

    placeholder="Example: Show top 10 trips"

)

# ===========================
# Generate SQL
# ===========================

if st.button("Generate SQL"):

    if question.strip() == "":

        st.warning("Please enter a question.")

        st.stop()

    if not api_key.strip():

        st.error(f"Enter a {provider} API key in the sidebar.")

        st.stop()

    if not model_name.strip():

        st.error("Enter a model name in the Model Name section of the sidebar.")

        st.stop()

    try:
        validate_model_for_provider(provider, model_name)
    except ValueError as error:
        st.error(str(error))
        st.stop()

    llm = create_llm(provider, api_key.strip(), model_name.strip())

    schema_text = json.dumps(schema, indent=2)

    prompt = f"""
You are an expert SQLite developer.

Database Schema

{schema_text}

Rules

1. Generate ONLY SQL.
2. No explanation.
3. Use only existing tables.
4. Use only existing columns.
5. Return valid SQLite SQL.
6. Never wrap SQL inside markdown.
7. Never use ```sql```.
8. Output only SQL.
9. Use SQLite syntax only.
10. Use LIMIT instead of TOP.

Question

{question}

SQL
"""

    with st.spinner("Generating SQL..."):

        response = llm.invoke(prompt)

        sql = clean_sql(response.content)

    try:

        validate_sql(sql)

        st.subheader("Generated SQL")

        st.code(sql, language="sql")

        with st.spinner("Executing Query..."):

            df = pd.read_sql(sql, engine)

        st.subheader("Query Result")

        st.dataframe(df, use_container_width=True)

        explanation_prompt = f"""
You are a helpful assistant.

User Question:
{question}

SQL Result:
{df.to_markdown(index=False)}

Explain the result in simple English.
"""

        answer = llm.invoke(explanation_prompt)

        st.subheader("Answer")

        st.write(answer.content)

    except Exception as e:

        st.error(str(e))