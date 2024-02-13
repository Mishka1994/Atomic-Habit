from django.db import models

from users.models import NULLABLE, User


class Place(models.Model):
    name_of_place = models.CharField(max_length=150, verbose_name='Название места')
    comments = models.TextField(verbose_name='Комментарии', **NULLABLE)

    def __str__(self):
        return f'{self.name_of_place}'

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='user', **NULLABLE)
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, verbose_name='Место', related_name='place', **NULLABLE)
    time = models.TimeField(verbose_name='Время выполнения привычки')
    action = models.CharField(max_length=250, verbose_name='Действие')
    sign_pleasant_habit = models.BooleanField(default=False, verbose_name='Признак приятной привычки', **NULLABLE)
    associated_habit = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='Связанная привычка', **NULLABLE)
    frequency_in_days = models.IntegerField(verbose_name='Периодичность', default=1)
    reward = models.CharField(max_length=250, verbose_name='Вознаграждение', default='Нет награды')
    time_to_complete = models.TimeField(verbose_name='Время, потраченное на привычку')
    is_public = models.BooleanField(default=False, verbose_name='Признак публичности')

    def __str__(self):
        return f'{self.action} - ({self.user}, {self.place})'

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
