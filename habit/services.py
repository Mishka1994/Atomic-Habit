from django_celery_beat.models import IntervalSchedule, PeriodicTask


def create_schedule_set(habit_item):
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=habit_item.frequency_in_days,
        period=IntervalSchedule.DAYS
    )

    PeriodicTask.objects.create(
        interval=schedule,
        name=f'Habit of {habit_item.user}',
        task='habit.tasks.sending_remainder',
        args=[habit_item.id]
    )
