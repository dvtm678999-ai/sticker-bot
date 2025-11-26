import os
import time
import sys

print("=== БОТ ЗАПУСКАЕТСЯ ===")

try:
    # Проверяем базовые импорты
    from telegram.ext import Updater, CommandHandler
    print("✅ Библиотеки загружены")
    
    TOKEN = os.environ.get("BOT_TOKEN")
    if not TOKEN:
        print("❌ ОШИБКА: BOT_TOKEN не найден!")
        sys.exit(1)
    
    print(f"✅ Токен получен: {TOKEN[:10]}...")
    
    def start(update, context):
        update.message.reply_text("🤖 Бот работает!")
    
    updater = Updater(TOKEN, use_context=True)
    updater.dispatcher.add_handler(CommandHandler("start", start))
    
    print("✅ Бот запускается...")
    updater.start_polling()
    print("✅ Бот успешно запущен!")
    
    # Держим бота активным
    updater.idle()
    
except Exception as e:
    print(f"❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
    print(f"Тип ошибки: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
