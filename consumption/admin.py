from django.contrib import admin

from .models import Hotel, Meter, HalfHourly


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Meter)
class MeterAdmin(admin.ModelAdmin):
    list_display = ('id', 'fuel', 'unit')


@admin.register(HalfHourly)
class HalfHourlyAdmin(admin.ModelAdmin):
    pass
