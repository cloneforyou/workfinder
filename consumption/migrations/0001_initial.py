# Generated by Django 3.0 on 2019-12-08 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Meter',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fuel', models.CharField(choices=[('water', 'Water'), ('natural gas', 'Natural Gas'), ('electricity', 'Electricity')], max_length=16)),
                ('unit', models.CharField(choices=[('m3', 'm3'), ('kWh', 'kWh')], max_length=3)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meter', to='consumption.Hotel')),
            ],
        ),
        migrations.CreateModel(
            name='HalfHourly',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consumption', models.FloatField(default=0)),
                ('reading_date_time', models.DateTimeField()),
                ('meter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='halfhourly', to='consumption.Meter')),
            ],
        ),
    ]
