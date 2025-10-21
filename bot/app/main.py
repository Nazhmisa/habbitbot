import telebot
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_URL = os.getenv("API_URL", "http://backend:8000")

if not TELEGRAM_BOT_TOKEN:
    print("❌ TELEGRAM_BOT_TOKEN not found!")
    exit(1)

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Привет! Я бот для трекинга привычек!\n\n"
                         "Доступные команды:\n"
                         "/habits - Мои привычки\n"
                         "/add - Добавить привычку")

@bot.message_handler(commands=['habits'])
def show_habits(message):
    try:
        response = requests.get(f"{API_URL}/health")
        if response.status_code == 200:
            bot.send_message(message.chat.id, "📋 Список привычек:\n\n"
                                             "✅ Читать книгу (15/21)\n"
                                             "⬜ Зарядка (10/21)\n"
                                             "✅ Пить воду (20/21)\n\n"
                                             "Backend работает! 🎉")
        else:
            bot.send_message(message.chat.id, "❌ Backend не отвечает")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка подключения к backend: {e}")

@bot.message_handler(commands=['add'])
def add_habit(message):
    msg = bot.send_message(message.chat.id, "Введите название новой привычки:")
    bot.register_next_step_handler(msg, process_habit_name)

def process_habit_name(message):
    habit_name = message.text
    bot.send_message(message.chat.id, f"✅ Привычка '{habit_name}' добавлена!")

if __name__ == "__main__":
    print("🤖 Бот запущен...")
    bot.polling(none_stop=True)