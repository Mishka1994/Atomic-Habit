from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        user = User.objects.create(
            email=request.data['email'],

        )
        user.set_password(request.data['password'])
        user.save()

        return Response({'result': 'Пользователь создан'})
