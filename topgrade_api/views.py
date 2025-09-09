from ninja import NinjaAPI
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from .schemas import LoginSchema

# Initialize Django Ninja API
api = NinjaAPI()

@api.post("/login")
def login(request, credentials: LoginSchema):
    """
    Simple login API that returns access_token and refresh_token
    """
    user = authenticate(username=credentials.email, password=credentials.password)
    
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return {
            "success": True,
            "message": "Login successful",
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        }
    else:
        return JsonResponse({"message": "Invalid credentials"}, status=401)
