

# # # from django.shortcuts import render
# # # from rest_framework import status
# # # from rest_framework.decorators import api_view, permission_classes
# # # from rest_framework.permissions import IsAuthenticated
# # # from rest_framework.response import Response
# # # from django.contrib.auth import get_user_model
# # # from .models import Booking
# # # from accounts.models import TechnicianProfile
# # # from notifications.models import Notification

# # # User = get_user_model()

# # # # ============================================
# # # # GET ALL BOOKINGS FOR TECHNICIAN
# # # # ============================================
# # # @api_view(['GET'])
# # # @permission_classes([IsAuthenticated])
# # # def get_technician_bookings(request):
# # #     if request.user.role != 'technician':
# # #         return Response({'error': 'Only technicians can access this'}, status=status.HTTP_403_FORBIDDEN)
    
# # #     bookings = Booking.objects.filter(technician=request.user)
# # #     data = []
# # #     for booking in bookings:
# # #         data.append({
# # #             'id': booking.id,
# # #             'customer_name': f"{booking.customer.first_name} {booking.customer.last_name}",
# # #             'customer_phone': booking.customer.phone,
# # #             'customer_address': booking.address,
# # #             'service_type': booking.service_type,
# # #             'status': booking.status,
# # #             'total_amount': str(booking.total_amount),
# # #             'scheduled_time': booking.scheduled_time.strftime('%Y-%m-%d %H:%M') if booking.scheduled_time else 'N/A',
# # #             'created_at': booking.created_at.strftime('%Y-%m-%d %H:%M'),
# # #             'payment_method': booking.payment_method
# # #         })
# # #     return Response(data, status=status.HTTP_200_OK)

# # # # ============================================
# # # # GET ALL BOOKINGS FOR CUSTOMER
# # # # ============================================
# # # @api_view(['GET'])
# # # @permission_classes([IsAuthenticated])
# # # def get_customer_bookings(request):
# # #     if request.user.role != 'customer':
# # #         return Response({'error': 'Only customers can access this'}, status=status.HTTP_403_FORBIDDEN)
    
# # #     bookings = Booking.objects.filter(customer=request.user)
# # #     data = []
# # #     for booking in bookings:
# # #         data.append({
# # #             'id': booking.id,
# # #             'technician_name': f"{booking.technician.first_name} {booking.technician.last_name}",
# # #             'technician_phone': booking.technician.phone,
# # #             'service_type': booking.service_type,
# # #             'address': booking.address,
# # #             'status': booking.status,
# # #             'total_amount': str(booking.total_amount),
# # #             'scheduled_time': booking.scheduled_time.strftime('%Y-%m-%d %H:%M') if booking.scheduled_time else 'N/A',
# # #             'created_at': booking.created_at.strftime('%Y-%m-%d %H:%M'),
# # #             'payment_method': booking.payment_method,
# # #             'can_cancel': booking.status == 'pending'
# # #         })
# # #     return Response(data, status=status.HTTP_200_OK)

# # # # ============================================
# # # # UPDATE BOOKING STATUS - FIXED
# # # # Allows both technicians AND customers to update
# # # # ============================================
# # # @api_view(['PUT'])
# # # @permission_classes([IsAuthenticated])
# # # def update_booking_status(request, booking_id):
# # #     try:
# # #         booking = Booking.objects.get(id=booking_id)
# # #     except Booking.DoesNotExist:
# # #         return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
    
# # #     status_value = request.data.get('status')
# # #     if not status_value:
# # #         return Response({'error': 'Status is required'}, status=status.HTTP_400_BAD_REQUEST)
    
# # #     valid_statuses = ['accepted', 'in_progress', 'completed', 'cancelled', 'rejected']
# # #     if status_value not in valid_statuses:
# # #         return Response({'error': f'Invalid status. Valid: {valid_statuses}'}, status=status.HTTP_400_BAD_REQUEST)
    
# # #     user = request.user
# # #     is_technician = user.role == 'technician' and booking.technician == user
# # #     is_customer = user.role == 'customer' and booking.customer == user
    
