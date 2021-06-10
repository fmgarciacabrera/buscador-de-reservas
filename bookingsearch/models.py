from django.db import models

# Create your models here.

class RoomType(models.Model):
    room_name = models.CharField(max_length=40)
    room_code = models.CharField(max_length=3)
    room_number = models.IntegerField(default=0)
    room_capacity = models.IntegerField(default=1)

    def __str__(self):
        return self.room_code

    def to_string(self):
        return "{} ({})".format(self.room_name, self.room_code)


class RoomTariff(models.Model):
    roomtype = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    price_per_night = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return "{} {} {}".format(self.id, self.roomtype, self.price_per_night)


class ContactInfo(models.Model):
    name = models.CharField(max_length=80)
    email = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)


class Booking(models.Model):
    arrival = models.DateField(default=0)
    departure = models.DateField(default=0)
    roomtype = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    guest_number = models.IntegerField(default=1)
    contact_info = models.ForeignKey(ContactInfo, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    gds_number = models.CharField(max_length=32)
    room_number = models.IntegerField(default=1, blank=True)
