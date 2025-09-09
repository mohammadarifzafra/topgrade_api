from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
import datetime

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        username = email.split('@')[0]  # Auto-generate username from email
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    fullname = models.CharField(max_length=255, blank=True, null=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def save(self, *args, **kwargs):
        if self.email and not self.username:
            # Extract username from email (part before @)
            self.username = self.email.split('@')[0]
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.email


class OTPVerification(models.Model):
    email = models.EmailField()
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        unique_together = ['email']
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            # OTP verification expires after 10 minutes
            self.expires_at = timezone.now() + datetime.timedelta(minutes=10)
        super().save(*args, **kwargs)
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def __str__(self):
        return f"OTP for {self.email} - Verified: {self.is_verified}"


class PhoneOTPVerification(models.Model):
    phone_number = models.CharField(max_length=15)
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        unique_together = ['phone_number']
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            # OTP verification expires after 10 minutes
            self.expires_at = timezone.now() + datetime.timedelta(minutes=10)
        super().save(*args, **kwargs)
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def __str__(self):
        return f"Phone OTP for {self.phone_number} - Verified: {self.is_verified}"
