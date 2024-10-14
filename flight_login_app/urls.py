from django.urls import path
from flight_login_app.views import *
urlpatterns=[
    path("registration",UserRegistrationView.as_view()),
    path("login",UserLoginView.as_view()),
    path("logout",UserLogoutView.as_view()),
]