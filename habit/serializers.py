from rest_framework import serializers

from habit.models import Place, Habit
from habit.validators import DurationHabit, FrequencyHabit


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'


class HabitCreateSerializer(serializers.ModelSerializer):
    frequency_in_days = serializers.IntegerField(validators=[FrequencyHabit(), ])
    time_to_complete = serializers.TimeField(validators=[DurationHabit(), ])

    class Meta:
        model = Habit
        fields = '__all__'

    def create(self, validated_data):
        # Валидация приятной привычки
        if validated_data['sign_pleasant_habit']:
            # Проверка на наличие связанной привычки у приятной привычки
            if validated_data.get('associated_habit') is not None:
                raise serializers.ValidationError(
                    'У приятной привычки не может быть связанной привычки!'
                )
            # Проверка на наличие награды у приятной привычки
            elif validated_data.get('reward'):
                raise serializers.ValidationError(
                    'У приятной привычки нельзя указывать награду!'
                )

        # Валидация полезной привычки
        elif not validated_data['sign_pleasant_habit']:
            # Проверка на указанный вид привычки(может быть только приятная)
            if validated_data.get('associated_habit'):
                associated_habit = validated_data['associated_habit']
                if not associated_habit.sign_pleasant_habit:
                    raise serializers.ValidationError('В связанные привычки можно указывать только приятные привычки!')

                # Проверка на одновременное указание награды и связанной привычки
                elif validated_data.get('reward') and validated_data.get('associated_habit'):
                    raise serializers.ValidationError('Нельзя указывать награду и связанную привычку одновременно!')

        habit_item = Habit.objects.create(**validated_data)
        return habit_item


class HabitUpdateSerializer(serializers.ModelSerializer):
    frequency_in_days = serializers.IntegerField(validators=[FrequencyHabit(),])
    time_to_complete = serializers.TimeField(validators=[DurationHabit(), ])

    class Meta:
        model = Habit
        fields = '__all__'

    def update(self, instance, validated_data):
        # Валидация приятной привычки
        if instance.sign_pleasant_habit:
            # Проверка на добавление награды
            if validated_data.get('reward'):
                raise serializers.ValidationError('У приятной привычки нельзя указывать награду!')
            # Проверка на добавление связанной привычки
            elif validated_data.get('associated_habit'):
                raise serializers.ValidationError('У приятной привычки не может быть связанной привычки!')
        # Валидация полезной привычки
        elif not instance.sign_pleasant_habit:
            # Проверка добавляемой связанной привычки(можно добавить только приятную привычку)
            if validated_data.get('associated_habit'):
                associated_habit = validated_data['associated_habit']
                if not associated_habit.sign_pleasant_habit:
                    raise serializers.ValidationError('В связанные привычки можно указывать только приятные привычки!')
            # Проверка на добавление награды, если есть связанная привычка и
            # на добавление связанной привычки если есть награда
            if (validated_data.get('reward') and instance.associated_habit is not None) or \
                    validated_data.get('associated_habit') and instance.reward != 'Нет награды!':
                raise serializers.ValidationError('Нельзя указывать награду и связанную привычку одновременно!')

        instance.place = validated_data.get('place', instance.place)
        instance.user = validated_data.get('user', instance.user)
        instance.time = validated_data.get('time', instance.time)
        instance.action = validated_data.get('action', instance.action)
        instance.sign_pleasant_habit = validated_data.get('sign_pleasant_habit', instance.sign_pleasant_habit)
        instance.associated_habit = validated_data.get('associated_habit', instance.associated_habit)
        instance.frequency_in_days = validated_data.get('frequency_in_days', instance.frequency_in_days)
        instance.reward = validated_data.get('reward', instance.reward)
        instance.time_to_complete = validated_data.get('time_to_complete', instance.time_to_complete)
        instance.is_public = validated_data.get('is_public', instance.is_public)

        return instance
