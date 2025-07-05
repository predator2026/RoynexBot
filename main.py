############################################################
#  ROYNEX | VIP ⚡️ — Telegram-Bot (python-telegram-bot 20.8)
############################################################
#
# requirements.txt
#   python-telegram-bot>=20.8
#   Flask#
# ▸ Автор: ты  +  ChatGPT.  Права твои 😉
from keep_alive import keep_alive

keep_alive()
import os, json, threading
from telegram import (Update, InlineKeyboardButton, InlineKeyboardMarkup,
                      InputMediaPhoto)
from telegram.ext import (ApplicationBuilder, Application, CommandHandler,
                          CallbackQueryHandler, ContextTypes, filters)

# ---------- НАСТРОЙКИ ---------- #
ADMIN_ID = 8121378603  # кто может /addbalance
MAIN_PHOTO = "https://i.imgur.com/T0bvlAM.jpeg"
PROJECT_URL = "https://roynex.com"

REVIEWS_PHOTOS = [
    "https://i.imgur.com/ehnNYY6.jpeg",
    "https://i.imgur.com/qB7FNQw.jpeg",
    "https://i.imgur.com/6F0qKwc.jpeg",
    "https://i.imgur.com/huXIN7N.jpeg",
    "https://i.imgur.com/oIgbmTS.jpeg",
    "https://i.imgur.com/vj4uVwQ.jpeg",
    "https://i.imgur.com/oyFmhrg.jpeg",
    "https://i.imgur.com/yElySj3.jpeg",
    "https://i.imgur.com/0QJNzZT.jpeg",
    "https://i.imgur.com/zUybKUC.jpeg",
]

# ---------- ЭМОДЖИ (fallback / premium) ---------- #
# Если у вас есть Premium-emoji — впишите ID ↓
PREMIUM_DIAMOND_ID = None  # пример: "543210987654321"
PREMIUM_COIN_ID = None  # пример: "987654321012345"


def prem(emoji_id, default):
    return f'<tg-emoji emoji-id="{emoji_id}">{default}</tg-emoji>' if emoji_id else default


DIAMOND = prem(PREMIUM_DIAMOND_ID, "💎")
COIN = prem(PREMIUM_COIN_ID, "🪙")

# ---------- ТЕКСТЫ / КНОПКИ ---------- #
BTN_VIP = f"Գնել VIP {DIAMOND}"
BTN_REVIEW = "Կարծիքներ Roynex-ի մասին 💬"
BTN_ROYCOIN = f"RoyCoin {COIN} soon"
BTN_VIP_ADV = "VIP-ի առավելությունները 📈"
BTN_DUPL = "Ստանալ գումարը 💰"
BTN_BACK = "🔙 Վերադառնալ մենյու"

VIP_PRICE_TEXT = f"{DIAMOND} <b>VIP արժեքը — 45 000 դր.</b> 🔥"
VIP_ADV_TEXT = (
    "🧠 <b>VIP բաժինը նախատեսված է այն մարդկանց համար, ովքեր լիովին կենտրոնացած են արդյունքի վրա</b>․\n\n\n"
    "🚀 x2․4 շահույթ\n\n"
    "🗝️ Մուտք RoyCoin-ի գործարքներ\n\n"
    "📲 Հեռախոսազանգ մենեջերների հետ\n\n"
    "💼 Անսահման ներդրում (x2․4)\n\n"
    "📎 Մուտք 💵 <b>ELITE чат</b>")

PAYMENT_TMPL = (
    "🏦 <b>ACBA 4355 0539 2271 9150</b>\n\n"
    "✅ Փոխանցումից հետո ուղարկեք կտրոնը մենեջերներին 👉 "
    "<a href='https://t.me/RoynexManager'>@RoynexManager</a>\n\n"
    f"{DIAMOND} VIP օգտվողների շահույթը կրկնապատկվում է <b>x2.4</b>")

DUPL_AMOUNTS = [
    "10 000💎", "20 000💎", "40 000💎", "80 000💎", "200 000💎", "400 000💎",
    "1 000 000💎"
]

# ---------- «База» (балансы / VIP-список) ---------- #
DATA_FILE = "db.json"
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"balances": {}, "vip": []}, f)
with open(DATA_FILE, "r") as f:
    db = json.load(f)


def save_db():  # можно дописать реальный учёт
    with open(DATA_FILE, "w") as f:
        json.dump(db, f, ensure_ascii=False)


# ---------- Хранилище ID сообщений ---------- #
user_msgs: dict[int, list[int]] = {}


