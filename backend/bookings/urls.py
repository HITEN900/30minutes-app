from django.urls import path
from . import views

urlpatterns = [
    path('technician/', views.get_technician_bookings, name='technician_bookings'),
    path('customer/', views.get_customer_bookings, name='customer_bookings'),
    path('<int:booking_id>/update-status/', views.update_booking_status, name='update_booking_status'),
]
