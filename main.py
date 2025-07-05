from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Բարեւ։ Սա RoynexBot է։")

if __name__ == '__main__':
    app = ApplicationBuilder().token("ТВОЙ_ТОКЕН").build()
    
    app.add_handler(CommandHandler("start", start))

    app.run_polling()
