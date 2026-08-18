from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Service, ServiceCategory
from accounts.models import TechnicianProfile

@api_view(['GET'])
@permission_classes([AllowAny])
def get_services(request):
    category = request.GET.get('category')
    services = Service.objects.filter(is_active=True)
    
    if category:
        services = services.filter(category__name__iexact=category)
    
    data = []
    for service in services:
        data.append({
            'id': service.id,
            'title': service.title,
            'description': service.description,
            'price': str(service.price),
            'duration_minutes': service.duration_minutes,
            'category': service.category.name,
            'technician': {
                'id': service.technician.id,
                'email': service.technician.email,
                'first_name': service.technician.first_name,
                'last_name': service.technician.last_name,
                'rating': str(service.technician.technician_profile.rating) if hasattr(service.technician, 'technician_profile') else '0',
                'service_type': service.technician.technician_profile.service_type if hasattr(service.technician, 'technician_profile') else ''
            }
        })
    
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_service(request):
    if request.user.role != 'technician':
        return Response({'error': 'Only technicians can create services'}, status=status.HTTP_403_FORBIDDEN)
    
    data = request.data
    required_fields = ['title', 'description', 'price', 'category']
    for field in required_fields:
        if not data.get(field):
            return Response({'error': f'{field} is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    category, _ = ServiceCategory.objects.get_or_create(name=data['category'])
    
    service = Service.objects.create(
        technician=request.user,
        category=category,
        title=data['title'],
        description=data['description'],
        price=data['price'],
        duration_minutes=data.get('duration_minutes', 30)
    )
    
    return Response({
        'message': 'Service created successfully',
        'service': {
            'id': service.id,
            'title': service.title,
            'description': service.description,
            'price': str(service.price),
            'duration_minutes': service.duration_minutes
        }
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_categories(request):
    categories = ServiceCategory.objects.all()
    data = [{'id': c.id, 'name': c.name, 'icon': c.icon} for c in categories]
    return Response(data)
