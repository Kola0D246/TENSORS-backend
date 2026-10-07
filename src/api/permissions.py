from rest_framework import permissions
from institutes.models import Faculty, Student

class RoleBasedAccessPermission(permissions.BasePermission):
    """
    Restricts access based on the logged-in user's role.
    """

    def has_permission(self, request, view):
        # Allow safe methods (GET, HEAD, OPTIONS) for everyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Must be authenticated for write operations
        if not request.user or not request.user.is_authenticated:
            return False
        
        role = getattr(request.user, "role", None)
        basename = getattr(view, 'basename', '')
        
        # Global role-based access (endpoint-level)
        if role == "Admin":
            return True  # full access
        
        elif role == "HOD":
            # HOD can manage department-specific resources
            return basename in ["departments", "courses", "subjects", "faculty", "students", "timeslots", "infras", "occupancies", "facultyunavailability"]
        
        elif role == "Faculty":
            # # Faculty can only modify their own FacultyUnavailability
            return basename == "facultyunavailability" and request.method in ["GET", "POST", "PUT", "PATCH"]
        
        elif role == "Student":
            # read-only access for certain models
            return request.method == "GET" and basename in ["institutes", "departments", "courses", "subjects", "occupancies"]

        return False
    
    def has_object_permission(self, request, view, obj):
        """
        Fine-grained object-level permissions:
        - Admin can read/write everything
        - HOD can read/write department resources
        - Faculty can read own department resources but only edit own pending FacultyUnavailability
        - Student can read own info and general tables
        """
        role = getattr(request.user, "role", None)
        user_faculty = getattr(request.user, "faculty_profile", None)
        user_student = getattr(request.user, "student_profile", None)

        # --- READ permissions ---
        if request.method in permissions.SAFE_METHODS:
            if role == "Admin":
                return True  # can read everything

            elif role == "HOD":
                # HOD sees department data
                if hasattr(obj, "department"):
                    return obj.department == request.user.department
                if hasattr(obj, "faculty"):
                    return obj.faculty.department == request.user.department
                if hasattr(obj, "students"):
                    return obj.students.filter(department=request.user.department).exists()
                return True  # for tables without department FK (Timeslot, Infra)

            elif role == "Faculty":
                # Faculty sees own department data, but not other faculty personal info
                if hasattr(obj, "department"):
                    return obj.department == request.user.department
                if isinstance(obj, Faculty):
                    return obj == user_faculty  # cannot see other faculty
                if hasattr(obj, "students"):
                    return obj.students.filter(department=request.user.department).exists()
                return True  # read-only for other config tables (Timeslot, Infra)

            elif role == "Student":
                # Student sees only own info or read-only general tables
                if isinstance(obj, Student):
                    return obj == user_student
                if hasattr(obj, "students"):
                    return user_student in obj.students.all()
                return True  # general tables like Timeslot, Infra, Course, Occupancy

        # --- WRITE / non-safe permissions ---
        if role == "Admin":
            return True  # full write access

        elif role == "HOD":
            # HOD can edit objects in their department
            if hasattr(obj, "department"):
                return obj.department == request.user.department
            # HOD can approve/reject FacultyUnavailability in their department
            if hasattr(obj, "faculty"):
                return obj.faculty.department == request.user.department
            # HOD can update Occupancy
            if isinstance(obj, Occupancy):
                return True
            return False

        elif role == "Faculty":
            # Faculty can only modify their own pending FacultyUnavailability
            if isinstance(obj, Faculty):
                return obj == user_faculty
            if hasattr(obj, "faculty") and obj.faculty == user_faculty:
                # Only allow edit if status is pending
                return getattr(obj, "status", None) == "pending"
            return False

        elif role == "Student":
            # Student cannot modify anything
            return False

        return False