# # #     # Check permissions
# # #     if status_value == 'cancelled':
# # #         # Allow customer to cancel their own pending bookings
# # #         if is_customer and booking.status == 'pending':
# # #             booking.status = status_value
# # #             booking.save()
# # #             # Notify technician
# # #             Notification.objects.create(
# # #                 user=booking.technician,
# # #                 type='booking',
# # #                 title='Booking Cancelled',
# # #                 message=f'Booking #{booking.id} has been cancelled by the customer.'
# # #             )
# # #             return Response({'message': 'Booking cancelled successfully', 'status': booking.status}, status=status.HTTP_200_OK)
# # #         elif is_technician:
# # #             booking.status = status_value
# # #             booking.save()
# # #             # Notify customer
# # #             Notification.objects.create(
# # #                 user=booking.customer,
# # #                 type='booking',
# # #                 title='Booking Cancelled',
# # #                 message=f'Your booking #{booking.id} has been cancelled.'
# # #             )
# # #             return Response({'message': 'Booking cancelled successfully', 'status': booking.status}, status=status.HTTP_200_OK)
# # #         else:
# # #             return Response({'error': 'You are not authorized to cancel this booking'}, status=status.HTTP_403_FORBIDDEN)
    
# # #     # For other statuses (accepted, in_progress, completed, rejected) - only technicians can update
# # #     if not is_technician:
# # #         return Response({'error': 'Only technicians can update booking status'}, status=status.HTTP_403_FORBIDDEN)
    
# # #     # Technician can update any status except cancelled (handled above)
# # #     booking.status = status_value
# # #     booking.save()
    
# # #     # Notify customer
# # #     Notification.objects.create(
# # #         user=booking.customer,
# # #         type='booking',
# # #         title='Booking Status Updated',
# # #         message=f'Your booking #{booking.id} status is now {status_value}'
# # #     )
    
# # #     return Response({
# # #         'message': 'Booking status updated',
# # #         'status': booking.status
# # #     }, status=status.HTTP_200_OK)

# # import logging
# # import re
# # from django.contrib.auth import authenticate
# # from django.contrib.auth.hashers import make_password
# # from django.core.validators import validate_email
# # from django.core.exceptions import ValidationError
# # from django.db import IntegrityError
# # from rest_framework import status
# # from rest_framework.decorators import api_view, permission_classes
# # from rest_framework.permissions import AllowAny, IsAuthenticated
# # from rest_framework.response import Response
# # from rest_framework_simplejwt.tokens import RefreshToken
# # from .models import User, TechnicianProfile
# # from bookings.models import Booking
# # from notifications.models import Notification
# # from services.models import Service

# # logger = logging.getLogger(__name__)

# # def validate_password(password):
# #     if len(password) < 6:
# #         return False, "Password must be at least 6 characters long."
# #     return True, "Password is valid."

# # # ============================================
# # # REGISTER USER
# # # ============================================
# # @api_view(['POST'])
# # @permission_classes([AllowAny])
# # def register_user(request):
# #     data = request.data
# #     user_type = data.get('type', 'customer')
    
# #     print(f"📝 Registration attempt: {data.get('email')} as {user_type}")
    
# #     required_fields = ['firstName', 'lastName', 'email', 'phone', 'password']
# #     for field in required_fields:
# #         if not data.get(field):
# #             return Response({'error': f'{field} is required'}, status=status.HTTP_400_BAD_REQUEST)
    
# #     try:
# #         validate_email(data['email'])
# #     except ValidationError:
# #         return Response({'error': 'Invalid email format'}, status=status.HTTP_400_BAD_REQUEST)
    
# #     is_valid, msg = validate_password(data['password'])
# #     if not is_valid:
# #         return Response({'error': msg}, status=status.HTTP_400_BAD_REQUEST)
    
# #     if User.objects.filter(email=data['email']).exists():
# #         return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)
    
# #     if User.objects.filter(phone=data['phone']).exists():
# #         return Response({'error': 'Phone number already registered'}, status=status.HTTP_400_BAD_REQUEST)
    
