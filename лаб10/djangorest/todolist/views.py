from rest_framework import generics, exceptions, request, viewsets
from .serializers import TaskSerializer, TaskListSerializer, TagSerializer, UserSerializer
from .models import Task, TaskList, Tag
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import permissions
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from django.db.models import Q

class TagCreateView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated,)

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated,)

class TagDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated,)


class UserCreateView(generics.CreateAPIView):

    serializer_class = UserSerializer


    def perform_create(self, serializer):
        owner = self.request.user

        if owner.is_authenticated():
            raise PermissionDenied()
        serializer.save()


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    '''def filter_queryset(self, queryset):
        queryset = queryset.filter(username=self.request.user)

        return queryset'''


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(pk=self.kwargs.get('pk'))


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = TaskList.objects.all()
        #print (queryset)
        queryset = queryset.filter(Q(owner=self.request.user)|Q(friend=self.request.user))
        #queryset = queryset.filter(owner=self.request.user)
        return queryset


class TaskListDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = TaskList.objects.all()
        queryset = queryset.filter(Q(owner=self.request.user)|Q(friend=self.request.user))
        return queryset


class TaskCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        #print('We are HERE!!!!!!')
        queryset = Task.objects.all()
        list_id = self.kwargs.get('list_id', None)
        if list_id is not None:
            queryset = queryset.filter(tasklist_id=list_id)
        return queryset

    def perform_create(self, serializer):
        list_id = self.kwargs.get('list_id', None)
        try:
            tasklist = TaskList.objects.get(pk=list_id)
        except:
            raise exceptions.NotFound()
        serializer.save(tasklist=tasklist)

    def post(self, request, list_id, *args, **kwargs):
        print(type(request.data), request.data)
        tasklist = TaskList.objects.get(pk=list_id)
        tag_names = request.data.get('tags', []).split(',')
        data = request.data.copy()
        data.pop('tags')
        tags_set = []
        for tag_name in tag_names:
            tags_set.append(Tag.objects.get_or_create(name=tag_name)[0])
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(tasklist=tasklist)
        for tag in tags_set:
            serializer.instance.tags.add(tag)
        return Response(serializer.data)


class TaskDetailsView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Task.objects.all()
        list_id = self.kwargs.get('list_id', None)
        if list_id is not None:
            queryset = queryset.filter(tasklist_id=list_id)
        return queryset

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        tag_names = request.data.get('tags', []).split(',')
        print(tag_names)
        data = request.data.copy()
        print('DATAAAAAA', data)
        data.pop('tags')
        tags_set = []
        for tag_name in tag_names:
            tags_set.append(Tag.objects.get_or_create(name=tag_name)[0])
        serializer = self.serializer_class(instance=instance, data=data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        print ('CTTTTTN',tags_set)
        for tag in tags_set:
            print (tags_set, 'tags_set')
            serializer.instance.tags.add(tag)
        return Response(serializer.data)

