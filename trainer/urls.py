from django.urls import path, re_path
from .views import *

app_name = 'trainer'

urlpatterns = [
    path('index/', trainer_index, name='index'),
    re_path(r'^(?P<id>\d+)/$', trainer_detail, name='detail'),
    path('create/', trainer_create, name='create'),
    re_path(r'^(?P<slug>[\w-]+)/update/$', trainer_update, name='update'),
    re_path(r'^(?P<slug>[\w-]+)/delete/', trainer_delete, name='delete'),
]

