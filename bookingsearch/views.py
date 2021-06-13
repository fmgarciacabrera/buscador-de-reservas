from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext

# Create your views here.

from .models import Booking, RoomType, ContactInfo
from .forms import NewBookingForm, ContactInfoForm
from . import defaults
from . import availability

def index(request):
    booking_list = Booking.objects.all()

    template = loader.get_template('bookingsearch/index.html')
    context = {
        'booking_list': booking_list,
        'defaults': defaults,
        'subtitle': "Listado de reservas"
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
            rooms = availability.available_rooms(arrival, departure, guests)

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
        'rooms': rooms,
        'defaults': defaults,
        'subtitle': 'Nueva reserva'
    }

    return HttpResponse(template.render(context, request))


def newsearch(request):
    return HttpResponseRedirect("/newbooking")


def contact(request):

    if request.method == "GET":
        return HttpResponseRedirect("/newbooking/")

    if request.method == "POST":

        # return HttpResponse(":".join(request.POST.values()))
        form = ContactInfoForm(request.POST)

        roomtype = request.POST["roomtype"]
        bookingdata = {
            'arrival': request.POST["arrival"],
            'departure': request.POST["departure"],
            'guests': request.POST["guests"],
            'roomtype': roomtype,
            'roomnumber': request.POST["roomnumber"],
            'price': request.POST["price"]
        }
        room = RoomType.objects.get(pk=roomtype)

        contactdata = {}

        if form.is_valid():
            data = form.cleaned_data
            contact = ContactInfo(name=data["name"], email=data["email"],
                phone_number=data["phone_number"])
            contact.save()

            roomtype = RoomType.objects.get(pk=data["roomtype"])
            booking = Booking(arrival= data["arrival"],
                departure= data["departure"],
                roomtype = roomtype,
                guest_number = data["guests"],
                contact_info = contact,
                price = data["price"],
                gds_number = availability.generate_unique_booking_reference(),
                room_number = data["roomnumber"]
            )
            booking.save()

            return HttpResponseRedirect("/")

    template = loader.get_template('bookingsearch/contact.html')
    context = {
        'defaults': defaults,
        'subtitle': 'Datos de contacto',
        'bookingdata': bookingdata,
        'room': room,
        'form': form,
        'contactdata': contactdata
    }

    # return HttpResponse("Contact view. Gathers contact information.")
    return HttpResponse(template.render(context, request))


def about(request):
    template = loader.get_template('bookingsearch/about.html')
    context = {
        'defaults': defaults,
        'subtitle': 'Acerca de...'
    }

    return HttpResponse(template.render(context, request))
