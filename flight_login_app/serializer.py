from rest_framework import serializers
from django.contrib.auth.models import User

class USERSERIALIZER(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','email','password']
    # HEAR IT CREATE THE USER
    def create(self, validated_data):
        user=User(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

