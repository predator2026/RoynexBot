import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Բարև, սա RoynexBot է 🔐")

async def main():
    token = os.getenv("8153276855:AAEqgDMBDCsQBwlzIdB7iMtO-g6E1SWwTtg")
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))

    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