# #     try:
# #         user = User.objects.create(
# #             username=data['email'],
# #             email=data['email'],
# #             phone=data['phone'],
# #             first_name=data['firstName'],
# #             last_name=data['lastName'],
# #             password=make_password(data['password']),
# #             role=user_type,
# #             is_phone_verified=True
# #         )
# #         print(f"✅ User created: {user.email} (ID: {user.id})")
# #     except Exception as e:
# #         print(f"❌ Error creating user: {e}")
# #         return Response({'error': 'User creation failed. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
    
# #     if user_type == 'technician':
# #         tech_fields = ['serviceType', 'experience', 'hourlyRate', 'aadhaar']
# #         for field in tech_fields:
# #             if not data.get(field):
# #                 user.delete()
# #                 return Response({'error': f'{field} is required for technician'}, status=status.HTTP_400_BAD_REQUEST)
        
# #         if TechnicianProfile.objects.filter(aadhaar_number=data['aadhaar']).exists():
# #             user.delete()
# #             return Response({'error': 'Aadhaar number already registered'}, status=status.HTTP_400_BAD_REQUEST)
        
# #         try:
# #             profile = TechnicianProfile.objects.create(
# #                 user=user,
# #                 aadhaar_number=data['aadhaar'],
# #                 voter_id=data.get('voterId', ''),
# #                 service_type=data['serviceType'],
# #                 experience_years=int(data.get('experience', 0)),
# #                 hourly_rate=float(data.get('hourlyRate', 0)),
# #                 service_charge=float(data.get('serviceCharge', 0)),
# #                 is_approved=True,
# #                 is_available=True
# #             )
# #             print(f"✅ Technician profile created for: {user.email}")
# #         except Exception as e:
# #             print(f"❌ Error creating technician profile: {e}")
# #             user.delete()
# #             return Response({'error': 'Failed to create technician profile'}, status=status.HTTP_400_BAD_REQUEST)
        
# #         Notification.objects.create(
# #             user=user,
# #             type='system',
# #             title='Welcome to 30 Minutes! 🎉',
# #             message=f'Welcome {user.first_name}! Your professional account has been created.'
# #         )
    
# #     refresh = RefreshToken.for_user(user)
    
# #     technician_data = None
# #     if user.role == 'technician' and hasattr(user, 'technician_profile'):
# #         profile = user.technician_profile
# #         technician_data = {
# #             'service_type': profile.service_type,
# #             'experience': profile.experience_years,
# #             'hourly_rate': str(profile.hourly_rate),
# #             'is_approved': profile.is_approved,
# #             'is_available': profile.is_available
# #         }
    
# #     return Response({
# #         'message': 'Registration successful!',
# #         'access_token': str(refresh.access_token),
# #         'refresh_token': str(refresh),
# #         'user': {
# #             'id': user.id,
# #             'email': user.email,
# #             'phone': user.phone,
# #             'first_name': user.first_name,
# #             'last_name': user.last_name,
# #             'role': user.role,
# #             'is_verified': user.is_phone_verified,
# #             'technician': technician_data
# #         }
# #     }, status=status.HTTP_201_CREATED)

# # # ============================================
# # # LOGIN
# # # ============================================
# # @api_view(['POST'])
# # @permission_classes([AllowAny])
# # def login_user(request):
# #     email = request.data.get('email')
# #     password = request.data.get('password')
    
# #     print(f"🔑 Login attempt for: {email}")
    
# #     if not email or not password:
# #         return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    
# #     try:
# #         user = User.objects.get(email=email)
        
# #         if not user.check_password(password):
# #             print(f"❌ Invalid password for: {email}")
# #             return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
# #         if not user.is_active:
# #             return Response({'error': 'Account is disabled'}, status=status.HTTP_403_FORBIDDEN)
        
# #         print(f"✅ Login successful for: {email} (Role: {user.role})")
        
# #         refresh = RefreshToken.for_user(user)
        
