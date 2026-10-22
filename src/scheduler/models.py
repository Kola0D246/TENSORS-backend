from django.db import models

class Occupancy(models.Model):
    room = models.ForeignKey("institute.Room", on_delete=models.CASCADE)
    timeslot = models.ForeignKey("institute.TimeSlot", on_delete=models.CASCADE)
    subject = models.ForeignKey("institute.Subject", on_delete=models.CASCADE)
    faculty = models.ForeignKey("institute.Faculty", on_delete=models.CASCADE)
    students = models.ManyToManyField("institute.Student")
    # need to create student groups

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['room', 'timeslot'],
                name='unique_timeslot_room'
            ),
            models.UniqueConstraint(
                fields=['faculty', 'timeslot'],
                name='unique_timeslot_faculty'
            )
        ]

# TODO: model to store multiple generated timetable