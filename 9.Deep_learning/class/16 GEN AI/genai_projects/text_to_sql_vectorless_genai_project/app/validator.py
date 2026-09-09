import re


ALLOWED = [
    "SELECT",
    "WITH"
]


BLOCKED = [
    "DROP",
    "DELETE",
    "UPDATE",
    "ALTER",
    "INSERT",
    "TRUNCATE",
    "CREATE"
]


def validate(sql):

    sql_upper = sql.upper()

    for keyword in BLOCKED:

        if keyword in sql_upper:

            raise Exception(
                f"Blocked SQL keyword: {keyword}"
            )

    if not any(
        sql_upper.startswith(k)
        for k in ALLOWED
    ):

        raise Exception("Only SELECT queries are allowed.")

    return sql