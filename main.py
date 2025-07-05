import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📸 Կարծիքներ Roynex-ի մասին", callback_data="reviews")],
        [InlineKeyboardButton("💼 Մյուս նախագծեր", callback_data="projects")],
        [InlineKeyboardButton("💎 Գնել VIP", callback_data="buy_vip")],
        [InlineKeyboardButton("💰 Լիցքավորել հաշիվ", callback_data="top_up")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Բարի գալուստ RoyNex Bot 🔐", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "reviews":
        await query.edit_message_text("📸 Ահա Roynex-ի կարծիքները...")
    elif query.data == "projects":
        await query.edit_message_text("💼 Այստեղ կգտնես մեր մյուս նախագծերը...")
    elif query.data == "buy_vip":
        await query.edit_message_text("💎 Գնելու համար VIP՝ փոխանցիր 45000 Դրամ այս համարին՝\n\n**4355 0539 2271 9150**")
    elif query.data == "top_up":
        await query.edit_message_text("💰 Լիցքավորման համար ուղարկիր սքրին՝ վճարման մասին: Մենք կհաստատենք հաշիվը:")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
