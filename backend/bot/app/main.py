import telebot
from telebot import types
from app.core.config import settings
from app.handlers import start, habits, tracking

bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)

# Регистрация обработчиков
start.register_handlers(bot)
habits.register_handlers(bot)
tracking.register_handlers(bot)

if __name__ == "__main__":
    bot.polling(none_stop=True)