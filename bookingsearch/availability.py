import datetime

from .models import Booking, RoomType, RoomTariff


def stay_nights(arrival, departure):
    """
    Calcula las noches de estancia de una reserva. La fecha de salida no cuenta,
    porque normalmente el check-out se produce durante el día
    """
    return (departure - arrival).days


def expand_range(arrival, departure):
    """
    Expande el rango de fechas [arrival, departure). Por ejemplo:

      expand_range('2021-06-01', '2020-06-03')

    produce

      ['2021-06-01', '2021-06-02']

    """
    stay = []
    nights = (departure - arrival).days
    for x in range(0, nights):
        stay.append(arrival + datetime.timedelta(days = x))
    return stay


def available_rooms(arrival, departure):
    bookings = find_bookings(arrival, departure)
    nights = stay_nights(arrival, departure)
    roomtypes = find_roomtypes()
    tariffs = find_tariffs()

    rooms = {}
    if len(bookings) == 0:
        rooms = [
            {'room_type': 1, 'available': 10, 'price': nights * 20.0},
            {'room_type': 2, 'available': 5, 'price': nights * 30.0},
            {'room_type': 3, 'available': 4, 'price': nights * 40.0},
            {'room_type': 4, 'available': 6, 'price': nights * 50.0},
        ]
    else:
        occupied_rooms = {}
        for booking in bookings:
            occupied_rooms[booking.id] = booking.roomtype

    return rooms


def find_bookings(arrival, departure):
    bookings = []
    range = expand_range(arrival, departure)
    for date in range:
        set = Booking.objects.filter(arrival__lte=date, departure__gt=date)
        values = set.values()
        if len(values):
            bookings.append(values)

    return bookings


def find_roomtypes():
    return RoomType.objects.all()


def find_tariffs():
    return RoomTariff.objects.all()
