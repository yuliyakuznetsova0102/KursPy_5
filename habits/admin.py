from django.contrib import admin
from .models import Habit, TelegramUser, HabitCompletion


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('action', 'time', 'place', 'user', 'is_pleasant', 'is_public')
    list_filter = ('is_pleasant', 'is_public')
    search_fields = ('action', 'place')


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'chat_id', 'username')
    search_fields = ('user__email', 'username')


@admin.register(HabitCompletion)
class HabitCompletionAdmin(admin.ModelAdmin):
    list_display = ('habit', 'date')
    list_filter = ('date',)
