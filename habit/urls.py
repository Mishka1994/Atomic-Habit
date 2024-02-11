from django.urls import path

from habit.apps import HabitConfig
from habit.views import PlaceCreateView

app_name = HabitConfig.name

urlpatterns = [
    path('place/create/', PlaceCreateView.as_view(), name='place-create'),

]
