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
        extra_fields.setdefault('role', 'admin')  # Set role to admin for superusers

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    USER_ROLES = [
        ('student', 'Student'),
        ('admin', 'Admin'),
    ]
    
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    fullname = models.CharField(max_length=255, blank=True, null=True)
    area_of_intrest = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=20, choices=USER_ROLES, default='student')
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

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Program(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='programs')
    image = models.ImageField(upload_to='program_images/', blank=True, null=True)
    batch_starts = models.CharField(max_length=50)
    available_slots = models.IntegerField()
    duration = models.CharField(max_length=50)
    program_rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    job_openings = models.CharField(max_length=50)
    global_market_size = models.CharField(max_length=50)
    avg_annual_salary = models.CharField(max_length=50)
    is_best_seller = models.BooleanField(default=False)
    icon = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class Syllabus(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='syllabuses')
    module_title = models.CharField(max_length=200)

    def __str__(self):
        return self.module_title

class Topic(models.Model):
    syllabus = models.ForeignKey(Syllabus, on_delete=models.CASCADE, related_name='topics')
    topic_title = models.CharField(max_length=200)
    video_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.topic_title