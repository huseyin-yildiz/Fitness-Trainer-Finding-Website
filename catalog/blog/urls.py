from django.urls import path, include
from . import views

urlpatterns = [
    #path("",views.home,name = "home")
    path("",views.HomeView.as_view(),name="home")
]
