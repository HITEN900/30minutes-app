from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Booking
from accounts.models import TechnicianProfile
from notifications.models import Notification

User = get_user_model()

# ============================================
# GET ALL BOOKINGS FOR TECHNICIAN
# ============================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_technician_bookings(request):
    if request.user.role != 'technician':
        return Response({'error': 'Only technicians can access this'}, status=status.HTTP_403_FORBIDDEN)
    
    bookings = Booking.objects.filter(technician=request.user)
    data = []
    for booking in bookings:
        data.append({
            'id': booking.id,
            'customer_name': f"{booking.customer.first_name} {booking.customer.last_name}",
            'customer_phone': booking.customer.phone,
            'customer_address': booking.address,
            'service_type': booking.service_type,
            'status': booking.status,
            'total_amount': str(booking.total_amount),
            'scheduled_time': booking.scheduled_time.strftime('%Y-%m-%d %H:%M') if booking.scheduled_time else 'N/A',
            'created_at': booking.created_at.strftime('%Y-%m-%d %H:%M'),
            'payment_method': booking.payment_method
        })
    return Response(data, status=status.HTTP_200_OK)

# ============================================
# UPDATE BOOKING STATUS
# ============================================
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_booking_status(request, booking_id):
    if request.user.role != 'technician':
        return Response({'error': 'Only technicians can update booking status'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        booking = Booking.objects.get(id=booking_id, technician=request.user)
    except Booking.DoesNotExist:
        return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
    
    status_value = request.data.get('status')
    if not status_value:
        return Response({'error': 'Status is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    valid_statuses = ['accepted', 'in_progress', 'completed', 'cancelled', 'rejected']
    if status_value not in valid_statuses:
        return Response({'error': f'Invalid status. Valid: {valid_statuses}'}, status=status.HTTP_400_BAD_REQUEST)
    
    booking.status = status_value
    booking.save()
    
    # Notify customer
    Notification.objects.create(
        user=booking.customer,
        type='booking',
        title='Booking Status Updated',
        message=f'Your booking #{booking.id} status is now {status_value}'
    )
    
    return Response({
        'message': 'Booking status updated',
        'status': booking.status
    }, status=status.HTTP_200_OK)

# ============================================
# GET ALL BOOKINGS FOR CUSTOMER
# ============================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_customer_bookings(request):
    if request.user.role != 'customer':
        return Response({'error': 'Only customers can access this'}, status=status.HTTP_403_FORBIDDEN)
    
    bookings = Booking.objects.filter(customer=request.user)
    data = []
    for booking in bookings:
        data.append({
            'id': booking.id,
            'technician_name': f"{booking.technician.first_name} {booking.technician.last_name}",
            'technician_phone': booking.technician.phone,
            'service_type': booking.service_type,
            'address': booking.address,
            'status': booking.status,
            'total_amount': str(booking.total_amount),
            'scheduled_time': booking.scheduled_time.strftime('%Y-%m-%d %H:%M') if booking.scheduled_time else 'N/A',
            'created_at': booking.created_at.strftime('%Y-%m-%d %H:%M'),
            'payment_method': booking.payment_method
        })
    return Response(data, status=status.HTTP_200_OK)
