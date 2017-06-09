from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from .views import *

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'id')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class TaskSerializer(serializers.ModelSerializer):
    tags =TagSerializer

    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'completed', 'date_created', 'date_modified', 'due_date', 'priority',
                  'tags')
        read_only_fields = ('date_created', 'date_modified')

class TasklistSerializer(serializers.ModelSerializer):
    tasks = serializers.StringRelatedField(many=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Tasklist
        fields = ('name', 'tasks','id','owner')
        read_only_fields = ('tasks', 'owner')