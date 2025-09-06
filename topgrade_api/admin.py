from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email_or_phone = forms.CharField(
        max_length=254,
        help_text='Enter either an email address or phone number',
        label='Email or Phone Number'
    )
    
    class Meta:
        model = CustomUser
        fields = ('email_or_phone', 'first_name', 'last_name')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the default username field
        if 'username' in self.fields:
            del self.fields['username']
    
    def clean_email_or_phone(self):
        email_or_phone = self.cleaned_data.get('email_or_phone')
        if not email_or_phone:
            raise forms.ValidationError('Either email or phone number is required')
        
        # Check if it's an email or phone
        if '@' in email_or_phone:
            # It's an email - check if it already exists
            if CustomUser.objects.filter(email=email_or_phone).exists():
                raise forms.ValidationError('A user with this email already exists.')
        else:
            # It's a phone number - check if it already exists
            if CustomUser.objects.filter(phone_number=email_or_phone).exists():
                raise forms.ValidationError('A user with this phone number already exists.')
        
        return email_or_phone
    
    def save(self, commit=True):
        user = super().save(commit=False)
        email_or_phone = self.cleaned_data['email_or_phone']
        
        if '@' in email_or_phone:
            user.email = email_or_phone
            user.phone_number = None
        else:
            user.phone_number = email_or_phone
            user.email = None
            
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'phone_number', 'first_name', 'last_name', 'is_active', 'is_staff')


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    
    list_display = ('get_username', 'email', 'phone_number', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('email', 'phone_number', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    
    readonly_fields = ('date_joined',)
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email_or_phone', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    
    def get_username(self, obj):
        return obj.email or obj.phone_number or f'User {obj.id}'
    get_username.short_description = 'Username'
    get_username.admin_order_field = 'email'


# Register the custom user model with the custom admin
admin.site.register(CustomUser, CustomUserAdmin)
