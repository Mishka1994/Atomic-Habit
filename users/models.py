from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"null": True, "blank": True}


class User(AbstractUser):
    username = None

    email = models.EmailField(verbose_name='Почта', unique=True)
    first_name = models.CharField(max_length=150, verbose_name='Имя', **NULLABLE)
    last_name = models.CharField(max_length=150, verbose_name='Фамилия', **NULLABLE)
    telegram_id = models.CharField(max_length=50, verbose_name='ID телеграмма', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
