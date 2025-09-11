from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model

User = get_user_model()

def admin_required(view_func):
    """
    Decorator to ensure only admin users (superusers) can access dashboard views
    """
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/dashboard/signin/')
        
        if not request.user.is_superuser:
            return HttpResponseForbidden("Access denied. Only administrators can access the dashboard.")
        
        return view_func(request, *args, **kwargs)
    return wrapper

def signin_view(request):
    """
    Custom login view for dashboard - only allows admin users (superusers)
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Use AdminOnlyBackend for authentication
        user = authenticate(request, username=email, password=password)
        
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('dashboard:dashboard')
        else:
            messages.error(request, 'Invalid credentials or you are not authorized to access the dashboard.')
    
    return render(request, 'dashboard/signin.html')

def dashboard_logout(request):
    """
    Logout view for dashboard
    """
    logout(request)
    return redirect('dashboard:login')

@admin_required
def dashboard_home(request):
    """
    Dashboard home view - only accessible by admin users (superusers)
    """
    context = {
        'user': request.user,
        'total_students': User.objects.filter(role='student').count(),
        'total_admins': User.objects.filter(is_superuser=True).count(),
    }
    return render(request, 'dashboard/base.html', context)