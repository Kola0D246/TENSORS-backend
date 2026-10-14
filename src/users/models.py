from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('Management', 'Management'),
        ('HOD', 'HOD'),
        ('Faculty', 'Faculty'),
        ('Student', 'Student')
    ]
<<<<<<< HEAD:src/users/models.py
=======
    username = models.CharField(primary_key=True, max_length=200)
>>>>>>> 04a85fb48950a1c902548b48f7c61e224aed22bd:backend/users/models.py
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username}"