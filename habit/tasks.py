import requests

from config import settings
from config.celery import app
from habit.models import Habit


@app.task
def sending_remainder(habit_id):
    habit = Habit.objects.get(id=habit_id)
    message = f'Напоминание! Нужно выполнить привычку {habit.action}, в {habit.time} в {habit.place}'
    requests.post(
        url=f'{settings.URL_FOR_TELEGRAM}{settings.TELEGRAM_BOT_TOKEN}/sendMessage',
        data={
            'chat_id': habit.user.telegram_id,
            'text': message
        }
    )
