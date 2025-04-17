# Generated by Django 5.2 on 2025-04-17 10:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("habits", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="habit",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
        migrations.AddField(
            model_name="habitcompletion",
            name="habit",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="completions",
                to="habits.habit",
            ),
        ),
        migrations.AddField(
            model_name="telegramuser",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="telegram",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
