from django.urls import path, re_path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', signup, name='register'),
    path('logout/', logout_view, name='logout'),
]
