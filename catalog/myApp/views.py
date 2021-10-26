from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings

def index(request):

    send_mail('TestSubject','This is a test message',settings.DEFAULT_FROM_EMAIL,["huseyin3421___@hotmail.com"])
    return HttpResponse("Selamun Aleykum Dünya, İlk  django view'ım.")
# Create your views here.
