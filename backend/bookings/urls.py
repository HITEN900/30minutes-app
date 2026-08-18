from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_bookings, name='get_bookings'),
    path('create/', views.create_booking, name='create_booking'),
    path('<int:booking_id>/update-status/', views.update_booking_status, name='update_booking_status'),
]
