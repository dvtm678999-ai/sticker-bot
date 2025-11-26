import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

print("=== БОТ ЗАПУСКАЕТСЯ ===")

async def start(update: Update, context):
    await update.message.reply_text("🤖 Бот работает на Render!")

async def handle_message(update: Update, context):
    if update.message.text:
        text = update.message.text.lower()
        if any(word in text for word in ["бот", "1548", "инкогнито"]):
            await update.message.reply_text("иди нахуй")

def main():
    try:
        TOKEN = os.environ.get("BOT_TOKEN")
        if not TOKEN:
            print("❌ ОШИБКА: BOT_TOKEN не найден!")
            return
        
        print(f"✅ Токен получен: {TOKEN[:10]}...")
        
        # Создаем приложение
        application = Application.builder().token(TOKEN).build()
        
        # Добавляем обработчики
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        print("✅ Бот запускается...")
        
        # Запускаем бота
        application.run_polling()
        
    except Exception as e:
        print(f"❌ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
