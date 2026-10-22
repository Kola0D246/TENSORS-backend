from rest_framework import serializers
from .models import *

class InstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institute
        fields = '__all__'

class PeriodSerializer(serializers.ModelSerializer):
    institute = InstituteSerializer(read_only=True)
    
    class Meta:
        model = Period
        field = '__all__'

class TimeSlotSerializer(serializers.ModelSerializer):
    period = PeriodSerializer(read_only=True)

    def validate_time(self, value):
        pass
        # TODO: validate start_time < end_time

    class Meta:
        model = TimeSlot
        field = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    institute = InstituteSerializer(read_only=True)

    class Meta:
        model = Department
        field = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    department_name = DepartmentSerializer(read_only=True)
    
    class Meta:
        model = Institute
        fields = '__all__'