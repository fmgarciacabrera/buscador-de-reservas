import datetime
import random

from .models import Booking, RoomType, RoomTariff


def stay_nights(arrival, departure):
    """
    Calcula las noches de estancia de una reserva. La fecha de salida no cuenta,
    porque normalmente el check-out se produce durante el día. Dicho de otra
    forma la fecha de salida el huésped no hace noche en el establecimiento
    hotelero
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
    nights = stay_nights(arrival, departure)

    for x in range(0, nights):
        stay.append(arrival + datetime.timedelta(days = x))

    return stay


def available_rooms(arrival, departure, guests):
    """
    Obtiene las tipologías de habitaciones disponibles en las fechas de una
    estancia con un número de huéspedes dado

    Si no hay reservas solapadas con el rango de fechas de la reserva, están
    disponibles todas las habitaciones del establecimiento.

    Si hay alguna reserva solapada con el rango de fechas de la reserva, para
    cada tipología del establecimiento hotelero, el número de habitaciones
    disponibles es el número total de habitaciones de esa tipología menos las
    reservas solapadas de esa tipología.

    El número de habitación de la siguiente reserva de esa tipología, es el
    número de reservas de la tipología más uno.
    """
    # todas las tipologías de habitaciones que pueden acomodar a los huéspedes
    # de la reserva
    roomtypes = find_roomtypes(guests)
    # reservas registradas de las tipologías anteriores que se solapan con el
    # rango de fechas de la reserva
    bookings = find_bookings(arrival, departure, roomtypes)
    # noches de estancia
    nights = stay_nights(arrival, departure)
    # tarifas de las tipologías de habitaciones
    tariffs = find_tariffs()

    rooms = []
    if len(bookings) == 0:
        # al no haber reservas en ese rango, están disponibles todas las
        # habitaciones con capacidad suficiente para alojar a los huéspedes de
        # la reserva
        for roomtype in roomtypes:
            tariff = tariffs.filter(roomtype_id=roomtype.id).first()
            rooms.append({
                'room_type': roomtype,
                'available': roomtype.room_number,
                'room_number': 1,
                'price': nights * tariff.price_per_night})
    else:
        # si hay reservas, las habitaciones disponibles se obtienen a partir de
        # las tipologías reservadas que no alcanzan el número total de
        # habitaciones de cada tipología
        occupied_rooms = {}
        types_reserved = list(bookings.values())
        reserved = find_rooms_reserved(roomtypes, types_reserved)
        for roomtype in roomtypes:
            tariff = tariffs.filter(roomtype_id=roomtype.id).first()
            occupied = find_occupied(roomtype.id, reserved)
            # sólo se añade la habitación si hay disponibilidad
            available = roomtype.room_number - occupied
            if available:
                rooms.append({
                    'room_type': roomtype,
                    'available': available,
                    'room_number': occupied + 1,
                    'price': nights * tariff.price_per_night})

    return rooms


def find_bookings(arrival, departure, roomtypes):
    ids = {}
    bookings = {}
    range = expand_range(arrival, departure)
    for date in range:
        set = Booking.objects.filter(arrival__lte=date,
            departure__gt=date,
            roomtype__in=roomtypes).values_list('id', 'roomtype')
        values = list(set)
        if len(values):
            for value in values:
                # bookings[value.id] = value.roomtype
                bookings[value[0]] = value[1]

    # bookings contiene un diccionario, con clave el id de reserva y valor tipo
    # de habitación en el intervalo de búsqueda para los huéspedes indicados

    return bookings


def find_roomtypes(guests):
    return RoomType.objects.filter(room_capacity__gte=guests)


def find_tariffs():
    return RoomTariff.objects.all()


def find_rooms_reserved(roomtypes, types_reserved):
    rooms_reserved = []
    for roomtype in roomtypes:
        count = types_reserved.count(roomtype.id)
        room = {'roomtype': roomtype.id, 'occupied': count}
        rooms_reserved.append(room)

    return rooms_reserved


def find_occupied(roomtype, reserved_roomtypes):
    for reserved in reserved_roomtypes:
        if reserved['roomtype'] == roomtype:
            return reserved['occupied']

    return 0


def serialize_booking_data(data):
    """
    Serializes a dictionary containing booking data: arrival and departure
    dates, number of guests, room type, next available room number, booking
    price
    """
    keys = ["arrival", "departure", "guests", "roomtype_id", "room_number", "price"]
    vector = []
    for key in keys:
        vector.append(":".join([key, str(data[key])]))

    return ";".join(vector)


def generate_booking_reference():
    numbers = []
    for x in range(0,5):
        numbers.append(random.randint(1, 99))

    return "".join(map(lambda number : str(number).zfill(2), numbers))


def generate_unique_booking_reference():

    already_exists = True
    while already_exists:
        booking_number = generate_booking_reference()
        already_exists = Booking.objects.filter(gds_number=booking_number).exists()

    return booking_number
