from django import forms

from datetime import date, timedelta
from . import defaults

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
