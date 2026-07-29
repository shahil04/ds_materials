from app.schema_reader import load_schema
from app.prompt import build_prompt
from app.llm import generate_sql
from app.validator import validate
from app.sql_executor import execute


def ask(question):

    schema = load_schema()

    prompt = build_prompt(
        schema,
        question
    )

    sql = generate_sql(prompt)

    sql = validate(sql)

    print("\nGenerated SQL\n")
    print(sql)

    result = execute(sql)

    return result