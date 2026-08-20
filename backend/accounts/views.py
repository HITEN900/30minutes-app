import logging
import re
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, TechnicianProfile
from bookings.models import Booking
from notifications.models import Notification
from services.models import Service

logger = logging.getLogger(__name__)

def validate_password(password):
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    return True, "Password is valid."

# ============================================
# REGISTER USER - NO OTP
# ============================================
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    data = request.data
    user_type = data.get('type', 'customer')
    
    print(f"📝 Registration attempt: {data.get('email')} as {user_type}")
    
    required_fields = ['firstName', 'lastName', 'email', 'phone', 'password']
    for field in required_fields:
        if not data.get(field):
            return Response({'error': f'{field} is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        validate_email(data['email'])
    except ValidationError:
        return Response({'error': 'Invalid email format'}, status=status.HTTP_400_BAD_REQUEST)
    
    is_valid, msg = validate_password(data['password'])
    if not is_valid:
        return Response({'error': msg}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(email=data['email']).exists():
        return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(phone=data['phone']).exists():
        return Response({'error': 'Phone number already registered'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Create user - NO OTP, directly verified
        user = User.objects.create(
            username=data['email'],
            email=data['email'],
            phone=data['phone'],
            first_name=data['firstName'],
            last_name=data['lastName'],
            password=make_password(data['password']),
            role=user_type,
            is_phone_verified=True  # Directly verified, NO OTP
        )
        print(f"✅ User created: {user.email} (ID: {user.id})")
    except Exception as e:
        print(f"❌ Error creating user: {e}")
        return Response({'error': 'User creation failed. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # If technician, create technician profile
    if user_type == 'technician':
        tech_fields = ['serviceType', 'experience', 'hourlyRate', 'aadhaar']
        for field in tech_fields:
            if not data.get(field):
                user.delete()
                return Response({'error': f'{field} is required for technician'}, status=status.HTTP_400_BAD_REQUEST)
        
        if TechnicianProfile.objects.filter(aadhaar_number=data['aadhaar']).exists():
            user.delete()
            return Response({'error': 'Aadhaar number already registered'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            profile = TechnicianProfile.objects.create(
                user=user,
                aadhaar_number=data['aadhaar'],
                voter_id=data.get('voterId', ''),
                service_type=data['serviceType'],
                experience_years=int(data.get('experience', 0)),
                hourly_rate=float(data.get('hourlyRate', 0)),
                service_charge=float(data.get('serviceCharge', 0)),
                is_approved=True,
                is_available=True
            )
            print(f"✅ Technician profile created for: {user.email}")
        except Exception as e:
            print(f"❌ Error creating technician profile: {e}")
            user.delete()
            return Response({'error': 'Failed to create technician profile'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create welcome notification
        Notification.objects.create(
            user=user,
            type='system',
            title='Welcome to 30 Minutes! 🎉',
            message=f'Welcome {user.first_name}! Your professional account has been created.'
        )
    
    # Generate tokens - NO OTP REQUIRED
    refresh = RefreshToken.for_user(user)
    
    technician_data = None
    if user.role == 'technician' and hasattr(user, 'technician_profile'):
        profile = user.technician_profile
        technician_data = {
            'service_type': profile.service_type,
            'experience': profile.experience_years,
            'hourly_rate': str(profile.hourly_rate),
            'is_approved': profile.is_approved,
            'is_available': profile.is_available
        }
    
    # Return success - NO OTP MESSAGE
    return Response({
        'message': 'Registration successful!',
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh),
        'user': {
            'id': user.id,
            'email': user.email,
            'phone': user.phone,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'is_verified': user.is_phone_verified,
            'technician': technician_data
        }
    }, status=status.HTTP_201_CREATED)

# ============================================
# LOGIN
# ============================================
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    print(f"🔑 Login attempt for: {email}")
    
    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
        
        if not user.check_password(password):
            print(f"❌ Invalid password for: {email}")
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.is_active:
            return Response({'error': 'Account is disabled'}, status=status.HTTP_403_FORBIDDEN)
        
        print(f"✅ Login successful for: {email} (Role: {user.role})")
        
        refresh = RefreshToken.for_user(user)
        
        technician_data = None
        if user.role == 'technician' and hasattr(user, 'technician_profile'):
            profile = user.technician_profile
            technician_data = {
                'service_type': profile.service_type,
                'experience': profile.experience_years,
                'hourly_rate': str(profile.hourly_rate),
                'service_charge': str(profile.service_charge),
                'rating': str(profile.rating),
                'total_reviews': profile.total_reviews,
                'is_approved': profile.is_approved,
                'is_available': profile.is_available,
                'completed_bookings': profile.completed_bookings,
                'total_earnings': str(profile.total_earnings)
            }
        
        return Response({
            'message': 'Login successful',
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user': {
                'id': user.id,
                'email': user.email,
                'phone': user.phone,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
                'is_verified': user.is_phone_verified,
                'technician': technician_data
            }
        })
        
    except User.DoesNotExist:
        print(f"❌ User not found: {email}")
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# ============================================
# GET PROFILE
# ============================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    data = {
        'id': user.id,
        'email': user.email,
        'phone': user.phone,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'role': user.role,
        'is_verified': user.is_phone_verified,
        'address': user.address
    }
    
    if user.role == 'technician' and hasattr(user, 'technician_profile'):
        profile = user.technician_profile
        data['technician'] = {
            'service_type': profile.service_type,
            'experience': profile.experience_years,
            'hourly_rate': str(profile.hourly_rate),
            'rating': str(profile.rating),
            'total_reviews': profile.total_reviews,
            'completed_bookings': profile.completed_bookings,
            'total_earnings': str(profile.total_earnings),
            'is_available': profile.is_available,
            'is_approved': profile.is_approved
        }
    
    return Response(data)

# ============================================
# GET ALL SERVICES
# ============================================
@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_services(request):
    services = Service.objects.filter(is_active=True)
    data = []
    for service in services:
        technician = service.technician
        profile = technician.technician_profile if hasattr(technician, 'technician_profile') else None
        data.append({
            'id': service.id,
            'title': service.title,
            'description': service.description,
            'price': str(service.price),
            'duration_minutes': service.duration_minutes,
            'category': service.category.name if hasattr(service, 'category') else 'General',
            'technician': {
                'name': f"{technician.first_name} {technician.last_name}",
                'email': technician.email,
                'phone': technician.phone,
                'service_type': profile.service_type if profile else 'N/A',
                'rating': str(profile.rating) if profile else '0',
                'experience': profile.experience_years if profile else 0
            }
        })
    return Response(data)

# ============================================
# PROFESSIONAL DASHBOARD
# ============================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def professional_dashboard(request):
    if request.user.role != 'technician':
        return Response({'error': 'Only technicians can access this'}, status=status.HTTP_403_FORBIDDEN)
    
    user = request.user
    profile = user.technician_profile
    
    bookings = Booking.objects.filter(technician=user)
    
    total_bookings = bookings.count()
    completed = bookings.filter(status='completed').count()
    pending = bookings.filter(status='pending').count()
    accepted = bookings.filter(status='accepted').count()
    in_progress = bookings.filter(status='in_progress').count()
    cancelled = bookings.filter(status='cancelled').count()
    
    recent_bookings = bookings.order_by('-created_at')[:10]
    recent_data = []
    for booking in recent_bookings:
        recent_data.append({
            'id': booking.id,
            'customer_name': f"{booking.customer.first_name} {booking.customer.last_name}",
            'customer_phone': booking.customer.phone,
            'customer_address': booking.address,
            'service': booking.service.title if hasattr(booking, 'service') and booking.service else 'N/A',
            'status': booking.status,
            'total_amount': str(booking.total_amount),
            'scheduled_time': booking.scheduled_time.strftime('%Y-%m-%d %H:%M') if booking.scheduled_time else 'N/A',
            'created_at': booking.created_at.strftime('%Y-%m-%d %H:%M'),
            'latitude': booking.latitude,
            'longitude': booking.longitude
        })
    
    earnings_data = {
        'total_earnings': str(profile.total_earnings),
        'completed_bookings': profile.completed_bookings,
        'hourly_rate': str(profile.hourly_rate),
        'rating': str(profile.rating),
        'total_reviews': profile.total_reviews
    }
    
    unread_notifications = Notification.objects.filter(user=user, is_read=False).count()
    
    return Response({
        'statistics': {
            'total_bookings': total_bookings,
            'completed': completed,
            'pending': pending,
            'accepted': accepted,
            'in_progress': in_progress,
            'cancelled': cancelled
        },
        'recent_bookings': recent_data,
        'earnings': earnings_data,
        'profile': {
            'service_type': profile.service_type,
            'experience_years': profile.experience_years,
            'is_available': profile.is_available,
            'is_approved': profile.is_approved,
            'aadhaar': profile.aadhaar_number
        },
        'notifications': {
            'unread': unread_notifications
        }
    })
