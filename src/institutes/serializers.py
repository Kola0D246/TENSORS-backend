from rest_framework import serializers
from .models import Department, Course, Subject, Faculty, Student

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'department_name']

class CourseSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.department_name', read_only=True)

    class Meta:
        model = Course
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.course_name', read_only=True)

    class Meta:
        model = Subject
        fields = '__all__'


class FacultySerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.department_name', read_only=True)
    primary_subjects = serializers.StringRelatedField(many=True, read_only=True)
    secondary_subjects = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Faculty
        fields = '__all__'
        read_only_fields = ['faculty_name', 'primary_subjects', 'secondary_subjects']


class StudentSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.department_name', read_only=True)
    majors = serializers.StringRelatedField(many=True, read_only=True)
    minors = serializers.StringRelatedField(many=True, read_only=True)
    electives = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ['enrollment_no', 'majors', 'minors', 'electives']