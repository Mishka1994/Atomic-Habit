from django.urls import path

from habit.apps import HabitConfig
from habit.views import PlaceCreateView, HabitCreateView

app_name = HabitConfig.name

urlpatterns = [
    # Habit
    path('create/', HabitCreateView.as_view(), name='user-create'),

    # Place
    path('place/create/', PlaceCreateView.as_view(), name='place-create'),

]
