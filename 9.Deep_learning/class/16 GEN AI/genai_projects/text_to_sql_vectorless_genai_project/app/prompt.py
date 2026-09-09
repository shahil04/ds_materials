import json


def build_prompt(schema, question):

    schema_text = json.dumps(schema, indent=2)

    prompt = f"""
You are an expert SQL developer.

Database Schema:

{schema_text}

Rules:

1. Generate ONLY SQL.
2. Never explain.
3. Use only existing tables.
4. Use only existing columns.
5. Never hallucinate.
6. Prefer JOINs using foreign keys.
7. Return a valid MySQL query.
5. also remove the ```SQL\n\n```
Question:

{question}

SQL:
"""

    return prompt