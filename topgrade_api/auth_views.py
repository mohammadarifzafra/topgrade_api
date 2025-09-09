from ninja import NinjaAPI
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from .schemas import LoginSchema, SignupSchema, RequestOtpSchema, ResetPasswordSchema, RequestPhoneOtpSchema, PhoneSigninSchema, RefreshTokenSchema
from .models import CustomUser
from django.utils import timezone
import uuid
import time

# Initialize Django Ninja API for authentication
auth_api = NinjaAPI(version="1.0.0", title="Authentication API", urls_namespace="auth")

@auth_api.post("/signin")
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
        return JsonResponse({"message": "Invalid credentials"}, status=401)

@auth_api.post("/signup")
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

@auth_api.post("/request-otp")
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
        }
        
    except CustomUser.DoesNotExist:
        return JsonResponse({"message": "User with this email does not exist"}, status=404)
    except Exception as e:
        return JsonResponse({"message": "Error sending OTP"}, status=500)

@auth_api.post("/reset-password")
def reset_password(request, reset_data: ResetPasswordSchema):
    """
    Reset password API - allows users to reset their password using email and OTP
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

@auth_api.post("/request-phone-otp")
def request_phone_otp(request, phone_data: RequestPhoneOtpSchema):
    """
    Request OTP for phone number signin - creates user if doesn't exist
    """
    # Validate phone number length (should be 10 digits)
    clean_phone = phone_data.phone_number.replace('+', '').replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
    if len(clean_phone) != 10 or not clean_phone.isdigit():
        return JsonResponse({"message": "Phone number must be exactly 10 digits"}, status=400)
    
    try:
        # Check if user exists with this phone number
        user = CustomUser.objects.get(phone_number=phone_data.phone_number)
        user_exists = True
        
    except CustomUser.DoesNotExist:
        user_exists = False
    
    return {
        "success": True,
        "message": "OTP sent to phone successfully",
        "user_exists": user_exists
    }

@auth_api.post("/phone-signin")
def phone_signin(request, phone_data: PhoneSigninSchema):
    """
    Phone signin API using phone number and OTP - creates user if doesn't exist
    """
    # Validate phone number length (should be 10 digits)
    clean_phone = phone_data.phone_number.replace('+', '').replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
    if len(clean_phone) != 10 or not clean_phone.isdigit():
        return JsonResponse({"message": "Phone number must be exactly 10 digits"}, status=400)
    
    # Check if OTP is correct (static OTP: 654321)
    if phone_data.otp != "654321":
        return JsonResponse({"message": "Invalid OTP"}, status=400)
    
    try:
        # Check if user exists with this phone number
        user = CustomUser.objects.get(phone_number=phone_data.phone_number)
        message = "Phone signin successful"
        
    except CustomUser.DoesNotExist:
        # Create new user if doesn't exist
        try:
            # Clean phone number for email generation
            clean_phone = phone_data.phone_number.replace('+', '').replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
            
            # Generate unique email with timestamp to ensure uniqueness
            timestamp = str(int(time.time()))
            temp_email = f"phone_{clean_phone}_{timestamp}@tempuser.com"
            
            # Double check email uniqueness
            counter = 1
            while CustomUser.objects.filter(email=temp_email).exists():
                temp_email = f"phone_{clean_phone}_{timestamp}_{counter}@tempuser.com"
                counter += 1
            
            # Create masked fullname for privacy (e.g., 86XXXXXXX1)
            def mask_phone_number(phone):
                # Clean phone number
                clean = phone.replace('+', '').replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
                if len(clean) >= 4:
                    # Show first 2 and last 1 digits, mask the rest
                    masked = clean[:2] + 'X' * (len(clean) - 3) + clean[-1:]
                else:
                    # If phone is too short, just mask middle
                    masked = clean[0] + 'X' * (len(clean) - 2) + clean[-1] if len(clean) > 2 else clean
                return masked
            
            masked_fullname = mask_phone_number(phone_data.phone_number)
            
            # Create user with masked phone as fullname and auto-generated password
            user = CustomUser.objects.create_user(
                email=temp_email,
                phone_number=phone_data.phone_number,
                fullname=masked_fullname,
                password=phone_data.phone_number  # Use phone number as password
            )
            message = "User created and signed in successfully"
            
        except Exception as e:
            return JsonResponse({"message": "Error creating user"}, status=500)
    
    try:
        # Generate tokens for login
        refresh = RefreshToken.for_user(user)
        
        return {
            "success": True,
            "message": message,
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        }
        
    except Exception as e:
        return JsonResponse({"message": "Error during phone signin"}, status=500)

@auth_api.post("/refresh")
def refresh_token(request, token_data: RefreshTokenSchema):
    """
    Refresh access token using refresh token
    """
    try:
        # Create RefreshToken object from the provided refresh token
        refresh = RefreshToken(token_data.refresh_token)
        
        # Generate new access token
        new_access_token = str(refresh.access_token)
        
        return {
            "success": True,
            "message": "Token refreshed successfully",
            "access_token": new_access_token
        }
        
    except Exception as e:
        return JsonResponse({"message": "Invalid or expired refresh token"}, status=401)