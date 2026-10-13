from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

class User(AbstractUser):
    class Role(models.TextChoices):
        MANAGEMENT = 'Management', 'Management'
        HOD = 'HOD', 'HOD'
        FACULTY = 'Faculty', 'Faculty'
        STUDENT = 'Student', 'Student'

    email=models.EmailField('college email', unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)

    objects = UserManager()

    REQUIRED_FIELDS = ["email"]

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.strip().lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    # TODO: add Meta constraint: user_email_unique_lower
