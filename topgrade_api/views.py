from ninja import NinjaAPI
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from .schemas import LoginSchema, SignupSchema, RequestOtpSchema, ResetPasswordSchema
from .models import CustomUser
from django.utils import timezone
import uuid

# Initialize Django Ninja API
api = NinjaAPI()

@api.post("/signin")
def signin(request, credentials: LoginSchema):
    """
    Simple signin API that returns access_token and refresh_token
    """
    user = authenticate(username=credentials.email, password=credentials.password)
    
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return {
            "success": True,
            "message": "Signin successful",
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        }
    else:
        return JsonResponse({"message": "User not found"}, status=401)

@api.post("/signup")
def signup(request, user_data: SignupSchema):
    """
    User registration API
    """
    # Check if passwords match
    if user_data.password != user_data.confirm_password:
        return JsonResponse({"message": "Passwords do not match"}, status=400)
    
    # Check if user already exists
    if CustomUser.objects.filter(email=user_data.email).exists():
        return JsonResponse({"message": "User with this email already exists"}, status=400)
    
    try:
        # Create new user
        user = CustomUser.objects.create_user(
            email=user_data.email,
            password=user_data.password,
            fullname=user_data.fullname
        )
        
        # Generate tokens for immediate login
        refresh = RefreshToken.for_user(user)
        
        return {
            "success": True,
            "message": "User created successfully",
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        }
    except Exception as e:
        return JsonResponse({"message": "Error creating user"}, status=500)

@api.post("/request-otp")
def request_otp(request, otp_data: RequestOtpSchema):
    """
    Request OTP for password reset
    """
    try:
        # Check if user exists
        user = CustomUser.objects.get(email=otp_data.email)
        
        return {
            "success": True,
            "message": "OTP sent successfully",
            "otp": "654321"  # Static OTP
        }
        
    except CustomUser.DoesNotExist:
        return JsonResponse({"message": "User with this email does not exist"}, status=404)
    except Exception as e:
        return JsonResponse({"message": f"Error sending OTP: {str(e)}"}, status=500)

@api.post("/reset-password")
def reset_password(request, reset_data: ResetPasswordSchema):
    """
    Reset password API - allows users to reset their password using email, OTP and reset token
    """
    # Check if OTP is correct (static OTP: 654321)
    if reset_data.otp != "654321":
        return JsonResponse({"message": "Invalid OTP"}, status=400)
    
    # Check if passwords match
    if reset_data.new_password != reset_data.confirm_password:
        return JsonResponse({"message": "Passwords do not match"}, status=400)
    
    try:
        # Check if user exists
        user = CustomUser.objects.get(email=reset_data.email)
        
        # Update the password
        user.set_password(reset_data.new_password)
        user.save()
        
        return {
            "success": True,
            "message": "Password reset successfully"
        }
        
    except CustomUser.DoesNotExist:
        return JsonResponse({"message": "User with this email does not exist"}, status=404)
    except Exception as e:
        return JsonResponse({"message": "Error resetting password"}, status=500)