# #         technician_data = None
# #         if user.role == 'technician' and hasattr(user, 'technician_profile'):
# #             profile = user.technician_profile
# #             technician_data = {
# #                 'service_type': profile.service_type,
# #                 'experience': profile.experience_years,
# #                 'hourly_rate': str(profile.hourly_rate),
# #                 'service_charge': str(profile.service_charge),
# #                 'rating': str(profile.rating),
# #                 'total_reviews': profile.total_reviews,
# #                 'is_approved': profile.is_approved,
# #                 'is_available': profile.is_available,
# #                 'completed_bookings': profile.completed_bookings,
# #                 'total_earnings': str(profile.total_earnings)
# #             }
        
# #         return Response({
# #             'message': 'Login successful',
# #             'access_token': str(refresh.access_token),
# #             'refresh_token': str(refresh),
# #             'user': {
# #                 'id': user.id,
# #                 'email': user.email,
# #                 'phone': user.phone,
# #                 'first_name': user.first_name,
# #                 'last_name': user.last_name,
# #                 'role': user.role,
# #                 'is_verified': user.is_phone_verified,
# #                 'technician': technician_data
# #             }
# #         })
        
# #     except User.DoesNotExist:
# #         print(f"❌ User not found: {email}")
# #         return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# # # ============================================
# # # CREATE BOOKING
# # # ============================================
# # @api_view(['POST'])
# # @permission_classes([IsAuthenticated])
# # def create_booking(request):
# #     try:
# #         print("📝 Creating booking...")
# #         print(f"👤 User: {request.user.email} (Role: {request.user.role})")
        
# #         if request.user.role != 'customer':
# #             return Response({'error': 'Only customers can create bookings'}, status=status.HTTP_403_FORBIDDEN)
        
# #         data = request.data
# #         print(f"📋 Data received: {data}")
        
# #         required_fields = ['technician_id', 'service_type', 'address', 'datetime', 'price', 'payment_method']
# #         for field in required_fields:
# #             if not data.get(field):
# #                 return Response({'error': f'{field} is required'}, status=status.HTTP_400_BAD_REQUEST)
        
# #         try:
# #             technician = User.objects.get(id=data['technician_id'], role='technician')
# #             print(f"✅ Technician found: {technician.email}")
# #         except User.DoesNotExist:
# #             print(f"❌ Technician not found with ID: {data['technician_id']}")
# #             return Response({'error': 'Technician not found'}, status=status.HTTP_404_NOT_FOUND)
        
# #         # Generate 4-digit OTP
# #         import random
# #         otp = random.randint(1000, 9999)
        
# #         # Create booking
# #         booking = Booking.objects.create(
# #             customer=request.user,
# #             technician=technician,
# #             service_type=data['service_type'],
# #             description=data.get('description', 'Service booking'),
# #             address=data['address'],
# #             latitude=data.get('latitude', 0),
# #             longitude=data.get('longitude', 0),
# #             scheduled_time=data['datetime'],
# #             total_amount=data['price'],
# #             payment_method=data['payment_method'],
# #             status='pending'
# #         )
# #         print(f"✅ Booking created: {booking.id} with OTP: {otp}")
        
# #         # Create notification for technician
# #         Notification.objects.create(
# #             user=technician,
# #             type='booking',
# #             title='New Booking Request! 📋',
# #             message=f'New booking request from {request.user.first_name} {request.user.last_name} for {data["service_type"]}.'
# #         )
# #         print(f"✅ Notification sent to technician")
        
# #         return Response({
# #             'message': 'Booking created successfully',
# #             'booking_id': booking.id,
# #             'status': booking.status,
# #             'otp': otp
# #         }, status=status.HTTP_201_CREATED)
        
