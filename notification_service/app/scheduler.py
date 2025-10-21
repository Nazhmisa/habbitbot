import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models import Habit, User, HabitCompletion
from datetime import datetime, date, timedelta
import telebot

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)

def send_daily_reminders():
    db = SessionLocal()
    try:
        users = db.query(User).filter(User.is_active == True).all()
        
        for user in users:
            habits = db.query(Habit).filter(
                Habit.user_id == user.id,
                Habit.is_active == True
            ).all()
            
            if habits:
                message = "📋 Ваши привычки на сегодня:\n\n"
                for habit in habits:
                    completion = db.query(HabitCompletion).filter(
                        HabitCompletion.habit_id == habit.id,
                        HabitCompletion.completion_date == date.today()
                    ).first()
                    
                    status = "✅" if completion and completion.is_completed else "⬜"
                    message += f"{status} {habit.title}\n"
                
                try:
                    bot.send_message(user.telegram_id, message)
                except Exception as e:
                    print(f"Error sending message to user {user.telegram_id}: {e}")
                    
    finally:
        db.close()

def transfer_uncompleted_habits():
    db = SessionLocal()
    try:
        habits = db.query(Habit).filter(Habit.is_active == True).all()
        
        for habit in habits:
            # Подсчитываем количество выполнений за последние 21 день
            completions_count = db.query(HabitCompletion).filter(
                HabitCompletion.habit_id == habit.id,
                HabitCompletion.is_completed == True,
                HabitCompletion.completion_date >= date.today() - timedelta(days=21)
            ).count()
            
            # Если привычка выполнена менее 21 раза, создаем запись на завтра
            if completions_count < habit.target_days:
                tomorrow_completion = HabitCompletion(
                    habit_id=habit.id,
                    completion_date=date.today() + timedelta(days=1),
                    is_completed=False
                )
                db.add(tomorrow_completion)
        
        db.commit()
        
    finally:
        db.close()