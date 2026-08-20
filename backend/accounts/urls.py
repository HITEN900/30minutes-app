
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('register/', views.register_user, name='register'),
#     path('login/', views.login_user, name='login'),
#     path('profile/', views.get_user_profile, name='profile'),
#     path('dashboard/', views.professional_dashboard, name='professional_dashboard'),
#     path('services/', views.get_all_services, name='get_all_services'),
#     path('professionals/', views.get_all_professionals, name='get_all_professionals'),
#     path('professionals/by-service/', views.get_professionals_by_service, name='get_professionals_by_service'),
# ]
# # "@ | Out-File -FilePath "accounts\urls.py" -Encoding UTF8

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('register/', views.register_user, name='register'),
#     path('login/', views.login_user, name='login'),
#     path('profile/', views.get_user_profile, name='profile'),
#     path('dashboard/', views.professional_dashboard, name='professional_dashboard'),
#     path('services/', views.get_all_services, name='get_all_services'),
#     path('professionals/', views.get_all_professionals, name='get_all_professionals'),
#     path('professionals/by-service/', views.get_professionals_by_service, name='get_professionals_by_service'),
#     path('create-booking/', views.create_booking, name='create_booking'),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('profile/', views.get_user_profile, name='profile'),
    path('dashboard/', views.professional_dashboard, name='professional_dashboard'),
    path('services/', views.get_all_services, name='get_all_services'),
    path('professionals/', views.get_all_professionals, name='get_all_professionals'),
    path('professionals/by-service/', views.get_professionals_by_service, name='get_professionals_by_service'),
    path('create-booking/', views.create_booking, name='create_booking'),
]
# "@ | Out-File -FilePath "accounts\urls.py" -Encoding UTF8