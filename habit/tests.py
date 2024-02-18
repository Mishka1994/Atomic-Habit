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

    def test_create_habit_with_invalid_data(self):
        """Тест на создание привычки с невалидными данными"""

        data_with_invalid_frequency = {
            'place': self.place.pk,
            'time': '10:00:00',
            'action': 'Слушать музыку',
            'sign_pleasant_habit': True,
            'frequency_in_days': 14,
            'time_to_complete': '00:00:50'
        }

        data_with_invalid_time_to_complete = {
            'place': self.place.pk,
            'time': '10:00:00',
            'action': 'Слушать музыку',
            'sign_pleasant_habit': True,
            'frequency_in_days': 2,
            'time_to_complete': '05:00:00'
        }

        first_response = self.client.post(
            reverse('habit:habit-create'),
            data=data_with_invalid_frequency
        )

        self.assertEqual(
            first_response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            first_response.json(),
            {'frequency_in_days': ['Периодичность должна быть больше нуля и меньше или равна 7!']}
        )

        second_response = self.client.post(
            reverse('habit:habit-create'),
            data=data_with_invalid_time_to_complete
        )

        self.assertEqual(
            second_response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            second_response.json(),
            {'time_to_complete': ['Продолжительность выполнения не может быть больше 2 минут!']}
        )

    def test_nice_habit_create(self):
        """Тест на создание приятной привычки"""

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

    def test_incorrect_associated_habit(self):
        """Тест на создание полезной привычки с некорректной связанной привычкой"""
        self.habit = Habit.objects.create(
            place=self.place,
            time="10:00:00",
            action='Дыхательная медитация',
            frequency_in_days=1,
            time_to_complete='00:00:50',
            reward='Съесть пирожное'
        )

        data = {
            "place": self.place.pk,
            "time": "10:00:00",
            "action": "Бег в 10.00",
            "sign_pleasant_habit": False,
            "frequency_in_days": 1,
            "time_to_complete": "00:01:00",
            "associated_habit": self.habit.pk
        }

        response = self.client.post(
            reverse('habit:habit-create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            ['В связанные привычки можно указывать только приятные привычки!']
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

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            ['Нельзя указывать награду и связанную привычку одновременно!']
        )

    def test_update_habit(self):
        """Тест на обновление приятной привычки"""
        self.habit = Habit.objects.create(
            user=self.user,
            place=self.place,
            time='10:00:00',
            action='Слушать музыку',
            sign_pleasant_habit=True,
            frequency_in_days=1,
            time_to_complete='00:01:00'
        )
        data = {'action': 'Слушать музыку в наушниках'}

        response = self.client.patch(
            reverse('habit:habit-update', kwargs={'pk': self.habit.pk}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json().get('action'),
            'Слушать музыку в наушниках'
        )

    def test_incorrect_update_habit(self):
        """Тест на некорректное обновление приятной привычки"""
        self.habit = Habit.objects.create(
            user=self.user,
            place=self.place,
            time='10:00:00',
            action='Слушать музыку',
            sign_pleasant_habit=True,
            frequency_in_days=1,
            time_to_complete='00:01:00'
        )

        self.useful_habit = Habit.objects.create(
            place=self.place,
            time='09:00:00',
            action='Бег в 10:00',
            frequency_in_days=2,
            time_to_complete='00:01:55'
        )

        data_with_reward = {'reward': 'Смотреть сериал 1 час'}
        data_with_assertion_habit = {'associated_habit': self.useful_habit.pk}

        first_response = self.client.patch(
            reverse('habit:habit-update', kwargs={'pk': self.habit.pk}),
            data=data_with_reward
        )

        second_response = self.client.patch(
            reverse('habit:habit-update', kwargs={'pk': self.habit.pk}),
            data=data_with_assertion_habit
        )

        self.assertEqual(
            first_response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            first_response.json(),
            ['У приятной привычки нельзя указывать награду!']
        )

        self.assertEqual(
            second_response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            second_response.json(),
            ['У приятной привычки не может быть связанной привычки!']
        )

    def test_update_useful_habit(self):
        """Тест на обновление полезной привычки"""
        self.habit = Habit.objects.create(
            user=self.user,
            place=self.place,
            time='10:00:00',
            action='Бег в 10:00',
            sign_pleasant_habit=False,
            frequency_in_days=2,
            time_to_complete='00:01:00',
            reward='Смотреть сериал 1 час',

        )

        data = {'reward': 'Купить пирожное'}

        response = self.client.patch(
            reverse('habit:habit-update', kwargs={'pk': self.habit.pk}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json().get('reward'),
            'Купить пирожное'
        )

    def test_update_useful_habit_with_reward(self):
        """Тест на некорректное обновление полезной привычки с наградой"""
        self.useful_habit = Habit.objects.create(
            user=self.user,
            place=self.place,
            time='10:00:00',
            action='Бег в 10:00',
            sign_pleasant_habit=False,
            frequency_in_days=2,
            time_to_complete='00:01:00',
            reward='Смотреть сериал 1 час',

        )

        self.nice_habit = Habit.objects.create(
            user=self.user,
            place=self.place,
            time='10:00:00',
            action='Слушать музыку',
            sign_pleasant_habit=True,
            frequency_in_days=1,
            time_to_complete='00:01:00'
        )

        data = {'associated_habit': self.nice_habit.pk}

        response = self.client.patch(
            reverse('habit:habit-update', kwargs={'pk': self.useful_habit.pk}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            ['Нельзя указывать награду и связанную привычку одновременно!']
        )

    def test_update_useful_habit_with_associated_habit(self):
        """Тест на некорректное обновление полезной привычки со связанной привычкой"""
        self.nice_habit = Habit.objects.create(
            user=self.user,
            place=self.place,
            time='10:00:00',
            action='Слушать музыку',
            sign_pleasant_habit=True,
            frequency_in_days=1,
            time_to_complete='00:01:00'
        )

        self.useful_habit = Habit.objects.create(
            user=self.user,
            place=self.place,
            time='10:00:00',
            action='Бег в 10:00',
            sign_pleasant_habit=False,
            frequency_in_days=2,
            time_to_complete='00:01:00',
            associated_habit=self.nice_habit

        )

        data = {'reward': 'Смотреть сериал 1 час'}

        response = self.client.patch(
            reverse('habit:habit-update', kwargs={'pk': self.useful_habit.pk}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_list_users_habit(self):
        self.nice_habit = Habit.objects.create(
            user=self.user,
            place=self.place,
            time='10:00:00',
            action='Слушать музыку',
            sign_pleasant_habit=True,
            frequency_in_days=1,
            time_to_complete='00:01:00'
        )

        response = self.client.get(
            reverse('habit:habit-list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_list_public_habit(self):
        self.nice_habit = Habit.objects.create(
            user=self.user,
            place=self.place,
            time='10:00:00',
            action='Слушать музыку',
            sign_pleasant_habit=True,
            frequency_in_days=1,
            time_to_complete='00:01:00',
            is_public=False
        )

        response = self.client.get(
            reverse('habit:public_habit-list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            []
        )
