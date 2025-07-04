import os
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes, Application
)

# ───────────────────────────────────────
# 1)   БЕРЁМ ТОКЕН ИЗ ENV-переменной
# ───────────────────────────────────────
TOKEN = os.getenv("TOKEN")          #  ты уже добавил её в Settings → Environment
if not TOKEN:
    raise RuntimeError("❌  Environment variable TOKEN is not set!")

# ───────────────────────────────────────
# 2)   ХЭНДЛЕРЫ /start и /help
# ───────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Բարի գալուստ RoynexBot ⚡️\n"
        "Օգտագործի՛ր /help հրամանը, եթե ենթարկվում ես 😊"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start — գլխավոր մենյու\n"
        "/help — այս օգնությունը"
    )

# ───────────────────────────────────────
# 3)   ГЛАВНАЯ функция
# ───────────────────────────────────────
async def main():
    app: Application = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help",  help_cmd))

    print("✅  RoynexBot запущен (polling)…")
    await app.run_polling()

# ───────────────────────────────────────
if __name__ == "__main__":
    asyncio.run(main())
