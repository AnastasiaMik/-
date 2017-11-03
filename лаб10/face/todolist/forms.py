from django import forms
import datetime
from django.contrib.auth.models import User
import requests


class LoginForm(forms.Form):
    username = forms.CharField(max_length=200,label='Логин')
    password = forms.CharField(max_length=200,label='Пароль', widget=forms.PasswordInput())

class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=200,label='Имя')
    last_name = forms.CharField(max_length=200,label='Фамилия')
    username = forms.CharField(max_length=200,label='Логин')
    password = forms.CharField(max_length=200,label='Пароль')
    email = forms.CharField(max_length=200,label='Email')

class ListForm(forms.Form):
    name = forms.CharField(max_length=200,label='Название списка')
    
class TaskForm(forms.Form):
    name = forms.CharField(max_length=200,label='Название задачи')
    description = forms.CharField(max_length=200,label='Описание задачи')
    completed = forms.BooleanField(required=False, label='Завершена')
