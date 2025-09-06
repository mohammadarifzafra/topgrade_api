from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email=None, password=None, **extra_fields):
        # Handle both email and phone_number cases
        email_or_phone = email or extra_fields.get('phone_number')
        
        if not email_or_phone:
            raise ValueError('Either email or phone number must be provided')
        
        if email and '@' in email:
            # It's an email
            email = self.normalize_email(email)
            user = self.model(email=email, **extra_fields)
        elif extra_fields.get('phone_number'):
            # It's a phone number
            user = self.model(phone_number=extra_fields.pop('phone_number'), **extra_fields)
        else:
            # Fallback: treat as email if it contains @, otherwise as phone
            if '@' in email_or_phone:
                email = self.normalize_email(email_or_phone)
                user = self.model(email=email, **extra_fields)
            else:
                user = self.model(phone_number=email_or_phone, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    
    # Keep the original method for backward compatibility
    def create_user_with_email_or_phone(self, email_or_phone, password=None, **extra_fields):
        if not email_or_phone:
            raise ValueError('The Email or Phone field must be set')
        
        if '@' in email_or_phone:
            return self.create_user(email=email_or_phone, password=password, **extra_fields)
        else:
            return self.create_user(email=None, password=password, phone_number=email_or_phone, **extra_fields)
        
class CustomUser(AbstractBaseUser, PermissionsMixin):
  email = models.EmailField(unique=True, blank=True, null=True)
  phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
  first_name = models.CharField(max_length=30, blank=True, null=True)
  last_name = models.CharField(max_length=30, blank=True, null=True)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  date_joined = models.DateTimeField(auto_now_add=True)

  objects = CustomUserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

  class Meta:
    db_table = 'auth_user'

  def __str__(self):
    return self.email or self.phone_number or str(self.id)

  @property
  def username(self):
    return self.email or self.phone_number

  def clean(self):
    super().clean()
    if not self.email and not self.phone_number:
      raise ValueError('The Email or Phone Number must be provided')
    if self.email and self.phone_number:
      raise ValueError('Provide either email or phone number, not both')
      
    
  
  
        