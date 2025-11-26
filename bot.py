from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import random
import json
import os

TOKEN = os.environ.get("BOT_TOKEN", "7244583495:AAE0mLiQ2DOxb3EMhFluvm3mkrOG9RCxWBg")
STICKER_IDS = []
DEFAULT_PROBABILITY = 0.3

def load_settings():
    try:
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as f:
                return json.load(f)
    except:
        pass
    return {"probability": DEFAULT_PROBABILITY}

def save_settings():
    try:
        with open("settings.json", "w") as f:
            json.dump(settings, f)
    except:
        pass

def load_stickers():
    try:
        if os.path.exists("stickers.json"):
            with open("stickers.json", "r") as f:
                return json.load(f)
    except:
        pass
    return []

def save_stickers():
    try:
        with open("stickers.json", "w") as f:
            json.dump(STICKER_IDS, f)
    except:
        pass

settings = load_settings()
STICKER_IDS = load_stickers()

def start(update: Update, context):
    update.message.reply_text(
        "🤖 Стикер-бот\n\n"
        "Команды:\n"
        "/sticker - принудительно отправить стикер\n"
        "/freq 50 - установить частоту (1-100%)\n"
        "Бот отзывается на: бот, 1548, Инкогнито, 48, 405, коза\n"
        "Перешли стикеры чтобы добавить их в базу!"
    )

def force_sticker(update: Update, context):
    if STICKER_IDS:
        update.message.reply_sticker(random.choice(STICKER_IDS))
    else:
        update.message.reply_text("❌ Нет стикеров в базе")

def set_frequency(update: Update, context):
    if context.args:
        try:
            freq = int(context.args[0])
            if 1 <= freq <= 100:
                settings["probability"] = freq / 100
                save_settings()
                update.message.reply_text(f"✅ Частота: {freq}%")
        except:
            pass

def add_sticker(update: Update, context):
    if update.message.sticker:
        sticker_id = update.message.sticker.file_id
        if sticker_id not in STICKER_IDS:
            STICKER_IDS.append(sticker_id)
            save_stickers()
            update.message.reply_text(f'✅ Стикер добавлен! Всего: {len(STICKER_IDS)}')

def handle_message(update: Update, context):
    if update.message.text:
        text = update.message.text.lower()
        if any(word in text for word in ["бот", "1548", "инкогнито", "48", "405", "коза"]):
            responses = [
                "Созвать всех",
                "Яна самая прекрасная, сильная, умная девушка. Просто лучшая!!!",
                "иди нахуй",
                "чего тебе",
                "не мешай работать",
                "иди на экспу холоп",
                "отстань",
                "занят, не до тебя",
                "что опять надо?",
                "не сейчас",
                "тьма сама себя не купит",
                "саня пидр",
                "ДБ помойка ебаная",
                "ЖаднаяКоза лучшая",
                "Во всем виноват всегда 405, lowka и весь 1548",
                "Вы все биомусор",
                "Будете в соло межке еще год",
                "Я запрещаю вам ливать с 1548",
                "За алмазы вставать будете",
                "как вы заебали со своим ДБ и экспой",
                "ловка ливнул, вы не знали?",
                "дед пердун ленивый",
                "Вы все ежи прошли?",
                "Алеша, ты наш бог",
                "Саня скинет хуй через 30 секунд!!!",
                "Кто не ходит на экспу, тот пес",
                "Яна мышь",
                "Саня любит нас",
                "Вы меня заебали",
                "Как всегда все самое лучшее Лешеньке",
            ]
            update.message.reply_text(random.choice(responses))
        elif STICKER_IDS and random.random() < settings["probability"]:
            update.message.reply_sticker(random.choice(STICKER_IDS))

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("sticker", force_sticker))
    dp.add_handler(CommandHandler("freq", set_frequency))
    dp.add_handler(MessageHandler(Filters.sticker, add_sticker))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    
    print("✅ Бот запущен на Render!")
    updater.start_polling()
    updater.idle()

if name == "main":
    main()