# #     except Exception as e:
# #         print(f"❌ Error creating booking: {e}")
# #         import traceback
# #         traceback.print_exc()
# #         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# # # ============================================
# # # GET ALL PROFESSIONALS
# # # ============================================
# # @api_view(['GET'])
# # @permission_classes([AllowAny])
# # def get_all_professionals(request):
# #     try:
# #         technicians = TechnicianProfile.objects.filter(is_approved=True)
# #         data = []
# #         for tech in technicians:
# #             data.append({
# #                 'id': tech.id,
# #                 'user_id': tech.user.id,
# #                 'name': f"{tech.user.first_name} {tech.user.last_name}",
# #                 'email': tech.user.email,
# #                 'phone': tech.user.phone,
# #                 'service_type': tech.service_type,
# #                 'experience': tech.experience_years,
# #                 'hourly_rate': str(tech.hourly_rate),
# #                 'rating': str(tech.rating),
# #                 'total_reviews': tech.total_reviews,
# #                 'is_available': tech.is_available,
# #                 'latitude': tech.current_lat,
# #                 'longitude': tech.current_lng
# #             })
# #         return Response(data, status=status.HTTP_200_OK)
# #     except Exception as e:
# #         print(f"❌ Error fetching professionals: {e}")
# #         return Response({'error': 'Failed to fetch professionals'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# # # ============================================
# # # GET USER PROFILE
# # # ============================================
# # @api_view(['GET'])
# # @permission_classes([IsAuthenticated])
# # def get_user_profile(request):
# #     user = request.user
# #     data = {
# #         'id': user.id,
# #         'email': user.email,
# #         'phone': user.phone,
# #         'first_name': user.first_name,
# #         'last_name': user.last_name,
# #         'role': user.role,
# #         'is_verified': user.is_phone_verified,
# #         'address': user.address
# #     }
    
# #     if user.role == 'technician' and hasattr(user, 'technician_profile'):
# #         profile = user.technician_profile
# #         data['technician'] = {
# #             'service_type': profile.service_type,
# #             'experience': profile.experience_years,
# #             'hourly_rate': str(profile.hourly_rate),
# #             'rating': str(profile.rating),
# #             'total_reviews': profile.total_reviews,
# #             'completed_bookings': profile.completed_bookings,
# #             'total_earnings': str(profile.total_earnings),
# #             'is_available': profile.is_available,
# #             'is_approved': profile.is_approved
# #         }
    
# #     return Response(data)

# # # ============================================
# # # PROFESSIONAL DASHBOARD
# # # ============================================
# # @api_view(['GET'])
# # @permission_classes([IsAuthenticated])
# # def professional_dashboard(request):
# #     if request.user.role != 'technician':
# #         return Response({'error': 'Only technicians can access this'}, status=status.HTTP_403_FORBIDDEN)
    
# #     user = request.user
# #     profile = user.technician_profile
    
# #     bookings = Booking.objects.filter(technician=user)
    
# #     total_bookings = bookings.count()
# #     completed = bookings.filter(status='completed').count()
# #     pending = bookings.filter(status='pending').count()
# #     accepted = bookings.filter(status='accepted').count()
# #     in_progress = bookings.filter(status='in_progress').count()
# #     cancelled = bookings.filter(status='cancelled').count()
    
# #     recent_bookings = bookings.order_by('-created_at')[:10]
# #     recent_data = []
# #     for booking in recent_bookings:
# #         recent_data.append({
# #             'id': booking.id,
# #             'customer_name': f"{booking.customer.first_name} {booking.customer.last_name}",
# #             'customer_phone': booking.customer.phone,
# #             'customer_address': booking.address,
# #             'service': booking.service_type,
# #             'status': booking.status,
# #             'total_amount': str(booking.total_amount),
# #             'scheduled_time': booking.scheduled_time.strftime('%Y-%m-%d %H:%M') if booking.scheduled_time else 'N/A',
# #             'created_at': booking.created_at.strftime('%Y-%m-%d %H:%M'),
# #             'latitude': booking.latitude,
# #             'longitude': booking.longitude,
# #             'payment_method': booking.payment_method
# #         })
    
# #     earnings_data = {
# #         'total_earnings': str(profile.total_earnings),
# #         'completed_bookings': profile.completed_bookings,
# #         'hourly_rate': str(profile.hourly_rate),
# #         'rating': str(profile.rating),
# #         'total_reviews': profile.total_reviews
# #     }
    
