from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# FLIGHT MODELS
class FLIGHTDETAILS(models.Model):
    airline=models.CharField(max_length=100)
    flight_number=models.CharField(max_length=100)
    depreture_city=models.CharField(max_length=100)
    destination_city=models.CharField(max_length=100)
    deprature_time=models.TimeField()
    arival_time=models.TimeField()
    price=models.PositiveBigIntegerField()
    economy=models.PositiveIntegerField(default=200)
    business=models.PositiveIntegerField(default=30)
    fast_class=models.PositiveIntegerField(default=30)
    color=models.CharField(max_length=50,default="blue")
    logo=models.ImageField(upload_to="logo",blank=True,null=True)

    DAYS_OF_WEEK = [('MONDAY', 'Monday'),('TUESDAY', 'Tuesday'),('WEDNESDAY', 'Wednesday'),('THURSDAY', 'Thursday'),('FRIDAY', 'Friday'),('SATURDAY', 'Saturday'),('SUNDAY', 'Sunday'),]
    day=models.CharField(max_length=10,choices=DAYS_OF_WEEK,default="MONDAY")
    date=models.DateField(blank=True,null=True)

    def __str__(self):
        return self.airline+"   -   "+self.flight_number

# FLIGHT DATES MODEL
class FLIGHTDATES(models.Model):
    flightdate=models.DateField()
    flight_name=models.ForeignKey(FLIGHTDETAILS,on_delete=models.CASCADE)
    business=models.IntegerField(default=0)
    economic=models.IntegerField(default=0)
    first_class=models.IntegerField(default=0)

    def __str__(self):
        return str(self.flightdate)+"   "+(self.flight_name.airline)+"  "+(self.flight_name.flight_number)
    
# FLIGHT BOOKINF MODELS
class FLIGHTBOOKING(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    booking_id=models.CharField(max_length=10,blank=True,null=True)
    date=models.DateField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    STATUS_CHOICES = [('PENDING', 'Pending'),('CONFIRMED', 'Confirmed'),('CANCELLED', 'Cancelled'),('COMPLETED', 'Completed'),]
    booking_status=models.CharField(max_length=50,choices=STATUS_CHOICES,default='PENDING')

    def __str__(self):
        return str(self.id)+" "+self.user.username

# FLIGHT TICKET MODELS
class FLIGHTTICKETS(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    booking=models.ForeignKey(FLIGHTBOOKING,on_delete=models.CASCADE)
    flight=models.ForeignKey(FLIGHTDETAILS,on_delete=models.CASCADE)
    passanger_name=models.CharField(max_length=100)
    passanger_age=models.PositiveIntegerField()
    gender=models.CharField(max_length=20)
    sheet_number=models.CharField(max_length=20)
    journy_date=models.ForeignKey(FLIGHTDATES,on_delete=models.CASCADE)
    class_of_service = models.CharField(max_length=20)

    def __str__(self):
        return self.passanger_name