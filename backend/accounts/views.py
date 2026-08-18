from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
import random
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, OTP, TechnicianProfile
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def generate_otp():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    data = request.data
    user_type = data.get('type', 'customer')
    
    # Validate required fields
    required_fields = ['firstName', 'lastName', 'email', 'phone', 'password']
    for field in required_fields:
        if not data.get(field):
            return Response({'error': f'{field} is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Validate email
    try:
        validate_email(data['email'])
    except ValidationError:
        return Response({'error': 'Invalid email format'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if email exists
    if User.objects.filter(email=data['email']).exists():
        return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if phone exists
    if User.objects.filter(phone=data['phone']).exists():
        return Response({'error': 'Phone number already registered'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Create user
    user = User.objects.create_user(
        username=data['email'],
        email=data['email'],
        phone=data['phone'],
        first_name=data['firstName'],
        last_name=data['lastName'],
        password=data['password'],
        role=user_type
    )
    
    # If technician, create technician profile
    if user_type == 'technician':
        # Validate technician fields
        tech_fields = ['serviceType', 'experience', 'hourlyRate', 'aadhaar', 'voterId']
        for field in tech_fields:
            if not data.get(field):
                return Response({'error': f'{field} is required for technician'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if Aadhaar exists
        if TechnicianProfile.objects.filter(aadhaar_number=data['aadhaar']).exists():
            return Response({'error': 'Aadhaar number already registered'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if Voter ID exists
        if TechnicianProfile.objects.filter(voter_id=data['voterId']).exists():
            return Response({'error': 'Voter ID already registered'}, status=status.HTTP_400_BAD_REQUEST)
        
        TechnicianProfile.objects.create(
            user=user,
            aadhaar_number=data['aadhaar'],
            voter_id=data['voterId'],
            service_type=data['serviceType'],
            experience_years=data.get('experience', 0),
            hourly_rate=data.get('hourlyRate', 0),
            service_charge=data.get('serviceCharge', 0),
            is_approved=True  # Auto-approve for demo
        )
    
    # Send OTP
    otp_code = generate_otp()
    OTP.objects.create(
        user=user,
        phone=data['phone'],
        otp_code=otp_code,
        expires_at=timezone.now() + timedelta(minutes=5)
    )
    
    # In production, send SMS via Twilio
    print(f'📱 OTP for {data["phone"]}: {otp_code}')
    
    return Response({
        'message': 'User registered successfully. Please verify OTP.',
        'user_id': user.id,
        'phone': data['phone']
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    phone = request.data.get('phone')
    otp_code = request.data.get('otp')
    
    if not phone or not otp_code:
        return Response({'error': 'Phone and OTP are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        otp = OTP.objects.filter(phone=phone, otp_code=otp_code, is_used=False).latest('created_at')
    except OTP.DoesNotExist:
        return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not otp.is_valid():
        return Response({'error': 'OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Mark OTP as used
    otp.is_used = True
    otp.save()
    
    # Verify user
    user = otp.user
    user.is_phone_verified = True
    user.save()
    
    # Generate tokens
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'message': 'OTP verified successfully',
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh),
        'user': {
            'id': user.id,
            'email': user.email,
            'phone': user.phone,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'is_verified': user.is_phone_verified
        }
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    email = request.data.get('email')
    phone = request.data.get('phone')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Authenticate
    user = authenticate(username=email, password=password)
    
    if not user:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    if not user.is_phone_verified:
        return Response({'error': 'Please verify your phone number first'}, status=status.HTTP_403_FORBIDDEN)
    
    # Generate tokens
    refresh = RefreshToken.for_user(user)
    
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
            'is_verified': user.is_phone_verified
        }
    })

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
        'address': user.address,
        'profile_picture': user.profile_picture.url if user.profile_picture else None
    }
    
    if user.role == 'technician' and hasattr(user, 'technician_profile'):
        profile = user.technician_profile
        data['technician'] = {
            'service_type': profile.service_type,
            'experience': profile.experience_years,
            'hourly_rate': str(profile.hourly_rate),
            'service_charge': str(profile.service_charge),
            'rating': str(profile.rating),
            'total_reviews': profile.total_reviews,
            'is_available': profile.is_available,
            'is_approved': profile.is_approved
        }
    
    return Response(data)
