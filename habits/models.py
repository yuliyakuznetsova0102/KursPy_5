from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User


class Habit(models.Model):
    DAILY = 1
    WEEKLY = 7

    PERIODICITY_CHOICES = [
        (DAILY, 'Ежедневно'),
        (WEEKLY, 'Еженедельно'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    place = models.CharField(max_length=255, verbose_name='Место выполнения')
    time = models.TimeField(verbose_name='Время выполнения')
    action = models.CharField(max_length=255, verbose_name='Действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='Признак приятной привычки')
    linked_habit = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name='Связанная привычка')
    periodicity = models.PositiveSmallIntegerField(default=DAILY, choices=PERIODICITY_CHOICES,
                                                   validators=[MinValueValidator(1), MaxValueValidator(7)],
                                                   verbose_name='Периодичность (дни)')
    reward = models.CharField(max_length=255, blank=True, null=True, verbose_name='Вознаграждение')
    duration = models.PositiveIntegerField(validators=[MaxValueValidator(120)],
                                           verbose_name='Время на выполнение (секунды)')
    is_public = models.BooleanField(default=False, verbose_name='Признак публичности')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"Я буду {self.action} в {self.time} в {self.place}"

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['-created_at']


class TelegramUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='telegram')
    chat_id = models.CharField(max_length=50, verbose_name='ID чата в Telegram')
    username = models.CharField(max_length=100, blank=True, null=True, verbose_name='Username в Telegram')

    def __str__(self):
        return f"{self.user.email} - {self.chat_id}"

    class Meta:
        verbose_name = 'Telegram пользователь'
        verbose_name_plural = 'Telegram пользователи'


class HabitCompletion(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='completions')
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Выполнение привычки'
        verbose_name_plural = 'Выполнения привычек'
