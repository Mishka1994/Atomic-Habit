from rest_framework import serializers

from habit.models import Place, Habit
from habit.validators import FrequencyHabitExecution, DurationHabit


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'


class HabitSerializer(serializers.ModelSerializer):
    frequency_in_days = serializers.IntegerField(validators=[FrequencyHabitExecution(),])
    time_to_complete = serializers.TimeField(validators=[DurationHabit(),])

    class Meta:
        model = Habit
        fields = '__all__'

    def create(self, validated_data):
        if validated_data['sign_pleasant_habit']:
            # Проверка на наличие связанной привычки у приятной привычки
            if validated_data.get('associated_habit') is not None:
                raise serializers.ValidationError('У приятной привычки не может быть связанной привычки!')
            # Проверка на наличие награды у приятной привычки
            elif validated_data.get('reward'):
                raise serializers.ValidationError('У приятной привычки нельзя указывать награду!')

        elif not validated_data['sign_pleasant_habit'] and validated_data.get('associated_habit') is not None:
            # Проверка на указание награды, при указанной связанной привычке
            if len(validated_data['reward']) != 'Нет награды':
                raise serializers.ValidationError('Если указана связанная привычка, награду указывать нельзя!')

        habit_item = Habit.objects.create(**validated_data)
        return habit_item
