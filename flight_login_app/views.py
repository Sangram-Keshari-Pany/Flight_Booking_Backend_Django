from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import permissions, status
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from flight_login_app.serializer import USERSERIALIZER

# Create your views here.

class UserRegistrationView(GenericAPIView):
    # USER REGISTRATION VIEW
    serializer_class=USERSERIALIZER
    permission_classes = [permissions.AllowAny]

    def post(self,request,*args,**kwargs):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            return Response(
                {'user':USERSERIALIZER(user,context=self.get_serializer_context()).data,
                  'message':"user created"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(GenericAPIView):
    serializer_class=TokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]
    # VALIDATION AND TOKEN GENERATION FOR VALIDATE USER
    def post(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            tokens=serializer.validated_data
            user=serializer.user 
            return Response({
                'user':{
                    'id':user.pk,
                    'username':user.username,
                    'email':user.email,
                    'access':tokens['access'],
                    'refresh':tokens['refresh'],
                    },
            },status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    # LOGOUT FUNCTIONALITY
    def post(self,request):
        try:
            # Blacklist the user's refresh token
            # request.user.auth_token()  # If you use token blacklist feature
            
            return Response({'message': 'Logged out successfully.'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
