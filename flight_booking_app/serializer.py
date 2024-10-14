from rest_framework import serializers
from flight_booking_app.models import FLIGHTDETAILS,FLIGHTTICKETS,FLIGHTBOOKING,FLIGHTDATES
from django.contrib.auth.models import User

class USERDETAILSSERIALIZER(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','email']

class FLIGHTSERIALIZER(serializers.ModelSerializer):
    class Meta:
        model=FLIGHTDETAILS
        fields="__all__"

class FLIGHTDATESERIALIZER(serializers.ModelSerializer):
    class Meta:
        model=FLIGHTDATES
        fields="__all__"

class FLIGHTTICKETSERIALIZER(serializers.ModelSerializer):
    class Meta:
        model=FLIGHTTICKETS
        fields="__all__"

class FLIGHTBOOKINGSERIALIZER(serializers.ModelSerializer):
    class Meta:
        model=FLIGHTBOOKING
        fields="__all__"