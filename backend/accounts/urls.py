from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('profile/', views.get_user_profile, name='profile'),
    path('dashboard/', views.professional_dashboard, name='professional_dashboard'),
    path('services/', views.get_all_services, name='get_all_services'),
]
