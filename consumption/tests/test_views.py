import io
import csv
import os

import pytest
from django.urls import reverse

from consumption.tests.factories import HotelFactory, MeterFactory, HalfHourlyFactory
from consumption.views import CsvUpload
from consumption.models import Hotel, Meter, HalfHourly


@pytest.fixture
def mock_hotel(db):
    return HotelFactory()


@pytest.fixture
def mock_meter(db):
    return MeterFactory()


@pytest.fixture
def mock_half_hourly(db):
    return HalfHourlyFactory()


def test_fixtures(mock_hotel):
    # This is to ensure the fixtures are actually correct and not behaving
    hotel = mock_hotel
    meter = MeterFactory(hotel=hotel)
    half_hourly = HalfHourlyFactory(meter=meter)

    assert hotel.name == mock_hotel.name
    assert meter.hotel.name == hotel.name
    assert half_hourly.meter.unit == meter.unit


def test_view_graph(client, mock_half_hourly):
    # Check correct template is rendered
    data = mock_half_hourly
    url = reverse('meter_graph', kwargs={'meter_id': data.meter.id})
    response = client.get(url)

    assert response.status_code == 200
    assert response.templates[0].name == 'meter_charts.html'


@pytest.fixture
def mock_csv_file_hotel():
    with open('test.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(['id', 'name'])
        writer.writerow(['9539', 'Aberdeen'])

        data_file = csv_file

    return data_file


@pytest.fixture
def mock_csv_file_meter():
    with open('test.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(['building_id', 'id', 'fuel', 'unit'])
        writer.writerow(['9539', '196327', 'Water', 'm3'])

        data_file = csv_file

    return data_file


@pytest.fixture
def mock_csv_file_halfhourly():
    with open('test.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(['consumption', 'meter_id', 'reading_date_time'])
        writer.writerow(['66.642', '8718', '2018-12-01 00:00'])

        data_file = csv_file

    return data_file


def test_process_csv_hotel(db, mock_csv_file_hotel):
    csv_class = CsvUpload()

    with open('test.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        csv_class.process_csv('hotel', reader)

    os.remove('test.csv')
    # Should have only create one object
    hotels = Hotel.objects.all()

    assert len(hotels) == 1
    assert hotels[0].name == 'Aberdeen'


def test_process_csv_meter(db, mock_csv_file_meter):
    csv_class = CsvUpload()
    HotelFactory(id=9539, name='Aberdeen')

    with open('test.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        csv_class.process_csv('meter', reader)

    os.remove('test.csv')
    # Should have only create one object
    meters = Meter.objects.all()

    assert len(meters) == 1
    assert meters[0].hotel.name == 'Aberdeen'
    assert meters[0].fuel == 'water'
    assert meters[0].unit == 'm3'


def test_process_csv_halfhourly(db, mock_csv_file_halfhourly):
    csv_class = CsvUpload()
    MeterFactory(id=8718)

    with open('test.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        csv_class.process_csv('halfhourly', reader)

    os.remove('test.csv')
    # Should have only create one object
    halfhourly = HalfHourly.objects.all()

    assert len(halfhourly) == 1
    assert halfhourly[0].meter_id == 8718
    assert halfhourly[0].consumption == 66.642


def test_nothing_is_created(db, mock_csv_file_hotel):
    csv_class = CsvUpload()

    # Check no object is created when the incorrect data_type is given
    with open('test.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        csv_class.process_csv('funky', reader)

    os.remove('test.csv')

    hotels = Hotel.objects.all()
    meters = Meter.objects.all()
    halfhourly = HalfHourly.objects.all()

    assert len(hotels) == 0
    assert len(meters) == 0
    assert len(halfhourly) == 0
