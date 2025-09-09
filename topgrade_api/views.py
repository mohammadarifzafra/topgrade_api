from ninja import NinjaAPI

# Initialize Django Ninja API for general endpoints
api = NinjaAPI(version="1.0.0", title="General API")

# Example endpoint - you can add your other non-auth endpoints here
@api.get("/health")
def health_check(request):
    """
    Health check endpoint
    """
    return {"status": "healthy", "message": "API is running"}