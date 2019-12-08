from django import forms


CSV_TYPE = [
    ('hotel', 'Hotel'),
    ('meter', 'Meter'),
    ('halfhourly', 'Half Hourly'),
]


class UploadCSVForm(forms.Form):
    data_type = forms.ChoiceField(label='Type of data to upload', choices=CSV_TYPE)
    csv_file = forms.FileField()
