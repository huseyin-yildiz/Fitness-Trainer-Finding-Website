from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext

from payment.models import Sale
from payment.forms import SalePaymentForm

from django.core.mail import send_mail
from django.conf import settings


def charge(request,trainer_id):
    if request.method == "POST":
        form = SalePaymentForm(request.POST)
        
        if form.is_valid(): # charges the card
            return HttpResponse("Success! The payment is completed successfully")
        print("valid:",form.is_valid())
    else:
        form = SalePaymentForm()

    context= {
        'form':form,
        'user':request.user.id,
        'trainer_id':trainer_id
    }

    return render(request, "payment/charge.html", 
                        context)
