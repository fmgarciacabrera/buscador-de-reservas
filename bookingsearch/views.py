from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

# Create your views here.

from .models import Booking
from .forms import NewBookingForm
from . import defaults
from . import availability

def index(request):
    booking_list = Booking.objects.all()
    template = loader.get_template('bookingsearch/index.html')
    context = {
        'booking_list': booking_list
    }
    return HttpResponse(template.render(context, request))


def newbooking(request):
    # POST: se procesa el formulario recibido
    if request.method == 'POST':
        form = NewBookingForm(request.POST)

        # si es válido, se efectúa la búsqueda
        if form.is_valid():
            search_criteria = True
            arrival = form.cleaned_data.get("fecha_entrada")
            departure = form.cleaned_data.get("fecha_salida")
            guests = form.cleaned_data.get("guests")
            search = {
                'arrival': arrival,
                'sarrival': arrival.strftime(defaults.DATE_FORMAT),
                'departure': departure,
                'sdeparture': departure.strftime(defaults.DATE_FORMAT),
                'guests': guests,
                'nights': availability.stay_nights(arrival, departure)
            }
            rooms = availability.available_rooms(arrival, departure)

    # creamos el formulario vacío
    else:
        form = NewBookingForm()
        search_criteria = False
        search = {}
        rooms = {}

    template = loader.get_template('bookingsearch/newbooking.html')
    context = {
        'form': form,
        'search_criteria': search_criteria,
        'search': search,
        'rooms': rooms
    }

    return HttpResponse(template.render(context, request))


def newsearch(request):
    return HttpResponseRedirect("/newbooking")


def contact(request):
    return HttpResponse("Contact view. Gathers contact information.")


def about(request):
    return HttpResponse("About view. Info.")
