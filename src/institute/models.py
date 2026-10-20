from django.db import models
from django.conf import settings

# ---------------------------------------------------------------------------
# Onboarding
# ---------------------------------------------------------------------------

class Institute(models.Model):
    name = models.CharField(max_length=100)
    location = models.TextField()
    affiliation = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_number = models.CharField(max_length=20)
    email_domain = models.CharField(max_length=20, unique=True)  # e.g. "satiengg.in"
 
    def __str__(self):
        return self.name

class Period(models.Model):
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    period = models.PositiveSmallIntegerField(primary_key=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(start_time__lt=models.F("end_time")),
                name="period_start_before_end"
            ),
        ]

class TimeSlot(models.Model):
    class Days(models.TextChoices):
        MON = "mon", "Monday"
        TUES = "tue", "Tuesday"
        WED = "wed", "Wednesday"
        THUS = "thu", "Thursday"
        FRI = "fri", "Friday"
        SAT = "sat", "Saturday"
        SUN = "sun", "Sunday"

    day = models.CharField(max_length=10, choices=Days.choices)
    period = models.ForeignKey(Period, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['day', 'period'],
                name='unique_day_period'
            )
        ]

    def __str__(self):
        return f"{self.day} {self.period}"

class Department(models.Model):
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    department_name = models.CharField(max_length=200)
    department_code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.department_name

class Course(models.Model):
    class CourseTypes(models.TextChoices):
        MAJOR = "major", "Major"
        MINOR = "minor", "Minor"
        OPEN_ELECTIVE = "open_elective", "Open Elective"

    course_name = models.CharField(max_length=200)
    course_type = models.CharField(max_length=20, choices=CourseTypes.choices)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    total_semester = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.department} {self.course_name}"

# ---------------------------------------------------------------------------
#  Users
# ---------------------------------------------------------------------------

class Faculty(models.Model):
    employee_id = models.CharField(max_length=20, unique=True)
    faculty_name = models.CharField(max_length=200)
    qualification = models.TextField()
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.faculty_name

class Student(models.Model):
    enrollment_no = models.CharField(max_length=20, unique=True)
    student_name = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    course = models.ManyToManyField(Course)
    semester = models.PositiveSmallIntegerField()
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    
    def __str__(self):
        return f"{self.enrollment_no} {self.student_name}"

#class StudentGroup(models.Model):
#   incomplete

# ---------------------------------------------------------------------------
# Curriculum
# ---------------------------------------------------------------------------

class Subject(models.Model):
    subject_code = models.CharField(max_length=20, unique=True)
    subject_name = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.PositiveSmallIntegerField()
    faculty = models.ManyToManyField(Faculty)
    weekly_theory_hours = models.PositiveSmallIntegerField()
    weekly_practical_hours = models.PositiveSmallIntegerField()
 
    def __str__(self):
        return f"{self.subject_code} - {self.subject_name}"

# ---------------------------------------------------------------------------
# Resources
# ---------------------------------------------------------------------------

class Building(models.Model):
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    building_name = models.CharField(max_length=200)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["institute", "building_name"], name="unique_institute_building"
            ),
        ]

    def __str__(self):
        return self.building_name

class Room(models.Model):
    class RoomTypes(models.TextChoices):
        CLASS = 'class', 'Class'
        LAB = 'lab', 'Lab'
        SMARTCLASS = 'smartclass', 'Smartclass'

    room_no = models.CharField(max_length= 200)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    departments = models.ManyToManyField(Department)
    room_type = models.CharField(max_length=20, choices=RoomTypes.choices)
    subjects = models.ManyToManyField(Subject)
    capacity = models.PositiveSmallIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["room_no", "building"], 
                name="unique_roomno_building"
            )
        ]

    def __str__(self):
        return f"{self.building} {self.room_no}"

# ---------------------------------------------------------------------------
# Availability
# ---------------------------------------------------------------------------

class FacultyUnavailability(models.Model):    
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    no_of_weeks = models.PositiveSmallIntegerField()
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.faculty} unavailable at {self.timeslot.day} {self.timeslot.period}"

class RoomUnavailability(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    no_of_weeks = models.PositiveSmallIntegerField()
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room} unavailable at {self.timeslot.day} {self.timeslot.period}"

# ---------------------------------------------------------------------------
# M:M Relationship
# ---------------------------------------------------------------------------

class FacultyDepartment(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    designation = models.CharField(max_length=20, choices=[
        ('hod', 'HOD'), ('professor', 'Professor'), ('ass_professor', 'Ass Professor')
    ])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields= ['faculty', 'department'],
                name='unique_faculty_department'
            ),
        ]