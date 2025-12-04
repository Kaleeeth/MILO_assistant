from flask import Flask, request
from telegram import Update
from telegram.ext import Application
from milo import TOKEN

app = Flask(__name__)

application = Application.builder().token(TOKEN).build()

@app.post(f"/{TOKEN}")
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return "OK"
