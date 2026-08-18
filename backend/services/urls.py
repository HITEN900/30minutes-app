from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_services, name='get_services'),
    path('create/', views.create_service, name='create_service'),
    path('categories/', views.get_categories, name='get_categories'),
]
