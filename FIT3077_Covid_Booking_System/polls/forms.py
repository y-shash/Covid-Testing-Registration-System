from django import forms
from django.forms import CheckboxInput

from .models import Measurement, Booking


class MeasurementModelForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ('destination',)


class BookingModelForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('startTime',)
        widgets = {
            'Home Testing': CheckboxInput(attrs={'class': 'required checkbox form-control'}),
        }

# class UserModelForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('givenName', 'familyName', 'userName', 'password', 'phoneNumber', 'isCustomer', 'isReceptionist',
#                   'isHealthcareWorker', 'additionalInfo',)
