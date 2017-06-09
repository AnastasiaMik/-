from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = {
    url(r'^tag/$', CreateTag.as_view(), name='AllTag'),
    url(r'tag/(?P<pk>[0-9]+)/delete/$', DeleteTag.as_view(), name='DeleteTag'),
    url(r'tag/(?P<pk>[0-9]+)/update/$', UpdateTag.as_view(), name='UpdateTeg'),

    url(r'^users/$', ListUser.as_view(), name='ListUser'),
    url(r'^users/register/$', CreateUser.as_view(), name='CreateUser'),
    url(r'^users/(?P<pk>[0-9]+)/delete/$', DeleteUser.as_view(), name='DeleteUser'),
    url(r'^users/(?P<pk>[0-9]+)/update/$', UpdateUser.as_view(), name='UpdateUser'),

    url(r'^todolists/$', TasklistCreateView.as_view(), name="lists"),
    url(r'^todolists/(?P<pk>[0-9]+)/$', TasklistDetailsView.as_view(), name="list-detail"),
    url(r'^todolists/(?P<list_id>[0-9]+)/tasks', TaskCreateView.as_view(), name="tasks"),
    url(r'^todolists/(?P<list_id>[0-9]+)/tasks/(?P<pk>[0-9]+)', TaskDetailsView.as_view(), name="task-detail"),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
}

urlpatterns = format_suffix_patterns(urlpatterns)