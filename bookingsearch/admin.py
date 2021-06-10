from django.contrib import admin

# Register your models here.

from .models import RoomType, RoomTariff

admin.site.register(RoomType)
admin.site.register(RoomTariff)
