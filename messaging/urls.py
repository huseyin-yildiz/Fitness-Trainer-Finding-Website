from django.urls import path, re_path
from .views import *

app_name = 'messaging'

urlpatterns = [
    path('index/', message_view, name='index'),
    path('form/', create_message, name='form'),
    #re_path(r'^(?P<id>\d+)/$', trainer_detail, name='detail'),
    #path('create/', trainer_create, name='create'),
    #re_path(r'^(?P<id>[\w-]+)/update/$', trainer_update, name='update'),
    #re_path(r'^(?P<id>[\w-]+)/delete/', trainer_delete, name='delete'),
]

