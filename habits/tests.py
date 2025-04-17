from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from .models import Habit


class HabitTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='user@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            email='other@example.com',
            password='otherpass123'
        )

        # Приятная привычка
        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            place='Дома',
            time='08:00:00',
            action='Пить кофе',
            is_pleasant=True,
            duration=60,
            is_public=True
        )

        # Полезная привычка с вознаграждением
        self.useful_habit_reward = Habit.objects.create(
            user=self.user,
            place='Парк',
            time='09:00:00',
            action='Бегать',
            is_pleasant=False,
            reward='Кофе',
            duration=120,
            is_public=False
        )

        # Полезная привычка со связанной привычкой
        self.useful_habit_linked = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='19:00:00',
            action='Читать',
            is_pleasant=False,
            linked_habit=self.pleasant_habit,
            duration=90,
            is_public=True
        )

    def test_create_pleasant_habit(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('habits-list')
        data = {
            'place': 'Дома',
            'time': '07:00:00',
            'action': 'Медитировать',
            'is_pleasant': True,
            'duration': 60
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 4)

    def test_create_useful_habit_with_reward(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('habits-list')
        data = {
            'place': 'Спортзал',
            'time': '18:00:00',
            'action': 'Тренироваться',
            'is_pleasant': False,
            'reward': 'Смузи',
            'duration': 120
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_useful_habit_with_linked_habit(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('habits-list')
        data = {
            'place': 'Работа',
            'time': '13:00:00',
            'action': 'Гулять',
            'is_pleasant': False,
            'linked_habit': self.pleasant_habit.id,
            'duration': 90
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_habit_creation(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('habits-list')
        # Попытка создать привычку с длительностью > 120 секунд
        data = {
            'place': 'Дом',
            'time': '23:00:00',
            'action': 'Смотреть сериал',
            'is_pleasant': True,
            'duration': 121
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_habits_list(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('habits-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)

    def test_get_public_habits(self):
        self.client.force_authenticate(user=self.other_user)
        url = f"{reverse('habits-list')}?public=true"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # 2 публичные привычки

    def test_update_habit(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('habits-detail', args=[self.useful_habit_reward.id])
        data = {'action': 'Бегать быстро'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.useful_habit_reward.refresh_from_db()
        self.assertEqual(self.useful_habit_reward.action, 'Бегать быстро')

    def test_delete_habit(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('habits-detail', args=[self.useful_habit_reward.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 2)

    def test_habit_str_representation(self):
        self.assertEqual(
            str(self.pleasant_habit),
            "Я буду Пить кофе в 08:00:00 в Дома"
        )

    def test_validate_pleasant_habit_with_reward(self):
        habit = Habit(
            user=self.user,
            place='Тест',
            time='12:00:00',
            action='Тест',
            is_pleasant=True,
            reward='Не должно быть',
            duration=60
        )
        with self.assertRaises(Exception):
            habit.full_clean()

    def test_validate_linked_habit_not_pleasant(self):
        habit = Habit(
            user=self.user,
            place='Тест',
            time='12:00:00',
            action='Тест',
            is_pleasant=False,
            linked_habit=self.useful_habit_reward,  # Не приятная привычка
            duration=60
        )
        with self.assertRaises(Exception):
            habit.full_clean()
