from django.contrib.auth.models import UserManager as DjangoUserManager

class UserManager(DjangoUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = email.strip().lower()
        return super()._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("role", self.model.Role.MANAGEMENT)
        return super().create_superuser(username, email, password, **extra_fields)