from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, Http404, reverse
from trainer.models import Trainer
from .models import Message
# from .forms import TrainerForm, CommentForm
from django.contrib.auth.models import User
from .forms import MessageForm


def message_view(request):

    if not request.user.is_authenticated:
        return Http404()

    form = MessageForm(request.POST or None)
    if form.is_valid():
        message = form.save(commit=False)
        message.sender = request.user
        message.save()
        return HttpResponseRedirect(reverse('messaging:index'))

    messages = Message.objects.all()
    received_messages = None
    sent_messages = None
    if request.user.is_authenticated:
        received_messages = messages.filter(receiver=request.user)
        sent_messages = messages.filter(sender=request.user)

    context = {
        'received_messages': received_messages,
        'sent_messages': sent_messages,
        'form': form,
    }

    return render(request, 'messaging/messages.html', context)


# Create your views here.
def message_view2(request):
    # Kullaniciya ait olan mesajlarin listelenmesi

    messages = Message.objects.all()
    received_messages = None
    sent_messages = None
    if request.user.is_authenticated:
        received_messages = messages.filter(receiver=request.user)
        sent_messages = messages.filter(sender=request.user)

    return render(request, 'messaging/messages2.html', {'received_messages': received_messages, 'sent_messages': sent_messages})

def create_message(request):
    if not request.user.is_authenticated:
        return Http404()

    form = MessageForm(request.POST or None)
    if form.is_valid():
        message = form.save(commit=False)
        message.sender = request.user
        message.save()
        return HttpResponseRedirect(reverse('messaging:index'))

    context = {
        'form': form,
    }

    return render(request, 'messaging/form.html', context)
