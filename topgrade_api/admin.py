from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, OTPVerification, PhoneOTPVerification

# Restrict admin access to superusers only
def admin_login_required(view_func):
    """
    Decorator to ensure only superusers can access Django admin
    """
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("Access denied. Only superusers can access the admin panel.")
        return view_func(request, *args, **kwargs)
    return wrapper

# Override admin site login
original_admin_view = admin.site.admin_view
admin.site.admin_view = lambda view, cacheable=False: original_admin_view(admin_login_required(view), cacheable)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'fullname', 'role', 'is_staff', 'is_active', 'date_joined']
    list_filter = ['role', 'is_staff', 'is_active', 'date_joined']
    search_fields = ['email', 'fullname', 'phone_number']
    ordering = ['email']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('fullname', 'phone_number', 'area_of_intrest')}),
        ('Role', {'fields': ('role',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'fullname', 'role'),
        }),
    )
    
    def has_module_permission(self, request):
        """Only superusers can access this module"""
        return request.user.is_superuser
    
    def has_view_permission(self, request, obj=None):
        """Only superusers can view users"""
        return request.user.is_superuser
    
    def has_add_permission(self, request):
        """Only superusers can add users"""
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        """Only superusers can change users"""
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        """Only superusers can delete users"""
        return request.user.is_superuser

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_verified', 'verified_at', 'expires_at', 'is_expired_status']
    list_filter = ['is_verified', 'verified_at', 'expires_at']
    search_fields = ['email']
    readonly_fields = ['verified_at']
    ordering = ['-expires_at']
    
    def is_expired_status(self, obj):
        return obj.is_expired()
    is_expired_status.boolean = True
    is_expired_status.short_description = 'Is Expired'
    
    def has_module_permission(self, request):
        """Only superusers can access this module"""
        return request.user.is_superuser
    
    def has_view_permission(self, request, obj=None):
        """Only superusers can view OTP verifications"""
        return request.user.is_superuser
    
    def has_add_permission(self, request):
        """Only superusers can add OTP verifications"""
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        """Only superusers can change OTP verifications"""
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        """Only superusers can delete OTP verifications"""
        return request.user.is_superuser


@admin.register(PhoneOTPVerification)
class PhoneOTPVerificationAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'is_verified', 'verified_at', 'expires_at', 'is_expired_status']
    list_filter = ['is_verified', 'verified_at', 'expires_at']
    search_fields = ['phone_number']
    readonly_fields = ['verified_at']
    ordering = ['-expires_at']
    
    def is_expired_status(self, obj):
        return obj.is_expired()
    is_expired_status.boolean = True
    is_expired_status.short_description = 'Is Expired'
    
    def has_module_permission(self, request):
        """Only superusers can access this module"""
        return request.user.is_superuser
    
    def has_view_permission(self, request, obj=None):
        """Only superusers can view phone OTP verifications"""
        return request.user.is_superuser
    
    def has_add_permission(self, request):
        """Only superusers can add phone OTP verifications"""
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        """Only superusers can change phone OTP verifications"""
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        """Only superusers can delete phone OTP verifications"""
        return request.user.is_superuser
