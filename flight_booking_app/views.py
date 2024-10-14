from flight_booking_app.models import FLIGHTDETAILS,FLIGHTTICKETS,FLIGHTBOOKING,FLIGHTDATES
from flight_booking_app.serializer import FLIGHTSERIALIZER,FLIGHTTICKETSERIALIZER,FLIGHTBOOKINGSERIALIZER,FLIGHTDATESERIALIZER
from rest_framework.response import Response
from rest_framework import  permissions
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from flight_booking_app.serializer import USERDETAILSSERIALIZER
from datetime import datetime
from flight_booking_app.utils import GETDATE
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime
# Create your views here.
#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#

#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#
class FlightApiView(APIView):
    # AUTHENTICATION CHECKING
    authentication_classes=[JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    # GETTING THE DATA OF FLIGHT DETAILS
    queryset = FLIGHTDETAILS.objects.all()
    serializer_class = FLIGHTSERIALIZER
    # USED FOR STORING THE SEARCH DATA PERMANENTLY
    class_date=None
    def get (self,request,id=0,*args,**kwargs):
        # THIS BLOCK ONLY USED FOR RETRIVE FLIGHT BASED ON ID
        if id:
            flights=FLIGHTDETAILS.objects.get(id=id) # GETTING FLIGHT DATA
            query_serializer=FLIGHTSERIALIZER(flights) # SERIALIZE THE DATA
            flight=query_serializer.data # GETTING FLIGHT FROM SERIALIZER
            flight['logo']=request.build_absolute_uri(flight['logo']) # ADDDING THE DOMAIN URL
            if FlightApiView.class_date == None: # CHECKING THE DATE IN SEARCHED DATA
                flight['day']=GETDATE(flight['day']) # IF THE CLASS DATE NONE THE IT GIVE THE DATE BASED ON  DAY OF THE UPCOMMING DATE
            else:
                flight['day']=FlightApiView.class_date #IF IT IS NOT NONE THEN IT STORE THE SEARCHED DATA 
            # GETTING OR CREATING THE DATE OBJECT BASED ON DATE AND THE PARTICULAR FLIGHT
            date,created=FLIGHTDATES.objects.get_or_create(flightdate=flight['day'],flight_name=flights)
            # BASED ON DATE AND FLIGHT HEAR WE ARE MINUS THE SHEETS BOKKED SHEETS OF THE DIFFERENT CLASSES
            flight['economy']-=date.economic 
            flight['business']-=date.business
            flight['fast_class']-=date.first_class
            # RETURNING THE SERIALIZEABLE FLIGHT DATA
            return Response(flight)
        else:
            # THIS BLOCK ONLY USED FOR RETRIVE ALL THE FLIGHTS
            FlightApiView.class_date=None # UPDATEING THE VALUE TO NONE FOR EVERY TIME OF SERCHING ALL THE FLIGHTS
            flights=FLIGHTDETAILS.objects.all() # GETTING ALL THE FLIGHTS FROM THE DATA BASE
            query_serializer=FLIGHTSERIALIZER(flights,many=True) #SERIALIZE ALL THE FLIGHT RECORDS
            for flight in query_serializer.data:
                flight['logo']=request.build_absolute_uri(flight['logo']) # ADDING THE DOMAIN URL
                flight['day']=GETDATE(flight['day']) #GETTING THE UPCOMMING DATE FROM THE DAY
                perticular_flight=FLIGHTDETAILS.objects.get(id=flight['id']) #GETTING THE FILE OBJECT
                # GETIING OR CREATING THE OBJECT BASED ON DATE AND PARTICULAR FLIGHT
                date,created=FLIGHTDATES.objects.get_or_create(flightdate=flight['day'],flight_name=perticular_flight)
                # BASED ON DATE AND FLIGHT HEAR WE ARE MINUS THE SHEETS BOKKED SHEETS OF THE DIFFERENT CLASSES
                flight['economy']-=date.economic
                flight['business']-=date.business
                flight['fast_class']-=date.first_class
            # RETURNING THE SERIALIZEABLE FLIGHT DATA
            return Response (query_serializer.data)
        
    def post(self,request,*args,**kwargs):
        # FETCHING ALL THE RECORD FROM THE REQUEST DATA PASSED IN FRONTEND
        depreture_city=((request.data['from']).strip()).capitalize()
        destination_city=((request.data['to']).strip()).capitalize()
        date=request.data['date']
        # IF DATE IS PRESENT THIS BLOCK WILL BE EXECUTED
        if date:
            # CONVERTING THE DATE TO DAY FOR MATCHING WITH THE FLIGHT DAY
            date_object = datetime.strptime(date, "%Y-%m-%d").date()
            day_of_week = date_object.strftime("%A").upper()
            # SERCING THE FLIGHT BASED ON DEPRATURECITY AND DESTINATION CITY IN THE PARTICULAR DATE
            flights=FLIGHTDETAILS.objects.filter(depreture_city=depreture_city,destination_city=destination_city,day=day_of_week)
        # IF DATE IS NOT PRESENT THIS BLOCK WILL BE EXECUTED
        else:
            # SERCHING THE FLIGHTS BASED ON THE DEPRATURECITY AND DESTINATION CITY
            flights=FLIGHTDETAILS.objects.filter(depreture_city=depreture_city,destination_city=destination_city)
        # SERIALIZE THE FLIGHT DATA
        query_serializer=FLIGHTSERIALIZER(flights,many=True)
        for flight in query_serializer.data:
            flight['logo']=request.build_absolute_uri(flight['logo']) # ADDING THE DOMAIN URL
            if date:
                flight['day']=date # ASSIGN THE SERCH DATE TO THE FLIGHT DAY
                FlightApiView.class_date=date #UPDATING THE DATE BASED ON USER SERCHED DATE
            else:
                flight['day']=GETDATE(flight['day']) # IF USER NOT GIVING THE DATE IT ASSINGN THE UPCOMMING  DATE BASED ON FLIGHT DAY
        # RETURNING THE SERIALIZER FLIGHT SERCH DATA 
        return Response (query_serializer.data)
        

#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#

#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#
class TicketApiView(APIView):
     # AUTHENTICATION CHECKING
    authentication_classes=[JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
     # GETTING ALL THE FLIGHT DETAILS
    queryset=FLIGHTTICKETS.objects.all()
    serializer_class=FLIGHTTICKETSERIALIZER
    
    def get (self,request,*args,**kwargs):
        # GETTING OR CREATING THE BOOKING WHICH IS NOT COMPLITED
        booking,created=FLIGHTBOOKING.objects.get_or_create(user=request.user,complete=False)
        # BASED ON THE BOOKING WE ARE FETCHING THE TICKETS
        tickets=FLIGHTTICKETS.objects.filter(booking=booking)
        # THE FETCHED TICKETS CONVERING TO SERIALIZEABLE DATA
        ticket_serializer=FLIGHTTICKETSERIALIZER(tickets,many=True)
        # RETURNING THE SERIALIZEABLE DATA+
        return Response(ticket_serializer.data)
    
    def post (self,request,*args,**kwargs):
        # FETCHING THE DATA SEND IN FRONTEND
        flight_id=request.data["flight"]
        booking_date=request.data["journy_date"]
        class_of_service=request.data["class_of_service"]
        # GETTING THE PERTICULAR FLIGHT DATA FROM THE MODELS
        flight=FLIGHTDETAILS.objects.get(id=flight_id)
        # GETIING OR CREATING THE DATE OBJECT BASED ON USER JOURNY DATE AND THE PARTICULAR FLIGHT
        date,created=FLIGHTDATES.objects.get_or_create(flightdate=booking_date,flight_name=flight)
        # GETTING OR CREATING THE BOOKING BASED ON USER WHICH IS NOT COMPLITED 
        booking,created=FLIGHTBOOKING.objects.get_or_create(user=request.user,complete=False)
        # SHEETS UPGRADATION IN THE PARICULAR DATE OBJECT AND ASSIGN SHEET NUMBER IN TICKET
        if class_of_service=="ECONOMICS" and date.economic<flight.economy :
            date.economic+=1
            request.data['sheet_number']=class_of_service[:5:]+" "+str(date.economic)
        elif class_of_service=="BUSINESS" and date.business<flight.business :
            date.business+=1
            request.data['sheet_number']=class_of_service[:5:]+" "+str(date.business)
        elif class_of_service=="FIRST CLASS" and date.first_class<flight.fast_class :
            date.first_class+=1
            request.data['sheet_number']=class_of_service[:5:]+" "+str(date.first_class)
        else:
            return Response({"error": "Booking is full."}, status=status.HTTP_400_BAD_REQUEST)
        # DATE OBJECT SAVEING HEAR
        date.save()
        # EXTEND AND INITIALIZE ALL THE FILDS REQUIRED FOR A TICKETS
        request.data['booking']=booking.id
        request.data['journy_date']=date.id
        # SERIALIZING THE TICKETS DATA
        ticket_serializer=FLIGHTTICKETSERIALIZER(data=request.data)
        # CHECKING IT VAID OR NOT
        if ticket_serializer.is_valid():
            # SAVING THE DATA IN THE MODELS
            ticket_serializer.save()
            # RETURNING SUCESS MESSAGE
            return Response({"success": "Booking created successfully.", "booking": booking.id}, status=status.HTTP_201_CREATED)
        # IF THE TICKETE_SERIALIZER NOT VALID THEN RTURNING ERROR MESSAGE
        return Response({"error": "something eroor raised"}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id=0,*args,**kwargs):
        # DELETING RECORD FROM THE DATABASE BASED ON ID
        if id:
            # GETTING TICKET DETAILS
            ticket=FLIGHTTICKETS.objects.get(id=id)
            # GETTING THE FLIGHT DETAILS
            flight=FLIGHTDETAILS.objects.get(id=ticket.flight.id)
            # GETTING THE DATE FROM THE DATABASE BASED ON TICKET DATE AND THE FLIGHT
            date=FLIGHTDATES.objects.get(flightdate=ticket.journy_date.flightdate,flight_name=flight)
            # DESCRESING THE DATE OBJECT VALUE BASED ON THE TICKET CLASS OF SERVICE
            if ticket.class_of_service=="ECONOMICS":
                date.economic-=1
            elif ticket.class_of_service=="BUSINESS":
                date.business-=1
            elif ticket.class_of_service=="FIRST CLASS":
                date.first_class-=1
            # SAVING DATE OBJECT
            date.save()
            # DELETING THE TICKET
            ticket.delete()
            # SENDING SUCCESS MESSAGE
            return Response({"success": "deleted sucessfully."}, status=status.HTTP_201_CREATED)
        return Response({"error": "can't delete the tickets"}, status=status.HTTP_400_BAD_REQUEST)

#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#

#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#
class BookingHistoryApiView(APIView):
    # AUTHENTICATION CHECKING
    authentication_classes=[JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
   
    def get(self,request):
        # FETCHING ALL TTHE TICKETS BASED ON USER WITH DESCENDING ORDER
        tickets=FLIGHTTICKETS.objects.filter(user=request.user).order_by("-id")
        # CONVERTING TO SERIALIZABLE DATA
        ticket_serializer=FLIGHTTICKETSERIALIZER(tickets,many=True)
        for ticket in ticket_serializer.data:
            # IN TICKET USER ASSIGNING THE WHOLE USER DETAILS
            user=User.objects.get(id=ticket['user'])
            user_serializer=USERDETAILSSERIALIZER(user)
            ticket['user']=user_serializer.data
            # IN TICKET FLIGHTS ASSIGNING THE WHOLE FLIGHT DETAILS
            flight=FLIGHTDETAILS.objects.get(id=ticket['flight'])
            flight_serializer=FLIGHTSERIALIZER(flight)
            ticket['flight']=flight_serializer.data
            # IN TICKET BOOKING ASSIGNING THE WHOLE BOOKING DETAILS
            booking=FLIGHTBOOKING.objects.get(id=ticket['booking'])
            booking_serializer=FLIGHTBOOKINGSERIALIZER(booking)
            ticket['booking']=booking_serializer.data
            # IN TICKET DATES ASSIGNING THE WHOLE DATE SETAILS
            dates=FLIGHTDATES.objects.get(id=ticket['journy_date'])
            dates_serializer=FLIGHTDATESERIALIZER(dates)
            ticket['journy_date']=dates_serializer.data
            # ADDING DOMAIN URL IN THE LOGO
            ticket['flight']['logo']=request.build_absolute_uri(ticket['flight']['logo'])
        # RETUTNGIN THE SERIALIZER TICKET DATA
        return Response(ticket_serializer.data)
    
    def post (self,request,*args,**kwargs):
        # GETTING OR CREATED BOOKING FROM THE DATA BASE BASED ON USER WHICH NOT COMPLETED
        booking,created=FLIGHTBOOKING.objects.get_or_create(user=request.user,complete=False)
        # ASSIGNING ALL THE DATA AND COMPLETING THE BOOKING
        booking.booking_id="SPANYAIRLINE"+(datetime.now()).strftime('%Y%m%d%H%M%S')
        booking.booking_status="CONFIRMED"
        booking.complete=True
        booking.save()
        # RETRNING SUCCES MESAGE 
        return Response({"success": "deleted sucessfully."}, status=status.HTTP_201_CREATED)

    
    def delete (self,request,*args,**kwargs):
        # REMOVING ALL THE TICKETS OF THE CURRENT BOOKING
        # GEETING OR CREATING BOOKING BASED ON USER AND COMPLETE FALSE
        booking ,create =FLIGHTBOOKING.objects.get_or_create(user=request.user,complete=False) 
        # GETTING ALL THE TICKETS BASED ON THE BOOKING
        tickets=FLIGHTTICKETS.objects.filter(booking=booking)
        for ticket in tickets:
            # GETTING FLIGHT OBJECT BASED ON TICKET FLIGHT
            flight=FLIGHTDETAILS.objects.get(id=ticket.flight.id)
            # GETTING DATE OBJECT BASED ON DATE TICKET DATE AND FLIGHT
            date=FLIGHTDATES.objects.get(id=ticket.journy_date.id,flight_name=flight.id)
            # UPDATEINGT THE THE SHEET NUMBER BASED ON CLASS OF SERVICE
            if ticket.class_of_service=="ECONOMICS":
                date.economic-=1
            elif ticket.class_of_service=="BUSINESS":
                date.business-=1
            elif ticket.class_of_service=="FIRST CLASS":
                date.first_class-=1
            # SAVING THE DATE 
            date.save()
            # DELETING THE TICKET
            ticket.delete()
        # RETURNING SUCESS MESSAGE 
        return Response({"success": "deleted sucessfully."}, status=status.HTTP_201_CREATED)



        





