# Job Hunter Agent - Setup and Run Guide (Using uv)
C:\Users\hp\Documents\ds_materials\1.1_resume\me 
curl.exe -F "file=@C:\Users\hp\Documents\ds_materials\1.1_resume\me\shahil_Ds_CV_jan2025.pdf" http://localhost:5000/upload

## Prerequisites
- Python 3.9+ installed
- `uv` package manager installed ([install uv](https://docs.astral.sh/uv/getting-started/installation/))

## Installation Steps

### 1. Install `uv` (if not already installed)
```bash
# On Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Create Project Directory
```bash
mkdir job-hunter-agent
cd job-hunter-agent
```

### 3. Initialize UV Project
```bash
uv init --python 3.11
```

### 4. Sync Dependencies
Copy the `requirements.txt` file or use this command to sync all dependencies:
```bash
uv sync
```

This will create a `.venv` virtual environment and install all packages from `requirements.txt`.

### 5. Configure Environment Variables

Create a `.env` file in the project root with the following:

```env
OPENAI_API_KEY=your-openai-api-key-here
TAVILY_API_KEY=your-tavily-api-key-here
TELEGRAM_BOT_TOKEN=your-telegram-bot-token-here
```

**Get API Keys:**
- **OpenAI API Key**: https://platform.openai.com/api-keys
- **Tavily API Key**: https://tavily.com
- **Telegram Bot Token**: Create via [@BotFather](https://t.me/botfather) on Telegram

### 6. Activate Virtual Environment (Optional)
```bash
# On Windows
.\.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

## Running the Project

### Option A: Run Terminal Agent (Testing)
```bash
uv run python agent.py
```

This starts an interactive terminal mode where you can test the agent directly.

### Option B: Run Telegram Bot
```bash
uv run python bot.py
```

This starts the Telegram bot. It will connect to Telegram and wait for messages.

### Option C: Run with uv directly (without activating venv)
```bash
# Terminal agent
uv run agent.py

# Telegram bot
uv run bot.py
```

## Adding New Dependencies

If you need to add new packages:

```bash
uv add package-name
```

This will update `requirements.txt` and install the package automatically.

## Removing Dependencies

```bash
uv remove package-name
```

## Updating Dependencies

```bash
uv sync --upgrade
```

## Project Structure

```
job-hunter-agent/
├── .env                 # Environment variables (create this)
├── .gitignore          # Git ignore file
├── .venv/              # Virtual environment (auto-created by uv)
├── agent.py            # Core agent logic with OpenAI & LangChain
├── bot.py              # Telegram bot interface
├── requirements.txt    # Python dependencies
├── steps.md            # This file
└── pyproject.toml      # UV project configuration (auto-created)
```

## Key Features

- **OpenAI Integration**: Uses GPT-4o model for intelligent job recommendations
- **LangChain Support**: Structured tool calling and message handling
- **Job Search**: Powered by Tavily search API
- **Resume Parsing**: Extracts text from PDF resumes
- **Telegram Bot**: User-friendly interface for job hunting

## Usage Example (Terminal Mode)

```
You: Find me AI engineer jobs

Thinking...

Agent: I'll search for AI engineer positions...
  Calling tool: search_jobs
  Calling tool: read_job_posting
  Calling tool: score_job_match
  
Here are the top matches...
```

## Troubleshooting

### Error: "OPENAI_API_KEY not set"
- Make sure `.env` file exists in the project root
- Verify the API key is correct and valid
- Try restarting the bot

### Error: "ModuleNotFoundError"
- Run `uv sync` to ensure all dependencies are installed
- Check that you're using `uv run` or have activated the `.venv`

### Error: "Connection timeout"
- Check internet connection
- Verify API keys are correct
- Check if APIs are down at their respective dashboards

## Tips

1. **Faster Installation**: `uv` is significantly faster than `pip`
2. **Lock File**: Use `uv lock` to create a `uv.lock` file for reproducible environments
3. **Python Management**: `uv` can also manage Python versions (use `uv python install`)

## References

- [uv Documentation](https://docs.astral.sh/uv/)
- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Tavily Search API](https://tavily.com)
- [python-telegram-bot Documentation](https://python-telegram-bot.readthedocs.io/)
