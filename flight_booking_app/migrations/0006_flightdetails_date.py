# Generated by Django 5.1 on 2024-10-11 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight_booking_app', '0005_remove_flighttickets_journy_data_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='flightdetails',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
