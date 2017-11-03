from rest_framework import serializers
from .models import Task, TaskList, Tag, UserProfile
from django.contrib.auth.models import User
from django.core.mail import send_mail
import hashlib, datetime, random
from django.utils import timezone
from django.shortcuts import render_to_response, get_object_or_404


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password','first_name','last_name','email','is_active')
        write_only_fields = ('password','username','first_name','last_name','email','is_active')
        read_only_fields = ('is_staff', 'is_superuser', 'date_joined',)

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'], email=validated_data['email'],
                                   first_name=validated_data['first_name'], last_name=validated_data['last_name'],
                                   is_active=0)
        user.set_password(validated_data['password'])
        user.save()

        salt = hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()
        # print('SAAAAAAAAAAALT', salt)
        salt_bytes = salt.encode('utf-8')
        email_bytes = user.email.encode('utf-8')
        activation_key = hashlib.sha1(salt_bytes + email_bytes).hexdigest()
        key_expires = datetime.datetime.today() + datetime.timedelta(2)
        # return user
        new_profile = UserProfile(user=user, activation_key=activation_key,
                                  key_expires=key_expires)
        new_profile.save()
        # Send email with activation key
        email_subject = 'Подтверждение регистрации'
        email_body = "Здравствуйте, %s, спасибо за регистрацию на нашем сайте. Для активации аккаунта пройдите по ссылке в течении 48 часов \
         http://127.0.0.1:8080/activate/%s/" % (user.username, activation_key)
        # print(email_body)
        send_mail(email_subject, email_body, 'novikowalera@gmail.com',
                  [user.email], fail_silently=False)

        def save(self, commit=True):
            # user = super(RegistrationForm, self).save(commit=False)
            user.email = self.cleaned_data['email']
            if commit:
                user.is_active = 0  # not active until he opens activation link
            user.save()

        user.is_active = 1
        user.save()
        return user


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name','tasks')



class TaskListSerializer(serializers.ModelSerializer):
    tasks = serializers.StringRelatedField(many=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = TaskList
        fields = ('id', 'name', 'tasks', 'owner','friend')
        read_only_fields = ('tasks', 'owner')


class TaskSerializer(serializers.ModelSerializer):
    #tags = TagSerializer
    tags = serializers.SlugRelatedField(many=True,queryset=Tag.objects.all(), slug_field='name')
    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'completed', 'tags', 'date_created', 'date_modified',
                  'due_date', 'priority')
        read_only_fields = ('date_created', 'date_modified',)