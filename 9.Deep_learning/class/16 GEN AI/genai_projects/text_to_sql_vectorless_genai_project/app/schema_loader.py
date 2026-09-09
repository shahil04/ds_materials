import json
import os

from sqlalchemy import inspect

from app.database import engine
from app.config import DB_NAME


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
        for column in inspector.get_columns(table):

            table_info["columns"].append({
                "name": column["name"],
                "type": str(column["type"]),
                "nullable": column["nullable"]
            })

        # Primary Key
        pk = inspector.get_pk_constraint(table)

        table_info["primary_keys"] = pk.get(
            "constrained_columns",
            []
        )

        # Foreign Keys
        for fk in inspector.get_foreign_keys(table):

            table_info["foreign_keys"].append({

                "column": fk["constrained_columns"],

                "references_table":
                    fk["referred_table"],

                "references_column":
                    fk["referred_columns"]

            })

        schema["tables"].append(table_info)

    return schema


def save_schema():

    schema = extract_schema()

    os.makedirs("knowledge", exist_ok=True)

    with open(
        "knowledge/schema.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            schema,
            f,
            indent=4
        )

    print("Schema saved successfully.")