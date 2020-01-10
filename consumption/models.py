from django.db import models


class Hotel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return '{}'.format(self.name)


class Meter(models.Model):
    WATER = 'water'
    NATURAL_GAS = 'natural gas'
    ELECTRICITY = 'electricity'

    FUEL_CHOICES = [
       (WATER, 'Water'),
       (NATURAL_GAS, 'Natural Gas'),
       (ELECTRICITY, 'Electricity'), 
    ]

    M3 = 'm3'
    KWH = 'kWh'

    UNIT_CHOICES = [
        (M3, 'm3'),
        (KWH, 'kWh'),
    ]

    id = models.AutoField(primary_key=True)
    fuel = models.CharField(max_length=16, choices=FUEL_CHOICES)
    unit = models.CharField(max_length=3, choices=UNIT_CHOICES)
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE, related_name='meter')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return '{}-{}'.format(self.id, self.fuel)


class HalfHourly(models.Model):
    consumption = models.FloatField(default=0)
    reading_date_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    meter = models.ForeignKey('Meter', on_delete=models.CASCADE, related_name='halfhourly')

    class Meta:
        ordering = ['reading_date_time']

    def __str__(self):
        return '{}'.format(self.meter.fuel)
