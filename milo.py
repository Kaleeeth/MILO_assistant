import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, JobQueue
from datetime import time
from modules.news_module import fetch_news
from modules.weather_module import get_weather

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID_FILE = "data/chat_id.txt"

def save_chat_id(chat_id: int):
    with open(CHAT_ID_FILE, "w") as f:
        f.write(str(chat_id))

def load_chat_id():
    try:
        with open(CHAT_ID_FILE, "r") as f:
            return int(f.read().strip())
    except:
        return None

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    save_chat_id(chat_id)
    await context.bot.send_message(chat_id=chat_id, text="¡Listo! Chat ID guardado.")

async def hola_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text="Hola, soy MILO. ¿En qué te puedo ayudar?")

async def daily_briefing(context: ContextTypes.DEFAULT_TYPE):
    chat_id = load_chat_id()
    if not chat_id:
        return

    clima = get_weather("Merida")
    noticias = fetch_news(limit=3)

    noticias_texto = ""
    for n in noticias:
        noticias_texto += f"- {n['title']}: {n['summary']} ({n['url']})\n"

    briefing_text = (
        "Buenos días, soy MILO con tu informe diario.\n\n"
        f"Clima hoy en Mérida: {clima}\n\n"
        f"Noticias principales:\n{noticias_texto}\n\n"
        "Recuerda que no tienes que ser perfecto, solo avanzar un poco cada día."
    )

    await context.bot.send_message(chat_id=chat_id, text=briefing_text, parse_mode="Markdown")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("hola", hola_command))

    job_queue: JobQueue = app.job_queue
    job_queue.run_daily(daily_briefing, time(hour=5, minute=0, second=0))

    print("MILO running...")
    app.run_webhook(
    listen="0.0.0.0",
    port=int(os.environ.get("PORT", 8443)),
    webhook_url=f"https://milo-assistant.onrender.com/{TOKEN}"
)

if __name__ == "__main__":
    main()