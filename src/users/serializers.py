from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.department_name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'institute', 'institute_name', 'department', 'department_name']
