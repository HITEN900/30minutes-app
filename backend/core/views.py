from django.http import JsonResponse, HttpResponse

def home(request):
    return JsonResponse({
        'message': '🚀 Welcome to 30 Minutes Service Booking App!',
        'status': 'running',
        'version': '1.0.0',
        'endpoints': {
            '/': 'Home Page',
            '/api/': 'API Home',
            '/api/hello/': 'Hello World',
            '/admin/': 'Admin Panel'
        }
    })

def hello(request):
    return JsonResponse({
        'message': 'Hello from 30 Minutes App!',
        'service': 'Service Booking Platform',
        'availability': 'Technicians available within 30 minutes',
        'services': ['Plumber', 'Electrician', 'Carpenter', 'Mechanic', 'Painter', 'Cleaner']
    })
