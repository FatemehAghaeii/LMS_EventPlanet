from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # تعریف نقش‌ها
    class Role(models.TextChoices):
        ORGANIZER = 'ORGANIZER', 'Organizer / Teacher'
        PARTICIPANT = 'PARTICIPANT', 'Participant / Student'
    
    role = models.CharField(
        max_length=20, 
        choices=Role.choices, 
        default=Role.PARTICIPANT
    )
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"