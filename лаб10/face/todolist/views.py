from django.shortcuts import render, redirect
from django.contrib import sessions
from .forms import LoginForm, RegistrationForm, ListForm, TaskForm
import requests
import json
from django.template import loader
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.template.context_processors import csrf
from .forms import *
from .models import *
from django.template import RequestContext
from django.core.mail import send_mail
import hashlib, datetime, random
from django.utils import timezone


def Login(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username'] #clean_data - очищенные данные для БД
        password = form.cleaned_data['password']
        token = requests.post('http://127.0.0.1:8000/get-token/', data={'username': username, 'password': password}) #используем функцию гет-пост для заполнения БД
        request.session['token'] = token.json()['token']
        request.session['username'] = username #сохраняем в сессию токен и юзернейм
        return redirect('http://127.0.0.1:8080/getlists/')
    return render(request, 'login.html', {'form': form}) #берем шаблон логин и в поле форму на сайте уже заполняет текущую форму


def GetList(request):
    form = ListForm(request.POST or None)
    if "token" in request.session:
        header = {'Authorization': 'Token ' + request.session['token']} #контактенция
        response = requests.get('http://127.0.0.1:8000/todolists/', headers=header) #обращаюсь к серверу для получения списка списков задач, сохраняю результат с сервера
        lists = response.json()
        if form.is_valid(): #если данные введены корректно, то вызываем метод пост, создаем новый список задач
            name = request.POST['name']
            friend = request.POST['friend'].split()
            response = requests.post('http://127.0.0.1:8000/todolists/', data={'name': name, 'friend': friend},
                                     headers=header).json() #все храним в БД 9 лабы
            return redirect('http://127.0.0.1:8080/getlists/')

    return render(request, 'getlists.html',
                  {"lists": lists, "header": 'Списки задач', "header1": 'Создайте новый список', \
                   'form': form})


def GetTasks(request, list_id):
    form = TaskForm(request.POST or None)
    if "token" in request.session:
        header = {'Authorization': 'Token ' + request.session['token']}
        url = 'http://127.0.0.1:8000/todolists/' + str(list_id) + '/tasks/' #вытаскиваем айдишник текущего списка задач
        response = requests.get(url, headers=header)
        tasks = response.json()

        url = 'http://127.0.0.1:8000/tag/'
        response = requests.get(url, headers=header)
        tags = response.json()

        if form.is_valid():
            name = request.POST['name']
            description = request.POST['description']
            tags = request.POST['tags']
            completed = request.POST.get('completed', False)

            if completed:
                completed = True
            due_date = request.POST['due_date']
            priority = request.POST["priority"]
            response = requests.post('http://127.0.0.1:8000/todolists/' + str(list_id) + '/tasks/',
                                     data={'name': name, 'description': description, 'completed': completed,
                                           'due_date': due_date, 'priority': priority, 'tags': tags},
                                     headers=header).json()

            return redirect('http://127.0.0.1:8080/getlists/' + str(list_id) + '/tasks/')
    return render(request, 'gettasks.html',
                  {'list_id': list_id, "tasks": tasks, 'form': form, "header": 'Задачи списка',
                   "header1": 'Создайте новую задачу'}) #мы передаем данную форму в html файл, в данном случае этот шаблон для владельца списков задач


def GetShareTasks(request, list_id):
    form = TaskForm(request.POST or None)
    if "token" in request.session:
        header = {'Authorization': 'Token ' + request.session['token']}
        url = 'http://127.0.0.1:8000/todolists/' + str(list_id) + '/tasks/'
        response = requests.get(url, headers=header)
        tasks = response.json()

        url = 'http://127.0.0.1:8000/tag/'
        response = requests.get(url, headers=header)
        tags = response.json()

    return render(request, 'sharegettasks.html',
                  {'list_id': list_id, "tasks": tasks, 'form': form, "header": 'Задачи списка'}) #а этот шаблон для невладельца


def ListDetails(request, list_id): #функция для параметров списка задач
    if request.method == 'POST':
        name = request.POST['name']
        friend = request.POST.get('friend', False)

        if "token" in request.session:
            header = {'Authorization': 'Token ' + request.session['token']}
            url = 'http://127.0.0.1:8000/todolists/' + str(list_id) + '/'
            response = requests.put(url, data={'name': name, 'friend': friend}, headers=header)

    if "token" in request.session:
        header = {'Authorization': 'Token ' + request.session['token']}
        user = request.session['username']
        url = 'http://127.0.0.1:8000/todolists/' + str(list_id) + '/'
        response = requests.get(url, headers=header)
        details = response.json()
        tasks = details.get('tasks')

    return render(request, 'listdetails.html',
                  {"details": details, 'user': user, "header": 'Детали списка', "tasks": tasks, "list_id": list_id})


def TaskDetails(request, list_id, task_id):
    if "token" in request.session:
        header = {'Authorization': 'Token ' + request.session['token']}
        url = 'http://127.0.0.1:8000/todolists/' + str(list_id) + '/tasks/' + str(task_id) + '/'
        response = requests.get(url, headers=header)
        details = response.json()
        tasks = details.get('tasks')
        name = details.get('name')
        description = details.get('description')
        completed = details.get('completed')
        tags = details.get('tags')
        priority = details.get('priority')
        date_created = details.get('date_created')
        date_modified = details.get('date_modified')

        tag = {'tags': ''}
        for t in tags:
            tag['tags'] += t
        tags = str(tags).replace('[', '').replace(']', '').replace("'", '')


    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        completed = request.POST.get('completed', False)
        date_created = request.POST.get('date_created', False)
        date_modified = request.POST.get('date_modified', False)
        priority = request.POST.get('priority', False)
        tags = request.POST.get('tags', False)
        completed = request.POST.get('completed', False)
        if completed:
            completed = True
        if 'token' in request.session:
            header = {'Authorization': 'Token ' + request.session['token']}
            response = requests.put('http://127.0.0.1:8000/todolists/' + str(list_id) + '/tasks/' + str(task_id) + '/',
                                    data={'name': name, 'description': description,
                                          'date_created': date_created,
                                          'completed': completed, 'date_modified': date_modified,
                                          'priority': priority, 'tags': tags}, headers=header).json()

    return render(request, 'taskdetails.html',
                  {"priority": priority, "header": 'Детали задачи', 'tags': tags, 'name': name,
                   'description': description,
                   'list_id': list_id, 'task_id': task_id, 'completed': completed, ' date_created': date_created,
                   'details': details})


def ShareTaskDetails(request, list_id, task_id):
    if "token" in request.session:
        header = {'Authorization': 'Token ' + request.session['token']}
        url = 'http://127.0.0.1:8000/todolists/' + str(list_id) + '/tasks/' + str(task_id) + '/'
        response = requests.get(url, headers=header)
        details = response.json()
        tasks = details.get('tasks')
        name = details.get('name')
        description = details.get('description')
        completed = details.get('completed')
        tags = details.get('tags')
        priority = details.get('priority')
        date_created = details.get('date_created')
        date_modified = details.get('date_modified')
        tag = {'tags': ''}
        for t in tags:
            tag['tags'] += t
        tags = str(tags).replace('[', '').replace(']', '').replace("'", '')


    return render(request, 'sharetaskdetails.html',
                  {"priority": priority, "header": 'Детали задачи', 'tags': tags, 'name': name,
                   'description': description,
                   'list_id': list_id, 'task_id': task_id, 'completed': completed, ' date_created': date_created,
                   'details': details})


def ListDelete(request, list_id):
    if 'token' in request.session:
        header = {'Authorization': 'Token ' + request.session['token']}
        response = requests.delete('http://127.0.0.1:8000/todolists/' + list_id + '/', headers=header)
    return redirect('http://127.0.0.1:8080/getlists/')


def TaskDelete(request, list_id, task_id):
    if 'token' in request.session:
        header = {'Authorization': 'Token ' + request.session['token']}
        response = requests.delete('http://127.0.0.1:8000/todolists/' + str(list_id) + '/tasks/' + str(task_id) + '/',
                                   headers=header)

    return redirect('http://127.0.0.1:8080/getlists/' + str(list_id) + '/tasks/')


def UserList(request):
    if "token" in request.session:
        header = {'Authorization': 'Token ' + request.session['token']}
        response = requests.get('http://127.0.0.1:8000/users/', headers=header)
        lists = response.json()
        print(lists)
    return render(request, 'userlist.html', {"lists": lists, "header": 'Пользователи'})




def UserDetails(request, user_id):
    # print (list_id)
    if "token" in request.session:
        header = {'Authorization': 'Token ' + request.session['token']}
        url = 'http://127.0.0.1:8000/users/' + str(user_id) + '/'
        response = requests.get(url, headers=header)
        details = response.json()
        print(details)

    return render(request, 'userdetails.html', {"details": details, "header": 'Информация о пользователе'})


def LogOut(request):
    request.session['token'] = None #удаляется из сессии токен
    return redirect('http://127.0.0.1:8080/login/')


def Registration(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        last_name = request.POST['last_name']
        first_name = request.POST['first_name']
        response = requests.post('http://127.0.0.1:8000/users/register/',
                                 data={'username': username, 'email': email, 'password': password,
                                       'last_name': last_name, 'first_name': first_name}).json()
        return redirect('http://127.0.0.1:8080/login/')
    return render(request, 'registration.html', {'form': form})


def Activate(request, activation_key):
    return render(request, 'activate.html')

