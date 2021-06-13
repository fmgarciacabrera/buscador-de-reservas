from django import forms

from datetime import date, timedelta
from . import defaults

from .models import ContactInfo

class NewBookingForm(forms.Form):
    today = date.today()
    stoday = today.strftime(defaults.DATE_FORMAT)
    tomorrow = today + timedelta(days=3)
    stomorrow = tomorrow.strftime("%Y-%m-%d")
    fecha_entrada = forms.DateField(label="Fecha entrada", initial=stoday,
        widget=forms.DateInput(attrs={
            'class':'form-control datepicker',
            'placeholder': 'fecha entrada (yyyy-mm-dd)',
            'format': defaults.DATE_FORMAT
        }))
    fecha_entrada.label_classes = ('control-label')
    fecha_salida = forms.DateField(label="Fecha salida", initial=stomorrow,
        widget=forms.DateInput(attrs={
            'class':'form-control datepicker',
            'placeholder': 'fecha salida (yyyy-mm-dd)',
            'format': defaults.DATE_FORMAT
        }))
    guests = forms.IntegerField(label="Número de huéspedes", min_value=1,
        initial=1, max_value=4, widget=forms.NumberInput(attrs={
            'class':'form-control',
            'placeholder': 'Número de huéspedes'
        }))


class ContactInfoForm(forms.Form):

    name = forms.CharField(label="Nombre",
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder': 'Nombre'
        }))
    name.label_classes = ('control-label')
    email = forms.EmailField(label="Email",
        widget=forms.EmailInput(attrs={
            'class':'form-control',
            'placeholder': 'Escriba su email'
        }))
    email.label_classes = ('control-label')
    phone_number = forms.CharField(label="Teléfono",
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder': 'Número de teléfono'
        }))
    phone_number.label_classes = ('control-label')

    # campos ocultos
    arrival = forms.CharField(widget=forms.HiddenInput())
    departure = forms.CharField(widget=forms.HiddenInput())
    guests = forms.CharField(widget=forms.HiddenInput())
    roomtype = forms.CharField(widget=forms.HiddenInput())
    roomnumber = forms.CharField(widget=forms.HiddenInput())
    price = forms.CharField(widget=forms.HiddenInput())
