from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated


from habit.models import Place, Habit
from habit.paginators import HabitPaginator
from habit.permissions import IsOwner
from habit.serializers import PlaceSerializer, HabitCreateSerializer, HabitUpdateSerializer, HabitSerializer
from habit.services import create_schedule_set


class PlaceCreateView(CreateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticated]


class HabitCreateView(CreateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_habit = serializer.save()
        new_habit.user = self.request.user
        create_schedule_set(new_habit)
        new_habit.save()


class HabitUpdateView(UpdateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class HabitDeleteView(DestroyAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class ListUserHabitView(ListAPIView):
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user.id)


class ListPublicHabit(ListAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)
