from django.db import models
from django.contrib.auth.models import User

# Persona choices
PERSONA_CHOICES = [
    ('FARMER', 'Farmer'),
    ('BODABODA', 'BodaBoda Rider'),
    ('SMALL_SHOP', 'Small Shop Owner'),
    ('STUDENT', 'Student Freelancer'),
]

class UserProfile(models.Model):
    # Link to Django's built-in user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Extra fields
    phone_number = models.CharField(max_length=15, unique=True)
    persona = models.CharField(max_length=20, choices=PERSONA_CHOICES)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.persona}"
