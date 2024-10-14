from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# FLIGHT USER MODELS
class FlightUsers(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    passport_no=models.CharField(max_length=8)
    aadhar_no=models.BigIntegerField()
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    pincode=models.PositiveIntegerField()
    user_image=models.ImageField(upload_to="user_images",blank=True,null=True)


    def __str__(self):
        return str(self.user)