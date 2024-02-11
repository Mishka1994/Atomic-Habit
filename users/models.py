from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None

    email = models.EmailField(verbose_name='Почта', unique=True)
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    telegram_id = models.CharField(max_length=50, verbose_name='ID телеграмма')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
