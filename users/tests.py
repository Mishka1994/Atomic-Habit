from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):
    def setUp(self):
        self.data = {
            'id': 1,
            'email': 'test@mail.ru',
            'first_name': 'test',
            'last_name': 'user',
            'telegram_id': '111',
            'password': 'qwerty'

        }

    def test_create_user(self):
        """Тест на создание пользователя"""

        response = self.client.post(
            reverse('users:user-create'),
            data=self.data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'result': 'Пользователь создан'}
        )
