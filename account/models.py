from django.db import models

from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [
        ('USER', 'User'),
        ('OWNER', 'Owner'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_owner(self):
        return self.role == 'OWNER'

    def __str__(self):
        return f"{self.user.username} ({self.role})"
