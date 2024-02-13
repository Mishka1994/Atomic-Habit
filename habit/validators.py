import datetime

from rest_framework import serializers


class FrequencyHabitExecution:

    def __call__(self, value):
        if value <= 0 or value > 7:
            raise serializers.ValidationError('Периодичность должна быть больше нуля и меньше или равна 7!')


class DurationHabit:

    def __call__(self, value):
        max_time = datetime.time(minute=2)
        if value > max_time:
            raise serializers.ValidationError('Продолжительность выполнения не может быть больше 2 минут!')