# #     unread_notifications = Notification.objects.filter(user=user, is_read=False).count()
    
# #     return Response({
# #         'statistics': {
# #             'total_bookings': total_bookings,
# #             'completed': completed,
# #             'pending': pending,
# #             'accepted': accepted,
# #             'in_progress': in_progress,
# #             'cancelled': cancelled
# #         },
# #         'recent_bookings': recent_data,
# #         'earnings': earnings_data,
# #         'profile': {
# #             'service_type': profile.service_type,
# #             'experience_years': profile.experience_years,
# #             'is_available': profile.is_available,
# #             'is_approved': profile.is_approved,
# #             'aadhaar': profile.aadhaar_number
# #         },
# #         'notifications': {
# #             'unread': unread_notifications
# #         }
# #     })

# # from django.shortcuts import render
# # from rest_framework import status
# # from rest_framework.decorators import api_view, permission_classes
# # from rest_framework.permissions import IsAuthenticated
# # from rest_framework.response import Response
# # from django.contrib.auth import get_user_model
# # from .models import Booking
# # from accounts.models import TechnicianProfile
# # from notifications.models import Notification

# # User = get_user_model()

# # # ============================================
# # # GET ALL BOOKINGS FOR TECHNICIAN
# # # ============================================
# # @api_view(['GET'])
# # @permission_classes([IsAuthenticated])
# # def get_technician_bookings(request):
# #     if request.user.role != 'technician':
# #         return Response({'error': 'Only technicians can access this'}, status=status.HTTP_403_FORBIDDEN)
    
# #     bookings = Booking.objects.filter(technician=request.user)
# #     data = []
# #     for booking in bookings:
# #         data.append({
# #             'id': booking.id,
# #             'customer_name': f"{booking.customer.first_name} {booking.customer.last_name}",
# #             'customer_phone': booking.customer.phone,
# #             'customer_address': booking.address,
# #             'service_type': booking.service_type,
# #             'status': booking.status,
# #             'total_amount': str(booking.total_amount),
# #             'scheduled_time': booking.scheduled_time.strftime('%Y-%m-%d %H:%M') if booking.scheduled_time else 'N/A',
# #             'created_at': booking.created_at.strftime('%Y-%m-%d %H:%M'),
# #             'payment_method': booking.payment_method
# #         })
# #     return Response(data, status=status.HTTP_200_OK)

# # # ============================================
# # # GET ALL BOOKINGS FOR CUSTOMER
# # # ============================================
# # @api_view(['GET'])
# # @permission_classes([IsAuthenticated])
# # def get_customer_bookings(request):
# #     if request.user.role != 'customer':
# #         return Response({'error': 'Only customers can access this'}, status=status.HTTP_403_FORBIDDEN)
    
# #     bookings = Booking.objects.filter(customer=request.user)
# #     data = []
# #     for booking in bookings:
# #         data.append({
# #             'id': booking.id,
# #             'technician_name': f"{booking.technician.first_name} {booking.technician.last_name}",
# #             'technician_phone': booking.technician.phone,
# #             'service_type': booking.service_type,
# #             'address': booking.address,
# #             'status': booking.status,
# #             'total_amount': str(booking.total_amount),
# #             'scheduled_time': booking.scheduled_time.strftime('%Y-%m-%d %H:%M') if booking.scheduled_time else 'N/A',
# #             'created_at': booking.created_at.strftime('%Y-%m-%d %H:%M'),
# #             'payment_method': booking.payment_method,
# #             'can_cancel': booking.status == 'pending'
# #         })
# #     return Response(data, status=status.HTTP_200_OK)

# # # ============================================
# # # UPDATE BOOKING STATUS - FIXED
# # # Allows both technicians AND customers to update
# # # ============================================
# # @api_view(['PUT'])
# # @permission_classes([IsAuthenticated])
# # def update_booking_status(request, booking_id):
# #     try:
# #         booking = Booking.objects.get(id=booking_id)
# #     except Booking.DoesNotExist:
# #         return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
    
