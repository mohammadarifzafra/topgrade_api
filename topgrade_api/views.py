from ninja import NinjaAPI
from ninja.security import HttpBearer
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from .schemas import AreaOfInterestSchema

User = get_user_model()

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            # Validate the token
            UntypedToken(token)
            # Get user from token
            from rest_framework_simplejwt.tokens import AccessToken
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            user = User.objects.get(id=user_id)
            return user
        except (InvalidToken, TokenError, User.DoesNotExist):
            return None

# Initialize Django Ninja API for general endpoints
api = NinjaAPI(version="1.0.0", title="General API")

# Example endpoint - you can add your other non-auth endpoints here
@api.get("/health")
def health_check(request):
    """
    Health check endpoint
    """
    return {"status": "healthy", "message": "API is running"}

@api.post("/add-area-of-interest", auth=AuthBearer())
def add_area_of_interest(request, data: AreaOfInterestSchema):
    """
    Add area of interest for authenticated user
    """
    try:
        user = request.auth
        user.area_of_intrest = data.area_of_intrest
        user.save()
        
        return {
            "success": True,
            "message": "Area of interest updated successfully",
            "area_of_intrest": user.area_of_intrest
        }
    except Exception as e:
        return JsonResponse({"message": f"Error updating area of interest: {str(e)}"}, status=500)