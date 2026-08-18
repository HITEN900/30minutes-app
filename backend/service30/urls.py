from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("""
        <!DOCTYPE html>
        <html>
        <head><title>30 Minutes API</title></head>
        <body style="font-family: Arial; text-align: center; padding: 50px;">
            <h1>🚀 30 Minutes API</h1>
            <p>Welcome to the 30 Minutes Service Booking API</p>
            <h3>Endpoints:</h3>
            <ul style="list-style: none; padding: 0;">
                <li><strong>POST</strong> /api/auth/register/ - Register</li>
                <li><strong>POST</strong> /api/auth/verify-otp/ - Verify OTP</li>
                <li><strong>POST</strong> /api/auth/login/ - Login</li>
                <li><strong>GET</strong> /api/auth/profile/ - Get Profile</li>
                <li><strong>GET</strong> /api/services/ - Get Services</li>
                <li><strong>POST</strong> /api/services/create/ - Create Service</li>
                <li><strong>POST</strong> /api/bookings/create/ - Create Booking</li>
                <li><strong>GET</strong> /api/bookings/ - Get Bookings</li>
                <li><strong>GET</strong> /api/notifications/ - Get Notifications</li>
            </ul>
        </body>
        </html>
    """)

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/services/', include('services.urls')),
    path('api/bookings/', include('bookings.urls')),
    path('api/notifications/', include('notifications.urls')),
]
