import os
import random
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

print("=== БОТ ЗАПУЩЕН НА RENDER ===")

TOKEN = os.environ.get("BOT_TOKEN", "7244583495:AAE0mLiQ2DOxb3EMhFluvm3mkrOG9RCxWBg")
STICKER_IDS = []
DEFAULT_PROBABILITY = 0.3

# Загружаем настройки
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

# Загружаем стикеры
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

# Загружаем данные при запуске
settings = load_settings()
STICKER_IDS = load_stickers()

async def start(update: Update, context):
    if not update.message:
        return
    await update.message.reply_text(
        "🤖 Стикер-бот\n\n"
        "Команды:\n"
        "/sticker - принудительно отправить стикер\n"
        "/freq 50 - установить частоту (1-100%)\n"
        "/status - текущие настройки\n"
        "/stats - статистика стикеров\n"
        "/clear - очистить базу стикеров\n\n"
        "Бот отзывается на: бот, 1548, Инкогнито, 48, 405, коза\n"
        "Перешли стикеры чтобы добавить их в базу!"
    )

async def force_sticker(update: Update, context):
    if not update.message:
        return
        
    if not STICKER_IDS:
        await update.message.reply_text("❌ В базе нет стикеров! Перешли мне стикеры сначала.")
        return
    
    random_sticker = random.choice(STICKER_IDS)
    await update.message.reply_sticker(random_sticker)
    await update.message.reply_text("🎯 Стикер отправлен!")

async def set_frequency(update: Update, context):
    if not update.message:
        return
        
    if not context.args:
        await update.message.reply_text(
            f"📊 Текущая частота: {int(settings['probability'] * 100)}%\n"
            "Используйте: /freq 50 (где 50 = 50% шанс)\n"
            "Диапазон: от 1 до 100%"
        )
        return
    
    try:
        new_prob_percent = int(context.args[0])
        if 1 <= new_prob_percent <= 100:
            settings["probability"] = new_prob_percent / 100.0
            save_settings()
            await update.message.reply_text(
                f"✅ Частота установлена: {new_prob_percent}%\n"
                f"Теперь бот будет отправлять стикеры с шансом {new_prob_percent}%"
            )
        else:
            await update.message.reply_text("❌ Частота должна быть от 1 до 100%")
    except ValueError:
        await update.message.reply_text("❌ Используйте число: /freq 50")

async def show_status(update: Update, context):
    if not update.message:
        return
        
    prob_percent = int(settings['probability'] * 100)
    
    status_text = (
        f"📊 Статус бота:\n"
        f"• Стикеров в базе: {len(STICKER_IDS)}\n"
        f"• Частота отправки: {prob_percent}%\n"
        f"• Шанс отправки: {prob_percent} из 100 сообщений\n\n"
        f"Команды:\n"
        f"/sticker - принудительно отправить стикер\n"
        f"/freq - изменить частоту (1-100%)\n"
        f"/stats - статистика стикеров"
    )
    await update.message.reply_text(status_text)

async def add_sticker(update: Update, context):
    if not update.message:
        return
        
    if update.message.sticker:
        sticker_id = update.message.sticker.file_id
        if sticker_id not in STICKER_IDS:
            STICKER_IDS.append(sticker_id)
            save_stickers()
            await update.message.reply_text(f"✅ Стикер добавлен! Всего: {len(STICKER_IDS)}")
        else:
            await update.message.reply_text("⚠️ Этот стикер уже есть в базе")

async def send_sticker(update: Update, context):
    if not update.message:
        return
        
    if STICKER_IDS and random.random() < settings["probability"]:
        random_sticker = random.choice(STICKER_IDS)
        await update.message.reply_sticker(random_sticker)

async def show_stats(update: Update, context):
    if not update.message:
        return
        
    if STICKER_IDS:
        prob_percent = int(settings['probability'] * 100)
        await update.message.reply_text(
            f"📊 Статистика:\n"
            f"• Стикеров в базе: {len(STICKER_IDS)}\n"
            f"• Частота отправки: {prob_percent}%\n"
            f"• Шанс: {prob_percent} из 100 сообщений"
        )
    else:
        await update.message.reply_text("📊 В базе пока нет стикеров. Перешли мне стикеры!")

async def clear_stickers(update: Update, context):
    if not update.message:
        return
        
    STICKER_IDS.clear()
    save_stickers()
    await update.message.reply_text("🗑️ База стикеров очищена!")

async def handle_all_messages(update: Update, context):
    if not update.message:
        return
    
    if update.message.text:
        message_text = update.message.text.lower()
        
        trigger_words = ["бот", "1548", "инкогнито", "48", "405", "коза"]
        found_trigger = any(trigger in message_text for trigger in trigger_words)
        
        if found_trigger:
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
            response = random.choice(responses)
            await update.message.reply_text(response)
            return
        
        if STICKER_IDS and random.random() < settings["probability"]:
            random_sticker = random.choice(STICKER_IDS)
            await update.message.reply_sticker(random_sticker)

def main():
    application = Application.builder().token(TOKEN).build()
    
    # Команды
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("sticker", force_sticker))
    application.add_handler(CommandHandler("freq", set_frequency))
    application.add_handler(CommandHandler("status", show_status))
    application.add_handler(CommandHandler("stats", show_stats))
    application.add_handler(CommandHandler("clear", clear_stickers))
    # Обработчики сообщений
    application.add_handler(MessageHandler(filters.Sticker.ALL, add_sticker))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_all_messages))
    
    print(f"✅ Бот запущен на Render!")
    print(f"📊 Стикеров в базе: {len(STICKER_IDS)}")
    print(f"🎯 Частота отправки: {int(settings['probability'] * 100)}%")
    
    application.run_polling()

if __name__ == "__main__":
    main()
