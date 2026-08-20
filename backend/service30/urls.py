from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.http import HttpResponse

def serve_index(request):
    try:
        return render(request, 'index.html')
    except:
        return HttpResponse("<h1>🚀 30 Minutes API</h1><p>Service is running!</p>")

def serve_register(request):
    return render(request, 'register.html')

def serve_user_register(request):
    return render(request, 'user-register.html')

def serve_professional_register(request):
    return render(request, 'professional-register.html')

def serve_professional_dashboard(request):
    return render(request, 'professional-dashboard.html')

def serve_professional_bookings(request):
    return render(request, 'professional-bookings.html')

def serve_professional_earnings(request):
    return render(request, 'professional-earnings.html')

def serve_user_dashboard(request):
    return render(request, 'user-dashboard.html')

urlpatterns = [
    path('', serve_index, name='home'),
    path('register/', serve_register, name='register'),
    path('user-register/', serve_user_register, name='user_register'),
    path('professional-register/', serve_professional_register, name='professional_register'),
    path('professional-dashboard/', serve_professional_dashboard, name='professional_dashboard'),
    path('professional-bookings/', serve_professional_bookings, name='professional_bookings'),
    path('professional-earnings/', serve_professional_earnings, name='professional_earnings'),
    path('user-dashboard/', serve_user_dashboard, name='user_dashboard'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/services/', include('services.urls')),
    path('api/bookings/', include('bookings.urls')),
    path('api/notifications/', include('notifications.urls')),
]
