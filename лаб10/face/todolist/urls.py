from django.conf.urls import url, include
from .views import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^login/$', Login),
    url(r'^getlists/$', GetList),
    url(r'^getlists/(?P<list_id>[0-9]+)/$', ListDetails),
    url(r'^getlists/(?P<list_id>[0-9]+)/tasks/$', GetTasks),
    url(r'^getlists/(?P<list_id>[0-9]+)/sharetasks/$', GetShareTasks),
    url(r'^getlists/(?P<list_id>[0-9]+)/tasks/(?P<task_id>[0-9]+)/$', TaskDetails),
    url(r'^getlists/(?P<list_id>[0-9]+)/sharetasks/(?P<task_id>[0-9]+)/share/$', ShareTaskDetails),
    url(r'^users/$', UserList),
    url(r'^users/(?P<user_id>[0-9]+)/$', UserDetails),
    url(r'^logout/$', LogOut),
    url(r'^registration/$', Registration),
    url(r'^getlists/(?P<list_id>[0-9]+)/delete/$', ListDelete),
    url(r'^getlists/(?P<list_id>[0-9]+)/tasks/(?P<task_id>[0-9]+)/delete/$', TaskDelete),
    url(r'^activate/(?P<activation_key>[\w-]+)/', Activate),
]
