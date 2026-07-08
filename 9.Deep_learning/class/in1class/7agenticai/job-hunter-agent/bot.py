import os
from dotenv import load_dotenv
load_dotenv()
import logging
import tempfile
import pdfplumber
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from agent import run_agent

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def extract_text_from_pdf(file_path):
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        logger.error(f"PDF extraction error: {e}")
        return None
    return text.strip() if text.strip() else None

async def start_command(update, context):
    welcome = (
        "Hey! I'm your Job Hunter Agent.\n\n"
        "Here's how to use me:\n\n"
        "1. Upload your resume as a PDF file\n"
        "2. Tell me what jobs to find, like:\n"
        "   - Find me AI Agent Engineer jobs\n"
        "   - Find remote jobs based on my resume\n"
        "   - Search for Python developer roles\n\n"
        "Start by sending me your resume PDF."
    )
    await update.message.reply_text(welcome)

async def help_command(update, context):
    has_resume = "resume_text" in context.user_data and context.user_data["resume_text"]
    status = "Resume uploaded" if has_resume else "No resume uploaded"
    help_text = (
        f"Job Hunter Agent\n\n"
        f"Status: {status}\n\n"
        f"Commands:\n"
        f"/start - Welcome message\n"
        f"/help - This help text\n"
        f"/clear - Clear history and resume\n"
        f"/resume - Check resume status\n\n"
        f"Upload your resume as a PDF, then tell me what jobs to find!"
    )
    await update.message.reply_text(help_text)

async def clear_command(update, context):
    context.user_data["history"] = []
    context.user_data["resume_text"] = None
    await update.message.reply_text("Cleared! Upload a new resume to start fresh.")

async def resume_command(update, context):
    resume_text = context.user_data.get("resume_text")
    if resume_text:
        preview = resume_text[:200] + "..." if len(resume_text) > 200 else resume_text
        await update.message.reply_text(f"Resume loaded! ({len(resume_text)} characters)\n\nPreview:\n{preview}")
    else:
        await update.message.reply_text("No resume uploaded yet. Send me your resume as a PDF file.")

async def handle_document(update, context):
    document = update.message.document
    if not document.file_name.lower().endswith(".pdf"):
        await update.message.reply_text("Please upload a PDF file.")
        return
    processing_msg = await update.message.reply_text("Reading your resume...")
    try:
        file = await document.get_file()
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, f"resume_{update.effective_user.id}.pdf")
        await file.download_to_drive(file_path)
        resume_text = extract_text_from_pdf(file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
        if resume_text:
            context.user_data["resume_text"] = resume_text
            context.user_data["history"] = []
            await processing_msg.delete()
            await update.message.reply_text(
                f"Resume uploaded successfully! ({len(resume_text)} characters extracted)\n\n"
                f"Now tell me what jobs to search for. For example:\n"
                f"- Find me AI Agent Engineer jobs\n"
                f"- Find remote jobs based on my resume\n"
                f"- Search for Python developer roles"
            )
        else:
            await processing_msg.delete()
            await update.message.reply_text("Couldn't extract text from this PDF. Try a text-based PDF.")
    except Exception as e:
        logger.error(f"Document handling error: {e}")
        await processing_msg.delete()
        await update.message.reply_text(f"Error processing the file: {str(e)}")

async def handle_message(update, context):
    user_message = update.message.text
    if "history" not in context.user_data:
        context.user_data["history"] = []
    resume_text = context.user_data.get("resume_text")
    thinking_msg = await update.message.reply_text("Searching and analyzing jobs... This may take a minute or two.")
    try:
        response = run_agent(user_message, context.user_data["history"], resume_text=resume_text)
        await thinking_msg.delete()
        if len(response) <= 4096:
            try:
                await update.message.reply_text(response, parse_mode="Markdown")
            except Exception:
                await update.message.reply_text(response)
        else:
            chunks = split_message(response, 4096)
            for chunk in chunks:
                try:
                    await update.message.reply_text(chunk, parse_mode="Markdown")
                except Exception:
                    await update.message.reply_text(chunk)
    except Exception as e:
        logger.error(f"Agent error: {e}")
        await thinking_msg.delete()
        await update.message.reply_text(f"Something went wrong: {str(e)}\n\nTry again or use /clear to reset.")

def split_message(text, max_length=4096):
    if len(text) <= max_length:
        return [text]
    chunks, current = [], ""
    for line in text.split("\n"):
        if len(current) + len(line) + 1 <= max_length:
            current += line + "\n"
        else:
            if current:
                chunks.append(current.strip())
            current = line + "\n"
    if current.strip():
        chunks.append(current.strip())
    return chunks

def main():
    if not TELEGRAM_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not set!")
        return
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY not set!")
        return
    if not os.getenv("TAVILY_API_KEY"):
        print("Error: TAVILY_API_KEY not set!")
        return
    print("All API keys found")
    print("Starting Job Hunter Bot...")
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("clear", clear_command))
    app.add_handler(CommandHandler("resume", resume_command))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running! Send it a message on Telegram.")
    print("Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()