# DevOps Gemini Chatbot

This project implements a chatbot system designed to assist DevOps students by addressing their queries using the Gemini API. The chatbot is built with Gradio for a user-friendly web interface.

## Project Structure

```
devops-gemini-chatbot
├── src
│   ├── chatbot.py       # Main logic for the chatbot
│   └── prompts.py       # Defines prompts for user interaction
├── app.py               # Entry point for the application
├── requirements.txt     # Project dependencies
├── .env.example         # Template for environment variables
└── README.md            # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd devops-gemini-chatbot
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   - Copy `.env.example` to `.env` and fill in your Gemini API key:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```

## Usage

To run the chatbot application, execute the following command:

```bash
python app.py
```

This will start a local server, and you can access the chatbot interface in your web browser.

## Chatbot Capabilities

- Answering questions related to DevOps concepts and practices.
- Providing resources and guidance for DevOps tools and methodologies.
- Assisting with troubleshooting common DevOps issues.

Feel free to contribute to the project by submitting issues or pull requests!