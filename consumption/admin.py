from django.contrib import admin

from .models import Hotel, Meter, HalfHourly


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    pass


@admin.register(Meter)
class MeterAdmin(admin.ModelAdmin):
    pass


@admin.register(HalfHourly)
class HalfHourlyAdmin(admin.ModelAdmin):
    pass
