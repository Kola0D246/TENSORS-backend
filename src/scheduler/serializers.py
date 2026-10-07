from rest_framework import serializers
from .models import TimeSlot, Infra, FacultyUnavailability, Occupancy

class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = '__all__'

class InfraSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.department_name', read_only=True)

    class Meta:
        model = Infra
        fields = '__all__'

class FacultyUnavailabilitySerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source='faculty.faculty_name', read_only=True)
    timeslot_info = serializers.StringRelatedField(source='timeslot', read_only=True)

    class Meta:
        model = FacultyUnavailability
        fields = ['id', 'faculty', 'faculty_name', 'timeslot', 'timeslot_info', 'reason', 'status', 'created_at']
        read_only_fields = ['status', 'created_at', 'faculty_name', 'timeslot_info']

class OccupancySerializer(serializers.ModelSerializer):
    room_name = serializers.StringRelatedField(source='room', read_only=True)
    faculty_name = serializers.CharField(source='faculty.faculty_name', read_only=True)
    subject_name = serializers.CharField(source='subject.subject_name', read_only=True)
    student_ids = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Occupancy
        fields = '__all__'
