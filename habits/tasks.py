import requests
from django.conf import settings
from celery import shared_task
from django.utils import timezone
from .models import Habit, HabitCompletion

TELEGRAM_API_URL = f'https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/'


@shared_task
def send_telegram_notification(chat_id, message):
    url = TELEGRAM_API_URL + 'sendMessage'
    data = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    response = requests.post(url, data=data)
    return response.json()


@shared_task
def send_habit_reminders():
    now = timezone.now()
    current_time = now.time()

    habits = Habit.objects.filter(time__hour=current_time.hour,
                                  time__minute=current_time.minute)

    for habit in habits:
        last_completed = habit.completions.last()
        if last_completed:
            days_passed = (now.date() - last_completed.date).days
            if days_passed < habit.periodicity:
                continue

        message = (
            f"⏰ Напоминание о привычке!\n\n"
            f"*Действие:* {habit.action}\n"
            f"*Место:* {habit.place}\n"
            f"*Время на выполнение:* {habit.duration} секунд\n"
        )

        if habit.reward:
            message += f"*Вознаграждение:* {habit.reward}\n"
        elif habit.linked_habit:
            message += f"*Вознаграждение:* {habit.linked_habit.action}\n"

        send_telegram_notification.delay(habit.user.telegram.chat_id, message)
        HabitCompletion.objects.create(habit=habit)
