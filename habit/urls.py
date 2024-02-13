from django.urls import path

from habit.apps import HabitConfig
from habit.views import PlaceCreateView, HabitCreateView, HabitUpdateView, HabitDeleteView

app_name = HabitConfig.name

urlpatterns = [
    # Habit
    path('create/', HabitCreateView.as_view(), name='habit-create'),
    path('update/<int:pk>/', HabitUpdateView.as_view(), name='habit-update'),
    path('delete/<int:pk>/', HabitDeleteView.as_view(), name='habit-delete'),

    # Place
    path('place/create/', PlaceCreateView.as_view(), name='place-create'),

]
