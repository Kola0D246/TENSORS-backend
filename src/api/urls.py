from django.urls import path, include
from rest_framework.routers import DefaultRouter
from institutes.views import DepartmentViewSet, CourseViewSet, SubjectViewSet, FacultyViewSet, StudentViewSet
from scheduler.views import TimeSlotViewSet, InfraViewSet, FacultyUnavailabilityViewSet, OccupancyViewSet
from users.views import UserViewSet

router = DefaultRouter()
# institute app
router.register(r'departments', DepartmentViewSet, basename='departments')
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'subjects', SubjectViewSet, basename='subjects')
router.register(r'faculty', FacultyViewSet, basename='faculty')
router.register(r'students', StudentViewSet, basename='students')

# scheduler app
router.register(r'timeslots', TimeSlotViewSet, basename='timeslots')
router.register(r'infras', InfraViewSet, basename='infras')
router.register(r'facultyunavailability', FacultyUnavailabilityViewSet, basename='facultyunavailability')
router.register(r'occupancies', OccupancyViewSet, basename='occupancies')

# Users
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]
