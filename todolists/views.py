from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .serializers import *
from .models import *
from django.http import *
from django.contrib.auth import get_user_model
from rest_framework import generics, exceptions, request
from django.contrib.auth.models import User


class CreateTag(generics.ListCreateAPIView): #создание тега
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class DeleteTag(generics.DestroyAPIView): #удаление тега
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class UpdateTag(generics.UpdateAPIView): #обновление тега
    queryset = Tag.objects.all()
    serializer_class = TagSerializer



class ListUser(generics.ListAPIView): #список пользователей
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateUser(generics.CreateAPIView): #создание пользователя
    queryset = get_user_model()
    serializer_class = UserSerializer


class DeleteUser(generics.DestroyAPIView): #удаление пользователя
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UpdateUser(generics.UpdateAPIView): #обновить пользователя
    queryset = User.objects.all()
    serializer_class = UserSerializer




class TasklistCreateView(generics.ListCreateAPIView): #создание списка задач
    serializer_class = TasklistSerializer

    def get_queryset(self):
        queryset = Tasklist.objects.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TasklistDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TasklistSerializer

    def get_queryset(self):
        queryset = Tasklist.objects.all()
        return queryset


class TaskCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        list_id = self.kwargs.get('list_id', None)
        if list_id is not None:
            queryset = queryset.filter(tasklist_id = list_id)
        return queryset

    def perform_create(self, serializer):
        list_id = self.kwargs.get('list_id', None)
        try:
            tasklist = Tasklist.objects.get(pk=list_id)
        except Tasklist.DoesNotExist:
            raise NotFound()
        serializer.save(tasklist=tasklist)


class TaskDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        list_id = self.kwargs.get('list_id', None)
        if list_id is not None:
            queryset = queryset.filter(tasklist_id = list_id)
        return queryset

