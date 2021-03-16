from django.db import models
from django.urls import reverse


class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    capacity = models.PositiveIntegerField(default=0)
    projector = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('room:room_details', args=[self.pk])


class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    comment = models.TextField(blank=True)

    class Meta:
        unique_together = ('room', 'date',)
