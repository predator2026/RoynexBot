import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет! Я работаю.')

async def main():
    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    await app.initialize()
    await app.start()
    print("Bot запущен")# polling срабатывает на Имена обновлений
    await asyncio.Event().wait()       # держим процесс в живых

if __name__ == "__main__":
    asyncio.run(main())
