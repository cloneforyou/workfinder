import datetime
import factory
from factory.fuzzy import FuzzyChoice, FuzzyInteger, FuzzyDateTime, FuzzyFloat


from consumption.models import Hotel, Meter, HalfHourly


class HotelFactory(factory.DjangoModelFactory):
    class Meta:
        model = Hotel

    id = FuzzyInteger(1, 100)
    name = factory.Faker('company')


class MeterFactory(factory.DjangoModelFactory):
    class Meta:
        model = Meter

    id = FuzzyInteger(1, 100)
    fuel = FuzzyChoice(Meter.FUEL_CHOICES, getter=lambda x: x[0])
    unit = FuzzyChoice(Meter.UNIT_CHOICES, getter=lambda x: x[0])
    hotel = factory.SubFactory(HotelFactory)


class HalfHourlyFactory(factory.DjangoModelFactory):
    class Meta:
        model = HalfHourly

    consumption = FuzzyFloat(0,0, 100.99)
    reading_date_time = FuzzyDateTime(datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc))
    meter = factory.SubFactory(MeterFactory)
