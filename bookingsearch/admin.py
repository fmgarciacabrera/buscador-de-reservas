from django.contrib import admin

# Register your models here.

from .models import RoomType, RoomTariff, Booking, ContactInfo

admin.site.register(Booking)
admin.site.register(ContactInfo)
admin.site.register(RoomType)
admin.site.register(RoomTariff)
