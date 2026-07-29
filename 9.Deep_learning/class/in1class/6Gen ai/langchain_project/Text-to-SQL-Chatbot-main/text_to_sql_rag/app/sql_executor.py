import pandas as pd

from app.database import engine


def execute(sql):

    return pd.read_sql(sql, engine)