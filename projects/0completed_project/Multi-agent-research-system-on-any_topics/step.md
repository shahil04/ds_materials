# ResearchMind - Quick Start Guide

## Prerequisites

- Python 3.12+
- `uv` package manager (install with `pip install uv`)
- Tavily API Key ([Get it here](https://www.tavily.com/pricing))
- OpenAI API Key ([Get it here](https://platform.openai.com/api-keys))

---

## Step 1: Environment Setup

Create a virtual environment using `uv`:

```bash
uv venv --python 3.12
```

Activate the environment:
- **Windows**: `.venv\Scripts\activate`
- **Mac/Linux**: `source .venv/bin/activate`

---

## Step 2: Install Dependencies

Install all required packages from `requirements.txt`:

```bash
uv pip install -r requirements.txt
```

---

## Step 3: Add API Credentials

Create a `.env` file in the project root:

```bash
echo > .env
```

Add your API keys to `.env`:

```
TAVILY_API_KEY="your_tavily_api_key_here"
OPENAI_API_KEY="your_openai_api_key_here"
```

**Alternatively**, you can add credentials directly from the app's Credentials page after launching.

---

## Step 4: Run the Application

Start the Streamlit app:

```bash
uv run streamlit run app.py
```

Or simply:

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501` in your browser.

---

## Step 5: Using the App

1. **Home Page**: Enter a research topic in the search box
2. **Add Credentials**: Click "Add credentials" to paste your API keys if not already set
3. **Run Pipeline**: Click "Run Research Pipeline" to start the multi-agent workflow
4. **View Results**: See real-time pipeline progress and final research report

---

## Troubleshooting

- **Missing API Keys**: Ensure your `.env` file has both `TAVILY_API_KEY` and `OPENAI_API_KEY`
- **Port Already in Use**: Run on a different port with `streamlit run app.py --server.port 8502`
- **Module Not Found**: Re-run `uv pip install -r requirements.txt`
