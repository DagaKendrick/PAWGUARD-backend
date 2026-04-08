from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, LogoutView, DogViewSet

# Router for DogViewSet
router = DefaultRouter()
router.register(r'dogs', DogViewSet, basename='dog')

urlpatterns = [
    # Auth endpoints
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    
    # Dog endpoints (includes /dogs/, /dogs/{id}/, etc.)
    path('', include(router.urls)),
]