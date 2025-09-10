from django.urls import path
from ninja import NinjaAPI
from .views import api
from .auth_views import auth_api

urlpatterns = [
    path("", api.urls),
    path("auth/", auth_api.urls),
] 