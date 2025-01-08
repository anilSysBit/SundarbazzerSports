from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
import random
from sportsApp.models import OTP
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import AccessToken, TokenError
from sportsApp.utils import send_otp_email

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

class ChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True, min_length=8)




class SendOTPView(APIView):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                otp_code = str(random.randint(1000, 9999))
                OTP.objects.update_or_create(user=user, defaults={'otp': otp_code})
                send_otp_email(email,otp_code)
                return Response({'message': 'OTP sent to email.'}, status=status.HTTP_200_OK)
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class VerifyOTPView(APIView):
    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_code = serializer.validated_data['otp']
            user = User.objects.filter(email=email).first()
            if user:
                otp_entry = OTP.objects.filter(user=user, otp=otp_code).first()
                if otp_entry and otp_entry.is_valid():
                    return Response({'message': 'OTP verified.'}, status=status.HTTP_200_OK)
                return Response({'error': 'Invalid or expired OTP.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_code = serializer.validated_data['otp']
            new_password = serializer.validated_data['new_password']
            user = User.objects.filter(email=email).first()
            if user:
                otp_entry = OTP.objects.filter(user=user, otp=otp_code).first()
                if otp_entry and otp_entry.is_valid():
                    user.set_password(new_password)
                    user.save()
                    otp_entry.delete()  # Delete OTP after successful use
                    return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
                return Response({'error': 'Invalid or expired OTP.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyLoginSerializer(serializers.Serializer):
    access_token = serializers.CharField()

    def validate_access_token(self, value):
        try:
            # Decode and validate the token
            token = AccessToken(value)
            
            # Fetch the user using the token's payload
            user_id = token.get("user_id")
            user = User.objects.filter(id=user_id).first()

            if not user:
                raise serializers.ValidationError("Invalid token: User does not exist.")

            if not user.is_active:
                raise serializers.ValidationError("User account is inactive.")
            
            # Return the user object for further use
            return user

        except TokenError as e:
            raise serializers.ValidationError(f"Invalid token: {str(e)}")


class VerifyLoginView(APIView):
    def post(self, request):
        serializer = VerifyLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['access_token']
            return Response({"message": "Access token is valid.", "user": user.username}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)