from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from habit.models import Habit, Place
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='test_user@mail.ru',
            telegram_id='1111'
        )
        self.user.set_password('12345')
        self.user.save()

        response = self.client.post(
            reverse('users:token_obtain_pair'),
            data={
                'email': 'test_user@mail.ru',
                'password': '12345'
            }
        )

        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.place = Place.objects.create(
            name_of_place="test_place",
        )

    def test_create_place(self):
        """Тест на создание места выполнения привычки"""
        data = {
            "name_of_place": "test_place",
            "comments": "test_comments"
        }

        response = self.client.post(
            reverse('habit:place-create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json().get('name_of_place'),
            "test_place"
        )

    def test_nice_habit_create(self):
        """Тест на создание приятной привычки"""
        self.place = Place.objects.create(
            name_of_place="test_place",
        )

        data = {
            "place": self.place.pk,
            "time": "10:00:00",
            "action": "Слушать музыку",
            "sign_pleasant_habit": True,
            "frequency_in_days": 1,
            "time_to_complete": "00:01:00"
        }

        response = self.client.post(
            reverse("habit:habit-create"),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json().get('action'),
            "Слушать музыку"
        )

        self.assertTrue(response.json().get('sign_pleasant_habit'))

    def test_incorrect_nice_habit_create(self):
        """Тест на создание приятной привычки с указанием связанной привычки  """

        self.habit = Habit.objects.create(
            place=self.place,
            time="20:00:00",
            action='Test project',
            frequency_in_days=2,
            time_to_complete="00:00:30",
            reward="Смотреть сериал"
        )

        data_with_associated_habit = {
            "place": self.place.pk,
            "time": "10:00:00",
            "action": "Слушать музыку",
            "sign_pleasant_habit": True,
            "frequency_in_days": 1,
            "time_to_complete": "00:01:00",
            "associated_habit": self.habit.pk
        }

        response = self.client.post(
            reverse('habit:habit-create'),
            data=data_with_associated_habit
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            ["У приятной привычки не может быть связанной привычки!"]
        )

    def test_incorrect_habit_create(self):
        """Тест на создание некорректной приятной привычки с указанием награды"""

        data_with_reward = {
            "place": self.place.pk,
            "time": "10:00:00",
            "action": "Слушать музыку",
            "sign_pleasant_habit": True,
            "frequency_in_days": 1,
            "time_to_complete": "00:01:00",
            "reward": "Смотреть сериал"
        }

        response = self.client.post(
            reverse('habit:habit-create'),
            data=data_with_reward
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            ['У приятной привычки нельзя указывать награду!']
        )

    def test_useful_habit_create(self):
        """Тест на создание полезной привычки"""
        data = {
            "place": self.place.pk,
            "time": "10:00:00",
            "action": "Бег в 10.00",
            "sign_pleasant_habit": False,
            "frequency_in_days": 1,
            "time_to_complete": "00:01:00",
            "reward": "Смотреть сериал"
        }

        response = self.client.post(
            reverse('habit:habit-create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json().get('action'),
            "Бег в 10.00"
        )

    def test_incorrect_useful_habit_create(self):
        """Тест на создание некорректной полезной привычки"""
        self.habit = Habit.objects.create(
            place=self.place,
            time='10:00:00',
            action='Слушать музыку',
            sign_pleasant_habit=True,
            frequency_in_days=1,
            time_to_complete="00:01:00"
        )

        data = {
            "place": self.place.pk,
            "time": "10:00:00",
            "action": "Бег в 10.00",
            "sign_pleasant_habit": False,
            "frequency_in_days": 1,
            "time_to_complete": "00:01:00",
            "reward": "Смотреть сериал",
            "associated_habit": self.habit.pk
        }

        response = self.client.post(
            reverse('habit:habit-create'),
            data=data
        )
        #print(response.json())
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            ['Если указана связанная привычка, награду указывать нельзя!']
        )

