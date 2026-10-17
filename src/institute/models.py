from django.db import models
from django.conf import settings
from django.db.models import Q #a class used to encapsulate and build complex database queries using SQL logical operators like OR, AND, and NOT

class Period(models.Model):
    period = models.IntegerField(primary_key=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

class TimeSlot(models.Model):
    class Days(models.IntegerChoices):
        MON = 0, "Monday"
        TUES = 1, "Tuesday"
        WED = 2, "Wednesday"
        THUS = 3, "Thursday"
        FRI = 4, "Friday"
        SAT = 5, "Saturday"
        SUN = 6, "Sunday"

    day = models.IntegerField(choices=Days.choices)
    period = models.ForeignKey(Period, on_delete=models.CASCADE)

    class Meta:
        models.UniqueConstraint(
            fields=['day', 'period'],
            name='unique_day_period'
        )

    def __str__(self):
        return f"{self.day} {self.period}"

# ---------------------------------------------------------------------------
# Onboarding hierarchy
# ---------------------------------------------------------------------------

class Institute(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    affiliations = models.TextField(blank=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True)
    email_domain = models.CharField(max_length=100, unique=True)  # e.g. "satiengg.in"
    created_at = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return self.name

class Department(models.Model):
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, related_name="departments")
    department_name = models.CharField(max_length=200)
    department_short = models.CharField(max_length=10)
    code = models.CharField(max_length=10, null=True)
 
    class Meta:
        unique_together = ("institute", "code")

    def __str__(self):
        return self.department_name

class Course(models.Model):
    class CourseTypes(models.TextChoices):
        MAJOR = 'major', 'Major'
        MINOR = 'minor', 'Minor'
        ELECTIVE = 'elective', 'Elective'

    course_name = models.CharField(max_length=255)
    course_type = models.CharField(max_length=10, choices=CourseTypes.choices)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    total_semesters = models.IntegerField()

    def __str__(self):
        return f"{self.department} {self.course_name}"

# ---------------------------------------------------------------------------
# People (nullable link to the login account)
# ---------------------------------------------------------------------------

class Faculty(models.Model):
    employee_id = models.CharField(max_length=20, unique=True)
    faculty_name = models.CharField(max_length=200)
    qualification = models.CharField(max_length=1200)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="faculty_profile",)

    def __str__(self):
        return self.faculty_name

class Student(models.Model):
    enrollment_no = models.CharField(max_length=50, unique=True)
    student_name = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    course = models.ManyToManyField(Course)
    semester = models.IntegerField()
    user = models.OneToOneField(
            settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
            null=True, blank=True, related_name="student_profile",
        )
    
    def __str__(self):
        return f"{self.enrollment_no} {self.student_name}"

# ---------------------------------------------------------------------------
# Curriculum
# ---------------------------------------------------------------------------

class Subject(models.Model):
    class Category(models.TextChoices):
        CORE = "CORE", "Core (major)"
        OPEN_ELECTIVE = "OE", "Open elective"
        MINOR = "MINOR", "Minor"
 
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="subjects")
    subject_code = models.CharField(max_length=20, unique=True)
    subject_name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    total_theory_hours = models.IntegerField()
    total_practical_hours = models.IntegerField()
    semester = models.PositiveSmallIntegerField(null=True, blank=True)
    credits = models.PositiveSmallIntegerField(default=3)
    weekly_periods = models.PositiveSmallIntegerField(default=3)
    is_lab = models.BooleanField(default=False)
    consecutive_periods = models.PositiveSmallIntegerField(default=1)   # labs: 2-3
    # required_room_type = models.CharField(max_length=10, choices=RoomType.choices, default=RoomType.LECTURE)
    # required_lab_type = models.CharField(max_length=50, blank=True)
    #minor_program = models.ForeignKey(MinorProgram, null=True, blank=True, on_delete=models.SET_NULL, related_name="subjects")
 
    class Meta:
        unique_together = ("department", "subject_code")
 
    def __str__(self):
        return f"{self.subject_code} - {self.subject_name}"

# ---------------------------------------------------------------------------
# Resources
# ---------------------------------------------------------------------------

class Building(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class RoomTypes(models.TextChoices):
        CLASS = 'class', 'Class'
        LAB = 'lab', 'Lab'
        SMARTCLASS = 'smartclass', 'Smartclass'

class Room(models.Model):
    room_no = models.CharField(max_length= 200)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    departments = models.ManyToManyField(Department)
    room_type = models.CharField(max_length=20, choices=RoomTypes.choices)
    lab_type = models.CharField(max_length=50, blank=True)  # "Computer", "Electronics"
    subjects = models.ManyToManyField(Subject)
    capacity = models.IntegerField()
    availability = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.building} {self.room_no}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["room_no", "building"], 
                name="unique_roomno_building"
            )
        ]


# ---------------------------------------------------------------------------
# Availability (hard-constraint inputs)
# ---------------------------------------------------------------------------

class FacultyUnavailability(models.Model):    
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields= ['faculty', 'timeslot'],
                name='unique_faculty_timeslot'
            ),
        ]

    def __str__(self):
        return f"{self.faculty} unavailable at {self.timeslot.day} {self.timeslot.period}"

class RoomUnavailability(models.Model):
    """Recurring blocked slot (maintenance, reserved)."""
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="blocked_slots")
    #term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE)
    day_of_week = models.PositiveSmallIntegerField()
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    reason = models.CharField(max_length=150, blank=True)
 
    class Meta:
        unique_together = ("room", "day_of_week", "period")



# M:M Relation models

class FacultyDepartment(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    designation = models.CharField(max_length=20, choices=[
        ('HOD', 'HOD'), ('Professor', 'Professor'), ('Ass Professor', 'Ass Professor')
    ])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields= ['faculty', 'department'],
                name='unique_faculty_department'
            ),
        ]

#class StudentBatch(models.Model):
#   course = models.ForeignKey(Course, on_delete=models.CASCADE)
#   semester = models.IntegerField()
#   #incomplete