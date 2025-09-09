from django.contrib import admin
from .models import CustomUser, OTPVerification, PhoneOTPVerification

# Register your models here.
admin.site.register(CustomUser)

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
