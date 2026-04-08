from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Dog
from .serializers import UserSerializer, DogSerializer

# ========== AUTHENTICATION VIEWS ==========

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')
        
        if not username or not password:
            return Response({'error': 'Username and password required'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, password=password, email=email)
        token = Token.objects.create(user=user)
        
        return Response({
            'success': True,
            'user_id': user.id,
            'username': user.username,
            'token': token.key
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({'error': 'Username and password required'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)
        
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'success': True,
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'token': token.key
            })
        else:
            return Response({'error': 'Invalid credentials'}, 
                           status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response({'success': True, 'message': 'Logged out'})


# ========== DOGS CRUD VIEWS ==========

class DogViewSet(ModelViewSet):
    serializer_class = DogSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Users can only see their own dogs
        return Dog.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        # Automatically assign the logged-in user as owner
        serializer.save(owner=self.request.user)