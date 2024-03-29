# Generated by Django 5.0.2 on 2024-02-11 13:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habit', '0002_habit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='associated_habit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='habit.habit', verbose_name='Связанная привычка'),
        ),
        migrations.AlterField(
            model_name='habit',
            name='place',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='place', to='habit.place', verbose_name='Место'),
        ),
        migrations.AlterField(
            model_name='habit',
            name='reward',
            field=models.CharField(default='Нет награды', max_length=250, verbose_name='Вознаграждение'),
        ),
        migrations.AlterField(
            model_name='habit',
            name='sign_pleasant_habit',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Признак приятной привычки'),
        ),
    ]