# #     status_value = request.data.get('status')
# #     if not status_value:
# #         return Response({'error': 'Status is required'}, status=status.HTTP_400_BAD_REQUEST)
    
# #     valid_statuses = ['accepted', 'in_progress', 'completed', 'cancelled', 'rejected']
# #     if status_value not in valid_statuses:
# #         return Response({'error': f'Invalid status. Valid: {valid_statuses}'}, status=status.HTTP_400_BAD_REQUEST)
    
# #     user = request.user
# #     is_technician = user.role == 'technician' and booking.technician == user
# #     is_customer = user.role == 'customer' and booking.customer == user
    
# #     # Check permissions
# #     if status_value == 'cancelled':
# #         # Allow customer to cancel their own pending bookings
# #         if is_customer and booking.status == 'pending':
# #             booking.status = status_value
# #             booking.save()
# #             # Notify technician
# #             Notification.objects.create(
# #                 user=booking.technician,
# #                 type='booking',
# #                 title='Booking Cancelled',
# #                 message=f'Booking #{booking.id} has been cancelled by the customer.'
# #             )
# #             return Response({'message': 'Booking cancelled successfully', 'status': booking.status}, status=status.HTTP_200_OK)
# #         elif is_technician:
# #             booking.status = status_value
# #             booking.save()
# #             # Notify customer
# #             Notification.objects.create(
# #                 user=booking.customer,
# #                 type='booking',
# #                 title='Booking Cancelled',
# #                 message=f'Your booking #{booking.id} has been cancelled.'
# #             )
# #             return Response({'message': 'Booking cancelled successfully', 'status': booking.status}, status=status.HTTP_200_OK)
# #         else:
# #             return Response({'error': 'You are not authorized to cancel this booking'}, status=status.HTTP_403_FORBIDDEN)
    
# #     # For other statuses (accepted, in_progress, completed, rejected) - only technicians can update
# #     if not is_technician:
# #         return Response({'error': 'Only technicians can update booking status'}, status=status.HTTP_403_FORBIDDEN)
    
# #     # Technician can update any status except cancelled (handled above)
# #     booking.status = status_value
# #     booking.save()
    
# #     # Notify customer
# #     Notification.objects.create(
# #         user=booking.customer,
# #         type='booking',
# #         title='Booking Status Updated',
# #         message=f'Your booking #{booking.id} status is now {status_value}'
# #     )
    
# #     return Response({
# #         'message': 'Booking status updated',
# #         'status': booking.status
# #     }, status=status.HTTP_200_OK)













# from django.shortcuts import render
# from rest_framework import status
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from django.contrib.auth import get_user_model
# from .models import Booking
# from accounts.models import TechnicianProfile
# from notifications.models import Notification

# User = get_user_model()

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_technician_bookings(request):
#     if request.user.role != 'technician':
#         return Response({'error': 'Only technicians can access this'}, status=status.HTTP_403_FORBIDDEN)
    
#     bookings = Booking.objects.filter(technician=request.user)
#     data = []
#     for booking in bookings:
#         data.append({
#             'id': booking.id,
#             'customer_name': f"{booking.customer.first_name} {booking.customer.last_name}",
#             'customer_phone': booking.customer.phone,
#             'customer_address': booking.address,
#             'service_type': booking.service_type,
#             'status': booking.status,
#             'total_amount': str(booking.total_amount),
#             'scheduled_time': booking.scheduled_time.strftime('%Y-%m-%d %H:%M') if booking.scheduled_time else 'N/A',
#             'created_at': booking.created_at.strftime('%Y-%m-%d %H:%M'),
#             'payment_method': booking.payment_method
#         })
#     return Response(data, status=status.HTTP_200_OK)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_customer_bookings(request):
#     if request.user.role != 'customer':
#         return Response({'error': 'Only customers can access this'}, status=status.HTTP_403_FORBIDDEN)
    
