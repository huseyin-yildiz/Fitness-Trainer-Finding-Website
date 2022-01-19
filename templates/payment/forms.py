from datetime import date, datetime
from calendar import monthrange

from django import forms
from django.contrib.auth.models import User
from payment.models import Sale
from trainer.models import CalendarEvent, Reservation

class CreditCardField(forms.IntegerField):
    def clean(self, value):
        """Check if given CC number is valid and one of the
           card types we accept"""
        if value and (len(value) < 13 or len(value) > 16):
            raise forms.ValidationError("Please enter in a valid "+\
                "credit card number.")
        return super(CreditCardField, self).clean(value)


class CCExpWidget(forms.MultiWidget):
    """ Widget containing two select boxes for selecting the month and year"""
    def decompress(self, value):
        return [value.month, value.year] if value else [None, None]

    def format_output(self, rendered_widgets):
        html = u' / '.join(rendered_widgets)
        return u'<span style="white-space: nowrap">%s</span>' % html


class CCExpField(forms.MultiValueField):
    EXP_MONTH = [(x, x) for x in range(1, 13)]
    EXP_YEAR = [(x, x) for x in range(date.today().year,
                                       date.today().year + 15)]
    default_error_messages = {
        'invalid_month': u'Enter a valid month.',
        'invalid_year': u'Enter a valid year.',
    }

    def __init__(self, *args, **kwargs):
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])
        fields = (
            forms.ChoiceField(choices=self.EXP_MONTH,
                error_messages={'invalid': errors['invalid_month']}),
            forms.ChoiceField(choices=self.EXP_YEAR,
                error_messages={'invalid': errors['invalid_year']}),
        )
        super(CCExpField, self).__init__(fields, *args, **kwargs)
        self.widget = CCExpWidget(widgets =
            [fields[0].widget, fields[1].widget])

    def clean(self, value):
        exp = super(CCExpField, self).clean(value)
        if date.today() > exp:
            raise forms.ValidationError(
            "The expiration date you entered is in the past.")
        return exp

    def compress(self, data_list):
        year = int(data_list[1])
        month = int(data_list[0])
        # find last day of the month
        day = monthrange(year, month)[1]
        return date(year, month, day)
'''        if data_list:
            if data_list[1] in forms.fields.INVALID EMPTY_VALUES:
                error = self.error_messages['invalid_year']
                raise forms.ValidationError(error)
            if data_list[0] in forms.fields.EMPTY_VALUES:
                error = self.error_messages['invalid_month']
                raise forms.ValidationError(error)'''
            
        
   #     return None


class SalePaymentForm(forms.Form):
    
    number = CreditCardField(required=True, label="Card Number")
    expiration = CCExpField(required=True, label="Expiration")
    cvc = forms.IntegerField(required=True, label="CCV Number",
        max_value=9999, widget=forms.TextInput(attrs={'size': '4'}))

    thedate = forms.DateField(required=True, label="Date",initial=date.today)
    hour = forms.IntegerField(required=True, label="Hour")
    trainer_id = forms.IntegerField(required=True, label="trainer_id")
    customer_id = forms.IntegerField(required=True, label="customer_id")
    is_online = forms.BooleanField(required=True, label="is_online")
    address = forms.CharField(required=False)

    

    def clean(self):
        """
        The clean method will effectively charge the card and create a new
        Sale instance. If it fails, it simply raises the error given from
        Stripe's library as a standard ValidationError for proper feedback.
        """
        
        cleaned = super(SalePaymentForm, self).clean()
        
        
        if not self.errors:
            number = self.cleaned_data["number"]
            exp_month = self.cleaned_data["expiration"].month
            exp_year = self.cleaned_data["expiration"].year
            cvc = self.cleaned_data["cvc"]
            thedate = self.cleaned_data["thedate"]
            hour = self.cleaned_data["hour"]
            trainer_id = self.cleaned_data["trainer_id"]
            is_online = self.cleaned_data["is_online"]
            address = self.cleaned_data["address"]
            customer_id = self.cleaned_data["customer_id"]
            

            sale = Sale()
            
            # let's charge $10.00 for this particular item
            success, instance = sale.charge(1000, number, exp_month, 
                                                exp_year, cvc)
            
            if not success:
                raise forms.ValidationError("Error: %s" % instance.message)
            else:
                instance.save()
                reservate(trainer_id,customer_id,thedate,hour)
                # we were successful! do whatever you will here... 
                # perhaps you'd like to send an email...
                pass
        
        return cleaned
    
    


def reservate(trainerId,customer_id,daydate,hour):


    dayofweek = daydate.weekday()
    
    customer = User.objects.filter(id=customer_id).first()
    print(daydate.day)
    event = CalendarEvent.objects.filter(day_of_week=dayofweek,trainer=trainerId,start_time=hour ).first()
    trainer = event.trainer
    

    Reservation.objects. create(event=event,trainer=trainer,customer=customer,date_time=daydate)


    
