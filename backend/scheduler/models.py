from django.db import models
from institutes.models import TimeSlot, Room, Faculty, Subject, Student

class TimeSlot(models.Model):
    day = models.CharField(max_length=20)
    period = models.ForeignKey(Periods, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.day} {self.period}"

class FacultyUnavailability(models.Model):    
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    reason = models.CharField(max_length=1200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.faculty} unavailable at {self.timeslot.day} {self.timeslot.period}"

class Occupancy(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)
    status = models.CharField(max_length=20, choices=[('available', 'Available'), ('booked', 'Booked'), ('blocked', 'Blocked')])

    class Meta:
        unique_together = ('room', 'timeslot')