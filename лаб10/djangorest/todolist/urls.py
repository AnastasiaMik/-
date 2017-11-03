from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
from .views import *
#TagCreateView,UserCreateView,UserList,UserDetail,TaskListCreateView,TaskListDetailsView,TaskCreateView,TaskDetailsView, TagViewSet, TagDetailsView



urlpatterns = {
    url(r'^users/$', UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', UserDetail.as_view()),
    url(r'^users/register', UserCreateView.as_view(), name="create-user"),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^todolists/$', TaskListCreateView.as_view(), name="lists"),
    url(r'^todolists/(?P<pk>[0-9]+)/$', TaskListDetailsView.as_view(), name="list-detail"),
    url(r'^todolists/(?P<list_id>[0-9]+)/tasks/$', TaskCreateView.as_view(), name="tasks"),
    url(r'^todolists/(?P<list_id>[0-9]+)/tasks/(?P<pk>[0-9]+)/$', TaskDetailsView.as_view(), name="task-detail"),
    url(r'^tag/$', TagCreateView.as_view(), name="tag"),
    url(r'^tag/(?P<pk>[0-9]+)/$', TagDetailsView.as_view(), name="tags"),
    url(r'^get-token/', obtain_auth_token),
    # url(r'^todolists/shared/$', SharedTasklistView.as_view()),
    # url(r'^todolists/shared/(?P<list_id>[0-9]+)/tasks/$', SharedTaskView.as_view()),
    # url(r'^todolists/shared/(?P<list_id>[0-9]+)/tasks/(?P<pk>[0-9]+)/$', SharedTaskView.as_view()),
   }

urlpatterns = format_suffix_patterns(urlpatterns)
