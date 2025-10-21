import time
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_URL = os.getenv("API_URL", "http://backend:8000")

def check_backend():
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend доступен")
            return True
        else:
            print("❌ Backend не отвечает")
            return False
    except Exception as e:
        print(f"❌ Backend недоступен: {e}")
        return False

def send_test_notification():
    print("🔔 Проверка уведомлений...")
    if check_backend():
        print("✅ Система работает нормально")

if __name__ == "__main__":
    print("⏰ Сервис уведомлений запущен...")
    
    # Простой цикл вместо APScheduler для начала
    counter = 0
    while True:
        send_test_notification()
        counter += 1
        print(f"🔁 Итерация #{counter}")
        time.sleep(30)  # Проверка каждые 30 секунд