from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'telegram_chat_id', 'is_staff')
    list_filter = ('is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Telegram', {'fields': ('telegram_chat_id', 'telegram_username')}),
    )


admin.site.register(User, CustomUserAdmin)
