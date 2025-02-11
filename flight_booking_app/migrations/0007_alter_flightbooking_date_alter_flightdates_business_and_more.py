# Generated by Django 5.1 on 2024-10-11 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight_booking_app', '0006_flightdetails_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flightbooking',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='flightdates',
            name='business',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='flightdates',
            name='economic',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='flightdates',
            name='first_class',
            field=models.IntegerField(default=0),
        ),
    ]
