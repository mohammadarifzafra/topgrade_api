from django.urls import path
from ninja import NinjaAPI
from .views import api

urlpatterns = [
    path("api/", api.urls),
]