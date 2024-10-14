from django.urls import path
from flight_booking_app.views import *
urlpatterns=[
    path("flightapi",FlightApiView.as_view()),
    path("flightapi/<int:id>",FlightApiView.as_view()),
    path("ticketapi",TicketApiView.as_view()),
    path("ticketapi/<int:id>",TicketApiView.as_view()),
    path("booking-history",BookingHistoryApiView.as_view()),
]