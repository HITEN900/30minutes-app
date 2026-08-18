from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('technician', 'Technician'),
        ('admin', 'Admin'),
    )
    
    phone_regex = RegexValidator(
        regex=r'^[0-9]{10}$',
        message='Phone number must be exactly 10 digits.'
    )
    
    phone = models.CharField(max_length=10, unique=True, validators=[phone_regex])
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    is_phone_verified = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone']
    
    def __str__(self):
        return f'{self.email} ({self.role})'
    
    class Meta:
        db_table = 'users'

class TechnicianProfile(models.Model):
    SERVICE_TYPES = (
        ('plumber', 'Plumber'),
        ('electrician', 'Electrician'),
        ('carpenter', 'Carpenter'),
        ('mechanic', 'Mechanic'),
        ('painter', 'Painter'),
        ('cleaner', 'Cleaner'),
        ('hvac', 'HVAC Technician'),
        ('others', 'Others'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='technician_profile')
    
    # Verification
    aadhaar_number = models.CharField(max_length=12, unique=True)
    voter_id = models.CharField(max_length=20, unique=True)
    is_aadhaar_verified = models.BooleanField(default=False)
    is_voter_verified = models.BooleanField(default=False)
    
    # Professional details
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES)
    experience_years = models.IntegerField(default=0)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    service_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_reviews = models.IntegerField(default=0)
    total_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    completed_bookings = models.IntegerField(default=0)
    
    # Status
    is_approved = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    is_busy = models.BooleanField(default=False)
    
    # Location
    current_lat = models.FloatField(null=True, blank=True)
    current_lng = models.FloatField(null=True, blank=True)
    
    bio = models.TextField(null=True, blank=True)
    skills = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user.email} - {self.service_type}'
    
    class Meta:
        db_table = 'technician_profiles'

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otps')
    phone = models.CharField(max_length=10)
    otp_code = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def is_valid(self):
        return not self.is_used and timezone.now() <= self.expires_at
    
    def __str__(self):
        return f'OTP for {self.phone}: {self.otp_code}'
    
    class Meta:
        db_table = 'otps'
