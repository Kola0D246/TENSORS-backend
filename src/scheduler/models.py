from django.db import models
from institute.models import TimeSlot, Room, Faculty, Subject, Student

class Occupancy(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)

    class Meta:
        models.UniqueConstraint(
            fields=['room', 'timeslot']
            name='unique_timeslot_room'
        )
