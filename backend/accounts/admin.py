from django.contrib import admin
from .models import User, TechnicianProfile, OTP

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'first_name', 'last_name', 'role', 'is_phone_verified')
    list_filter = ('role', 'is_phone_verified')
    search_fields = ('email', 'phone', 'first_name', 'last_name')

@admin.register(TechnicianProfile)
class TechnicianProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'service_type', 'is_approved', 'is_available', 'rating')
    list_filter = ('service_type', 'is_approved', 'is_available')

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('phone', 'otp_code', 'is_used', 'created_at')
