from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот работает 24/7 🔥")

app = ApplicationBuilder().token("8153276855:AAEqgDMBDCsQBwlzIdB7iMtO-g6E1SWwTtg").build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
