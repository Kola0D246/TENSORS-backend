from django.db import models

class Period(models.Model):
    period = models.IntegerField(primary_key=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

class TimeSlot(models.Model):
    day = models.CharField(max_length=20)
    period = models.ForeignKey(Period, on_delete=models.CASCADE)

    class Meta:
        models.UniqueConstraint(
            fields=['day', 'period'],
            name='unique_day_period'
        )

    def __str__(self):
        return f"{self.day} {self.period}"

class Department(models.Model):
    department_name = models.CharField(max_length=200)
    department_short = models.CharField(max_length=10)

    def __str__(self):
        return self.department_name

class Course(models.Model):
    course_name = models.CharField(max_length=255)
    course_type = models.CharField(max_length=10, choices=[
        ('major', 'Major'), ('minor', 'Minor'), ('elective', 'Elective')
    ])
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    total_semesters = models.IntegerField()

    def __str__(self):
        return f"{self.department} {self.course_name}"

class Subject(models.Model):
    subject_code = models.CharField(max_length=20, unique=True)
    subject_name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    total_theory_hours = models.IntegerField()
    total_practical_hours = models.IntegerField()

    def __str__(self):
        return f"{self.subject_code} {self.subject_name}"

class Faculty(models.Model):
    employee_id = models.CharField(max_length=20, unique=True)
    faculty_name = models.CharField(max_length=200)
    qualification = models.CharField(max_length=1200)

    def __str__(self):
        return self.faculty_name

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

class Building(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):
    room_no = models.CharField(max_length= 200)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    departments = models.ManyToManyField(Department)
    room_type = models.CharField(max_length=20, choices=[
        ('class', 'Class'), ('lab', 'Lab'), ('smartClass', 'Smart Class')
    ])
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

class Student(models.Model):
    enrollment_no = models.CharField(max_length=50, unique=True)
    student_name = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    semester = models.IntegerField()

    def __str__(self):
        return f"{self.enrollment_no} {self.student_name}"

# Relation ship models

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
