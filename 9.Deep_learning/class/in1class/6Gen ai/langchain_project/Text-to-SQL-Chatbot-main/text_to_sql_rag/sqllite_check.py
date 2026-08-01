import json
import pandas as pd
from sqlalchemy import create_engine, inspect

# ---------------------------------------
# Connect to SQLite Database
# ---------------------------------------

DATABASE_URL = "sqlite:///uber.db"

engine = create_engine(DATABASE_URL)

print("Connected Successfully!")

# ---------------------------------------
# Get Database Schema
# ---------------------------------------

inspector = inspect(engine)

schema = {
    "database": "uber",
    "tables": []
}

for table in inspector.get_table_names():

    columns = []
    for column in inspector.get_columns(table):
        columns.append({
            "name": column["name"],
            "type": str(column["type"]),
            "nullable": column["nullable"]
        })

    primary_keys = inspector.get_pk_constraint(table)["constrained_columns"]

    foreign_keys = []
    for fk in inspector.get_foreign_keys(table):
        foreign_keys.append({
            "column": fk["constrained_columns"],
            "references_table": fk["referred_table"],
            "references_column": fk["referred_columns"]
        })

    schema["tables"].append({
        "table_name": table,
        "columns": columns,
        "primary_keys": primary_keys,
        "foreign_keys": foreign_keys
    })

# ---------------------------------------
# Save Schema
# ---------------------------------------

with open("schema.json", "w", encoding="utf-8") as f:
    json.dump(schema, f, indent=4)

print("schema.json saved successfully!")

# ---------------------------------------
# Run SQL Query using Pandas
# ---------------------------------------

sql_query = """
SELECT *
FROM customers;
"""

result = pd.read_sql(sql_query, engine)

print(result.head())


#======================================
from sqlalchemy import create_engine, inspect
import pandas as pd

# Connect to SQLite database
DATABASE_URL = "sqlite:///uber.db"

engine = create_engine(DATABASE_URL)

print("Connected Successfully")

# Execute SQL query
sql_query = """
SELECT *
FROM drivers;
"""
result = pd.read_sql(sql_query, engine)

print(result)