#     bookings = Booking.objects.filter(customer=request.user)
#     data = []
#     for booking in bookings:
#         data.append({
#             'id': booking.id,
#             'technician_name': f"{booking.technician.first_name} {booking.technician.last_name}",
#             'technician_phone': booking.technician.phone,
#             'service_type': booking.service_type,
#             'address': booking.address,
#             'status': booking.status,
#             'total_amount': str(booking.total_amount),
#             'scheduled_time': booking.scheduled_time.strftime('%Y-%m-%d %H:%M') if booking.scheduled_time else 'N/A',
#             'created_at': booking.created_at.strftime('%Y-%m-%d %H:%M'),
#             'payment_method': booking.payment_method
#         })
#     return Response(data, status=status.HTTP_200_OK)

# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def update_booking_status(request, booking_id):
#     try:
#         booking = Booking.objects.get(id=booking_id)
#     except Booking.DoesNotExist:
#         return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
    
#     status_value = request.data.get('status')
#     if not status_value:
#         return Response({'error': 'Status is required'}, status=status.HTTP_400_BAD_REQUEST)
    
#     valid_statuses = ['accepted', 'in_progress', 'completed', 'cancelled', 'rejected']
#     if status_value not in valid_statuses:
#         return Response({'error': f'Invalid status. Valid: {valid_statuses}'}, status=status.HTTP_400_BAD_REQUEST)
    
#     user = request.user
#     is_technician = user.role == 'technician' and booking.technician == user
    
#     # Only technicians can update status (except customer cancellation)
#     if not is_technician:
#         return Response({'error': 'Only technicians can update booking status'}, status=status.HTTP_403_FORBIDDEN)
    
#     booking.status = status_value
#     booking.save()
    
#     # Notify customer
#     Notification.objects.create(
#         user=booking.customer,
#         type='booking',
#         title='Booking Status Updated',
#         message=f'Your booking #{booking.id} status is now {status_value}'
#     )
    
#     return Response({
#         'message': f'Booking status updated to {status_value}',
#         'status': booking.status
#     }, status=status.HTTP_200_OK)




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
            'payment_method': booking.payment_method,
            'can_cancel': booking.status == 'pending'
        })
    return Response(data, status=status.HTTP_200_OK)

# ============================================
# UPDATE BOOKING STATUS - FIXED
# Allows both technicians AND customers to update
# ============================================
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_booking_status(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
    
    status_value = request.data.get('status')
    if not status_value:
        return Response({'error': 'Status is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    valid_statuses = ['accepted', 'in_progress', 'completed', 'cancelled', 'rejected']
    if status_value not in valid_statuses:
        return Response({'error': f'Invalid status. Valid: {valid_statuses}'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    is_technician = user.role == 'technician' and booking.technician == user
    is_customer = user.role == 'customer' and booking.customer == user
    
    # Check permissions
    if status_value == 'cancelled':
        # Allow customer to cancel their own pending bookings
        if is_customer and booking.status == 'pending':
            booking.status = status_value
            booking.save()
            # Notify technician
            Notification.objects.create(
                user=booking.technician,
                type='booking',
                title='Booking Cancelled',
                message=f'Booking #{booking.id} has been cancelled by the customer.'
            )
            return Response({'message': 'Booking cancelled successfully', 'status': booking.status}, status=status.HTTP_200_OK)
        elif is_technician:
            booking.status = status_value
            booking.save()
            # Notify customer
            Notification.objects.create(
                user=booking.customer,
                type='booking',
                title='Booking Cancelled',
                message=f'Your booking #{booking.id} has been cancelled.'
            )
            return Response({'message': 'Booking cancelled successfully', 'status': booking.status}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You are not authorized to cancel this booking'}, status=status.HTTP_403_FORBIDDEN)
    
    # For other statuses (accepted, in_progress, completed, rejected) - only technicians can update
    if not is_technician:
        return Response({'error': 'Only technicians can update booking status'}, status=status.HTTP_403_FORBIDDEN)
    
    # Technician can update any status except cancelled (handled above)
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
