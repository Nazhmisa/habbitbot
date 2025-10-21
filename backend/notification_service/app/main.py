from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from app.scheduler import send_daily_reminders, transfer_uncompleted_habits

scheduler = BlockingScheduler()

# Ежедневные напоминания в 9:00
scheduler.add_job(
    send_daily_reminders,
    CronTrigger(hour=9, minute=0),
    id='daily_reminders'
)

# Перенос привычек в 23:59
scheduler.add_job(
    transfer_uncompleted_habits,
    CronTrigger(hour=23, minute=59),
    id='transfer_habits'
)

if __name__ == "__main__":
    try:
        scheduler.start()
    except KeyboardInterrupt:
        pass