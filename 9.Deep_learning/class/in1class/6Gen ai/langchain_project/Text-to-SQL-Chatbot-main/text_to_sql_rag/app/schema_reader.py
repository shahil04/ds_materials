import json


def load_schema():

    with open(
        "knowledge/schema.json",
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)