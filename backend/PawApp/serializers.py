from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Dog

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# Dog Serializer
class DogSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.username', read_only=True)
    
    class Meta:
        model = Dog
        fields = ['id', 'name', 'breed', 'age', 'weight', 'color', 'owner_name', 'created_at']
        read_only_fields = ['id', 'created_at']