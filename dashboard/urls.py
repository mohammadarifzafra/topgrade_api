from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Dashboard authentication
    path('signin/', views.signin_view, name='login'),
    path('logout/', views.dashboard_logout, name='logout'),
    
    # Dashboard main views
    path('', views.dashboard_home, name='dashboard'),
]