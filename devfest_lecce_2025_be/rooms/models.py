from django.db import models


class Room(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=100)
    building = models.CharField(max_length=100)
    picture = models.ImageField(upload_to="rooms/", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"
