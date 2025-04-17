from django.test import TestCase
from django.core.exceptions import ValidationError
from users.models import User
from .models import Habit
from .validators import validate_pleasant_habit_fields, validate_reward_or_linked_habit


class HabitValidatorsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='08:00:00',
            action='Кофе',
            is_pleasant=True,
            duration=60
        )

    def test_pleasant_habit_with_reward(self):
        habit = Habit(
            user=self.user,
            place='Тест',
            time='12:00:00',
            action='Тест',
            is_pleasant=True,
            reward='Не должно быть',
            duration=60
        )
        with self.assertRaises(ValidationError):
            validate_pleasant_habit_fields(habit)

    def test_pleasant_habit_with_linked_habit(self):
        habit = Habit(
            user=self.user,
            place='Тест',
            time='12:00:00',
            action='Тест',
            is_pleasant=True,
            linked_habit=self.pleasant_habit,
            duration=60
        )
        with self.assertRaises(ValidationError):
            validate_pleasant_habit_fields(habit)

    def test_reward_and_linked_habit_together(self):
        habit = Habit(
            user=self.user,
            place='Тест',
            time='12:00:00',
            action='Тест',
            is_pleasant=False,
            reward='Награда',
            linked_habit=self.pleasant_habit,
            duration=60
        )
        with self.assertRaises(ValidationError):
            validate_reward_or_linked_habit(habit)

    def test_linked_habit_not_pleasant(self):
        not_pleasant_habit = Habit.objects.create(
            user=self.user,
            place='Тест',
            time='12:00:00',
            action='Тест',
            is_pleasant=False,
            duration=60
        )
        habit = Habit(
            user=self.user,
            place='Тест',
            time='12:00:00',
            action='Тест',
            is_pleasant=False,
            linked_habit=not_pleasant_habit,
            duration=60
        )
        with self.assertRaises(ValidationError):
            validate_reward_or_linked_habit(habit)
