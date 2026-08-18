from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Booking
from services.models import Service
from notifications.models import Notification
from django.utils import timezone

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_booking(request):
    if request.user.role != 'customer':
        return Response({'error': 'Only customers can create bookings'}, status=status.HTTP_403_FORBIDDEN)
    
    data = request.data
    required_fields = ['service_id', 'address', 'latitude', 'longitude', 'scheduled_time']
    for field in required_fields:
        if not data.get(field):
            return Response({'error': f'{field} is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        service = Service.objects.get(id=data['service_id'], is_active=True)
    except Service.DoesNotExist:
        return Response({'error': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)
    
    booking = Booking.objects.create(
        customer=request.user,
        technician=service.technician,
        service=service,
        address=data['address'],
        latitude=data['latitude'],
        longitude=data['longitude'],
        scheduled_time=data['scheduled_time'],
        total_amount=service.price
    )
    
    # Create notification for technician
    Notification.objects.create(
        user=service.technician,
        type='booking',
        title='New Booking Request',
        message=f'New booking request from {request.user.first_name} {request.user.last_name} for {service.title}'
    )
    
    return Response({
        'message': 'Booking created successfully',
        'booking': {
            'id': booking.id,
            'service': service.title,
            'technician': service.technician.email,
            'status': booking.status,
            'total_amount': str(booking.total_amount),
            'scheduled_time': booking.scheduled_time
        }
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_bookings(request):
    if request.user.role == 'customer':
        bookings = Booking.objects.filter(customer=request.user)
    elif request.user.role == 'technician':
        bookings = Booking.objects.filter(technician=request.user)
    else:
        bookings = Booking.objects.all()
    
    data = []
    for booking in bookings:
        data.append({
            'id': booking.id,
            'service': booking.service.title,
            'customer': booking.customer.email,
            'technician': booking.technician.email,
            'status': booking.status,
            'total_amount': str(booking.total_amount),
            'scheduled_time': booking.scheduled_time,
            'created_at': booking.created_at
        })
    
    return Response(data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_booking_status(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Only technician can update status
    if request.user.role != 'technician' or booking.technician != request.user:
        return Response({'error': 'Only the assigned technician can update status'}, status=status.HTTP_403_FORBIDDEN)
    
    status_value = request.data.get('status')
    if not status_value:
        return Response({'error': 'Status is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    valid_statuses = ['accepted', 'in_progress', 'completed', 'cancelled']
    if status_value not in valid_statuses:
        return Response({'error': f'Invalid status. Valid: {valid_statuses}'}, status=status.HTTP_400_BAD_REQUEST)
    
    booking.status = status_value
    if status_value == 'completed':
        booking.completed_at = timezone.now()
    
    booking.save()
    
    # Create notification for customer
    Notification.objects.create(
        user=booking.customer,
        type='booking',
        title='Booking Status Updated',
        message=f'Your booking #{booking.id} status is now {status_value}'
    )
    
    return Response({
        'message': 'Booking status updated',
        'status': booking.status
    })
