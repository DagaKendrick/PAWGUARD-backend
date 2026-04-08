from django.db import models
from django.contrib.auth.models import User

class Dog(models.Model):
    BREED_CHOICES = [
        ('LAB', 'Labrador'),
        ('GER', 'German Shepherd'),
        ('BUL', 'Bulldog'),
        ('PUD', 'Poodle'),
        ('MIX', 'Mixed'),
        ('OTH', 'Other'),
    ]
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dogs')
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=10, choices=BREED_CHOICES, default='MIX')
    age = models.IntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    color = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} (Owner: {self.owner.username})"