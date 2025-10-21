import requests
from telebot import types
from app.services.api_client import APIClient

def register_handlers(bot):
    @bot.message_handler(commands=['habits'])
    def show_habits(message):
        api_client = APIClient()
        habits = api_client.get_habits(message.from_user.id)
        
        if not habits:
            bot.send_message(message.chat.id, "У вас пока нет привычек. Создайте первую!")
            return
        
        markup = types.InlineKeyboardMarkup()
        for habit in habits:
            btn = types.InlineKeyboardButton(
                f"✅ {habit['title']}" if habit.get('completed_today') else f"⬜ {habit['title']}",
                callback_data=f"track_{habit['id']}"
            )
            markup.add(btn)
        
        markup.add(types.InlineKeyboardButton("➕ Добавить привычку", callback_data="add_habit"))
        bot.send_message(message.chat.id, "Ваши привычки на сегодня:", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data == "add_habit")
    def add_habit_callback(call):
        msg = bot.send_message(call.message.chat.id, "Введите название новой привычки:")
        bot.register_next_step_handler(msg, process_habit_title)

    def process_habit_title(message):
        habit_data = {
            "title": message.text,
            "user_telegram_id": message.from_user.id
        }
        
        api_client = APIClient()
        response = api_client.create_habit(habit_data)
        
        if response:
            bot.send_message(message.chat.id, f"Привычка '{message.text}' создана!")
        else:
            bot.send_message(message.chat.id, "Ошибка при создании привычки")