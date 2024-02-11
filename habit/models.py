from django.db import models


class Place(models.Model):
    name_of_place = models.CharField(max_length=150, verbose_name='Название места')
    comments = models.TextField(verbose_name='Комментарии')

    def __str__(self):
        return f'{self.name_of_place}'

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'
