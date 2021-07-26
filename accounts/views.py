from . import serializers
from rest_framework import views 
from django.shortcuts import redirect
from rest_framework.generics import CreateAPIView, ListCreateAPIView, ListAPIView 
from rest_framework.permissions import IsAuthenticated
from django.contrib.sessions.models import Session
from rest_framework import status 
from rest_framework.response import Response 
from .utils.phone_verif import send_verification 
from rest_framework_simplejwt.views import TokenObtainPairView
from . import models 

# Create your views here.
class RegisterAPIView(views.APIView):
    serializer_class = serializers.ProfileSerializer

    def get(self, request):
        message = "Welcome to PayDrop! Create an account today!"
        return Response(message, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            phone_number = serializer.validated_data['phone_number']
            account_created = models.Profile.objects.get(phone_number=phone_number)

            send_verification(phone_number, account_created.verification_code)
            return redirect('http://0.0.0.0:8000/api/auth/verify/')

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyAPIView(views.APIView):
    serializer_class = serializers.VerifySerializer

    def get(self, request):
        message = "verify your account with the OTP code you received via SMS"
        return Response(message, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                account_to_verify = models.Profile.objects.get(verification_code=serializer.validated_data['otp'])
                if account_to_verify.is_active == True:
                    return Response("No need for verification.")

                else:
                    account_to_verify.is_active = True 
                    account_to_verify.verification_code = "VERIFIED"
                    account_to_verify.save()
                    return Response(f"Account {account_to_verify.email} has been activated.", status=status.HTTP_200_OK)

            except:
                return Response("Invalid Verification Code", status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





