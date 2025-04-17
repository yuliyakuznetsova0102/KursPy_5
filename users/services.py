from django.core.mail import send_mail
from django.conf import settings


def send_welcome_email(user):
    subject = 'Добро пожаловать в Habit Tracker!'
    message = f'Привет, {user.username}!\n\nСпасибо за регистрацию в нашем сервисе.'
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
