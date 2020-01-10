import csv
import io

from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

from .form import UploadCSVForm
from .models import HalfHourly, Hotel, Meter


class CsvUpload(View):
    def process_csv(self, data_type, contents):
        for row in contents:
            if data_type == 'hotel':
                # Ignore rows with empty strings
                if row['id'] == '' or row['name'] == '':
                    continue
                Hotel.objects.update_or_create(id=row['id'], name=row['name'])

            if data_type == 'meter':
                hotel = Hotel.objects.get(id=row['building_id'])
                if hotel:
                    Meter.objects.update_or_create(
                        id=row['id'],
                        fuel=row['fuel'].lower(),
                        unit=row['unit'],
                        hotel=hotel
                    )
                else:
                    raise Exception('Building {} does not exist'.format(row['building_id']))

            if data_type == 'halfhourly':
                HalfHourly.objects.update_or_create(
                    consumption=row['consumption'],
                    meter_id=row['meter_id'],
                    reading_date_time=row['reading_date_time']
                )

        return


    def get(self, request):
        form = UploadCSVForm()
        buildings = Hotel.objects.prefetch_related('meter').all()

        return render(
            request,
            'index.html',
            {
                'form': form,
                'buildings': buildings
            }
        )


    def post(self, request):
        data = request.POST
        csv_file = request.FILES['csv_file'].read().decode('utf-8-sig')
        io_stream = io.StringIO(csv_file)
        csv_reader = csv.DictReader(io_stream, delimiter=',')
        self.process_csv(data['data_type'], csv_reader)

        return HttpResponse('Data added for {}'.format(data['data_type']))


def view_graph(request, meter_id):
    meter = Meter.objects.get(id=meter_id)
    data = HalfHourly.objects.filter(meter=meter)
    usage = list(data.values_list('consumption', flat=True))
    dates = [x.reading_date_time.isoformat() for x in data]

    return render(request, 'meter_charts.html', {
        'meter': meter,
        'usage': usage,
        'dates': dates
    })
