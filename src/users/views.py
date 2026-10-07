from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from api.permissions import RoleBasedAccessPermission
from institutes.models import Faculty, Student

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [RoleBasedAccessPermission]

    def get_queryset(self):
        user = self.request.user
          
        if user.role == 'Admin':
            # Admin can see all users
            return User.objects.filter(institute=user.institute)
        elif user.role == 'HOD':
            # HOD sees department-level;
            return User.objects.filter(department=user.department)
        elif user.role == 'Faculty':
            # Faculty sees self
            return User.objects.filter(id=user.id)
        elif user.role == 'Student':
            # Student sees only self
            return User.objects.filter(id=user.id)

        # Default fallback
        return User.objects.none()