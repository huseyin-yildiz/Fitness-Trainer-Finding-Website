from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Selamun Aleykum Dünya, İlk  django view'ım.")
# Create your views here.
