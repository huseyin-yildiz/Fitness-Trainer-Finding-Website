from django.db.models.fields import DateField
from django.db.models.query import QuerySet
from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, Http404
from .models import CalendarEvent, Reservation, Trainer
from .forms import TrainerForm, CommentForm
from django.contrib import messages
from dict2xml import dict2xml
import datetime
from django.contrib.auth.decorators import login_required
from Product.models import Product
from django.core.mail import send_mail
from django.conf import settings
import jwt
import datetime
import requests
import json


def trainer_index(request):
    print("here")
    trainers = Trainer.objects.all()
    auth_trainer = None
    if request.user.is_authenticated:
        auth_trainer = trainers.filter(User_ID=request.user)

    return render(request, 'trainer/index.html', {'trainers': trainers, 'auth_trainer': auth_trainer})


def trainer_detail(request, id):
    trainer = get_object_or_404(Trainer, id=id)
    product = None
    product = Product.objects.all().first()

    disc_price = product.price * ((100 - product.discount_rate) / 100)

    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.trainer = trainer
        comment.save()
        return HttpResponseRedirect(trainer.get_absolute_url())

    context = {
        'trainer': trainer,
        'form': form,
        'product': product,
        'disc_price': disc_price,
    }

    return render(request, 'trainer/detail.html', context)


def trainer_create(request):
    form = TrainerForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
    else:
        form = TrainerForm()
    context = {
        'form': form,
    }
    return render(request, 'trainer/form.html', context)


def trainer_update(request, id):
    if not request.user.is_authenticated:
        return Http404()

    trainer = get_object_or_404(Trainer, id=id)
    print(trainer.User_ID)
    form = TrainerForm(request.POST or None, request.FILES or None, instance=trainer)
    if form.is_valid():
        if request.user == trainer.User_ID:
            form.save()
            messages.success(request, 'Successfully updated!')
            return HttpResponseRedirect(trainer.get_absolute_url())
        else:
            messages.warning(request, 'You can not edit another trainer\'s information.')
            return redirect('trainer:index')
    context = {
        'form': form,
    }
    return render(request, 'trainer/form.html', context)


def trainer_delete(request):
    return HttpResponse('Burası trainer delete sayfası')


def add_calendar_event(request):
    return HttpResponse('Burası trainer delete sayfası')


def is_free_at(trainerId, date, hour):
    dateS = date.split('-')
    dayofweek = datetime.date(int(dateS[0]), int(dateS[1]), int(dateS[2])).weekday()

    isThereTheEvent = CalendarEvent.objects.filter(day_of_week=dayofweek, trainer=trainerId, start_time=hour)

    if (isThereTheEvent):
        rezervations = Reservation.objects.filter(date_time=date, trainer=trainerId)  # id ile query hata hata
        if (rezervations.exists()):
            for res in rezervations:
                print("resssssssssssssS::", res.event.start_time)
                if (res.event.start_time == hour):
                    return False
            return True
        else:
            return True
    else:
        return False


def create_meeting(meeting_topic, year, month, day, hour, minute):
    time_now = datetime.datetime.now()
    expiration_time = time_now + datetime.timedelta(seconds=300)
    rounded_off_exp_time = round(expiration_time.timestamp())

    api_key = "2RfY60-aRFuYxApKuGpikw"
    api_secret = "7XdNSHl7FWlPRdXPRNPSZrz2Op31dPloWRi5"

    ## Generate token
    headers = {"alg": "HS256", "typ": "JWT"}
    payload = {"iss": api_key, "exp": rounded_off_exp_time}
    encoded_jwt = jwt.encode(payload, api_secret, algorithm="HS256")
    email = "turkoaygun@gmail.com"
    url = "https://api.zoom.us/v2/users/{}/meetings".format(email)
    date = datetime.datetime(year, month, day, hour, minute).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(date)
    obj = {"topic": meeting_topic,
           "start_time": date,
           "duration": 30,
           "password": "12345",
           "timezone": "Europe/Istanbul"
           }
    header = {"authorization": "Bearer {}".format(encoded_jwt)}
    r = requests.post(url, json=obj, headers=header)

    ## Print and return join URL & password
    inf = json.loads(r.text)
    join_URL = inf["join_url"]
    meetingPassword = inf["password"]

    print(
        f'\n here is your zoom meeting link {join_URL} and your \
            password: "{meetingPassword}"\n')

    return join_URL


def free__lectures(trainerId, date):
    free_lecs = list()

    for a in range(0, 23):
        isFree = is_free_at(trainerId, date, a)
        print("is free ", a, ":", isFree)
        if (isFree):
            free_lecs.append(a)
    return free_lecs

    dateS = date.split('-')
    print("date::::::", dateS)
    dayofweek = datetime.date(int(dateS[0]), int(dateS[1]), int(dateS[2])).weekday()
    print("dayofweek:", dayofweek)
    events = CalendarEvent.objects.filter(day_of_week=dayofweek, trainer=trainerId)
    print("events::", events)

    free__lecs = list()
    for event in events:
        print("eve::", event)
        if (is_free_at(trainerId, date, event.start_time)):
            free__lecs.append(event)
            print("eventt:::", event)

    return free__lecs


# Reservation part


def reservationInfo(request, id, date):
    free_lecs = free__lectures(id, date)

    a = [1, 2]
    data = {"free_lecs": free_lecs
            }

    xml = dict2xml(data)
    print(xml)

    return HttpResponse(str(xml))


@login_required
def reservation(request, id):
    return render(request, 'trainer/calendar.html')
