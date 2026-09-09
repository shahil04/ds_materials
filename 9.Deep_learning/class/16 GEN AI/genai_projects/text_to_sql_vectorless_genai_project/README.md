# Text-to-SQL RAG

Natural-language SQL assistant that uses an LLM and database schema context to generate read-only SQL queries. The generated query is validated before it is executed, and the result is returned as a pandas DataFrame.

## Features

- Converts natural-language questions into SQL using OpenAI's `gpt-4o-mini` model.
- Loads table, column, primary-key, and foreign-key metadata from `knowledge/schema.json`.
- Validates generated SQL and allows only `SELECT` and `WITH` queries in the reusable pipeline.
- Executes queries through SQLAlchemy and returns tabular results.
- Includes Streamlit demos for MySQL and SQLite.

## Requirements

- Python 3.12 or later
- An API key for OpenAI, Gemini, or Groq
- MySQL database credentials for the main pipeline and MySQL demo
- SQLite is enough for the SQLite demo

## Installation

Clone the repository and create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Alternatively, if you use `uv`:

```bash
uv sync
```

## Configuration

Create a `.env` file in the project root. The reusable pipeline and MySQL demo use these variables:

```env
OPENAI_API_KEY=your-openai-api-key
GOOGLE_API_KEY=your-gemini-api-key
GROQ_API_KEY=your-groq-api-key
DB_HOST=localhost
DB_PORT=3306
DB_USER=your-database-user
DB_PASSWORD=your-database-password
DB_NAME=your-database-name
```

Do not commit `.env` or API keys to source control.

## Usage

### Command-line pipeline

The main pipeline connects to MySQL, loads the saved schema, generates and validates SQL, and executes the query:

```bash
python main.py
```

Enter a question when prompted, for example:

```text
Show the top 10 customers by number of bookings
```

The pipeline is available programmatically through `app.pipeline.ask`:

```python
from app.pipeline import ask

result = ask("Show the top 10 customers by number of bookings")
print(result)
```

### Streamlit MySQL demo

Run the interactive MySQL application:

```bash
streamlit run demo.py
```

The app can inspect the configured database schema, generate SQL, execute the query, display the results, and explain the result in plain English.

### Streamlit SQLite demo

The SQLite demo uses a local `uber.db` file:

```bash
python sql_lite_datacreate.py
streamlit run demo_sqllite.py
```

The data-generation script recreates the sample ride-booking database with customers, drivers, cabs, bookings, feedback, trip details, and trip requests.

The SQLite demo does not require MySQL credentials. In its sidebar, select `OpenAI`, `Gemini`, or `Groq`, then enter the matching API key. Keys can also be prefilled from `OPENAI_API_KEY`, `GOOGLE_API_KEY`, or `GROQ_API_KEY` in `.env`.

## Updating the schema

For the reusable MySQL pipeline, refresh the schema file after database changes:

```python
from app.schema_loader import save_schema

save_schema()
```

Run that snippet from the project root after setting the database variables in `.env`. The resulting metadata is saved to `knowledge/schema.json`.

## Project structure

```text
app/
	config.py          Environment and database configuration
	database.py        SQLAlchemy MySQL engine
	llm.py             LLM setup and SQL generation
	pipeline.py        End-to-end question-to-result pipeline
	prompt.py          Prompt construction
	retriever.py       Schema/context retrieval helpers
	schema_loader.py   Database schema extraction and persistence
	schema_reader.py   Saved schema loading
	sql_executor.py    Query execution
	sql_generator.py   SQL-generation helpers
	validator.py       Read-only SQL validation
demo.py              Streamlit MySQL application
demo_sqllite.py      Streamlit SQLite application
main.py              Command-line entry point
knowledge/schema.json Saved schema context
sql_lite_datacreate.py Sample SQLite database generator
```

## Safety notes

The reusable pipeline rejects common data-definition and data-modification statements such as `DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, `TRUNCATE`, and `CREATE`, and requires the query to begin with `SELECT` or `WITH`. Use a database user with least-privilege, read-only access when possible.

## Troubleshooting

- `OpenAIError` or authentication errors: verify `OPENAI_API_KEY` is present in `.env`.
- MySQL connection errors: check `DB_HOST`, `DB_PORT`, credentials, database availability, and firewall rules.
- Missing or stale schema: regenerate `knowledge/schema.json` with `save_schema()`.
- SQLite demo cannot find `uber.db`: run `python sql_lite_datacreate.py` from the project root first.