async def clear_user(uid: int, bot):
    for mid in user_msgs.get(uid, []):
        try:
            await bot.delete_message(uid, mid)
        except:
            pass
    user_msgs[uid] = []


# ---------- Главное меню ---------- #
async def show_menu(uid: int, bot):
    kb = [
        [InlineKeyboardButton(BTN_VIP, callback_data="buy_vip")],
        [InlineKeyboardButton(BTN_REVIEW, callback_data="reviews")],
        [InlineKeyboardButton(BTN_ROYCOIN, callback_data="roycoin")],
        [InlineKeyboardButton(BTN_VIP_ADV, callback_data="vip_adv")],
        [InlineKeyboardButton(BTN_DUPL, callback_data="dupl")],
    ]
    msg = await bot.send_photo(uid,
                               MAIN_PHOTO,
                               caption="Բարի գալուստ RoyNex 🤝",
                               reply_markup=InlineKeyboardMarkup(kb))
    user_msgs.setdefault(uid, []).append(msg.message_id)


# ---------- /start ---------- #
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    # удаляем /start
    try:
        await context.bot.delete_message(uid, update.message.message_id)
    except:
        pass
    await clear_user(uid, context.bot)
    await show_menu(uid, context.bot)


# ---------- Callback-кнопки ---------- #
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q, uid = update.callback_query, update.callback_query.from_user.id
    await q.answer()
    await clear_user(uid, context.bot)

    if q.data == "reviews":
        media = [InputMediaPhoto(p) for p in REVIEWS_PHOTOS[:10]]
        if media:
            ms = await context.bot.send_media_group(uid, media=media)
            user_msgs.setdefault(uid, []).extend([m.message_id for m in ms])
        kb = [[InlineKeyboardButton(BTN_BACK, callback_data="back")]]
        m = await context.bot.send_message(
            uid,
            "Շնորհակալություն արձագանքման համար 💬",
            reply_markup=InlineKeyboardMarkup(kb))
        user_msgs[uid].append(m.message_id)

    elif q.data == "buy_vip":
        kb = [[InlineKeyboardButton(BTN_BACK, callback_data="back")]]
        m = await q.message.reply_text(VIP_PRICE_TEXT + "\n\n" + PAYMENT_TMPL,
                                       reply_markup=InlineKeyboardMarkup(kb),
                                       parse_mode="HTML")
        user_msgs[uid].append(m.message_id)

    elif q.data == "vip_adv":
        kb = [[InlineKeyboardButton(BTN_BACK, callback_data="back")]]
        m = await q.message.reply_text(VIP_ADV_TEXT,
                                       reply_markup=InlineKeyboardMarkup(kb),
                                       parse_mode="HTML")
        user_msgs[uid].append(m.message_id)

    elif q.data == "roycoin":
        kb = [[InlineKeyboardButton(BTN_BACK, callback_data="back")]]
        m = await q.message.reply_text("🚧 RoyCoin շուտով…",
                                       reply_markup=InlineKeyboardMarkup(kb))
        user_msgs[uid].append(m.message_id)

    elif q.data == "dupl":
        rows = [[
            InlineKeyboardButton(f"{amt} դր.", callback_data=f"dupl_{amt}")
        ] for amt in DUPL_AMOUNTS]
        rows.append([InlineKeyboardButton(BTN_BACK, callback_data="back")])
        m = await q.message.reply_text("♟ Ընտրեք գումարը՝",
                                       reply_markup=InlineKeyboardMarkup(rows))
        user_msgs[uid].append(m.message_id)

    elif q.data.startswith("dupl_"):
        kb = [[InlineKeyboardButton(BTN_BACK, callback_data="back")]]
        m = await q.message.reply_text(PAYMENT_TMPL,
                                       reply_markup=InlineKeyboardMarkup(kb),
                                       parse_mode="HTML")
        user_msgs[uid].append(m.message_id)

    elif q.data == "back":
        await show_menu(uid, context.bot)


# ---------- Flask keep-alive (Replit) ---------- #
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "ROYNEX bot is alive!", 200


def keep_alive():
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=8080)).start()


# ---------- MAIN ---------- #
def main():
    keep_alive()
    bot_token = os.getenv("BOT_TOKEN")
    # или пропишите руками:
    # bot_token = "YOUR_BOT_TOKEN_HERE"
    if not bot_token:
        print("❌  Добавь BOT_TOKEN в Secrets")
        return

    application: Application = ApplicationBuilder().token(bot_token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(buttons))

    print("✅  Roynex bot started")
    application.run_polling()


if __name__ == "__main__":
    main()
