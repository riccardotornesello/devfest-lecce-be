from django.db import models


class ConferencesTrack(models.Model):
    name = models.CharField()
    description = models.TextField(blank=True, null=True)


class Conference(models.Model):
    name = models.CharField()
    description = models.TextField(blank=True, null=True)

    track = models.ForeignKey(
        ConferencesTrack,
        on_delete=models.CASCADE,
        related_name="conferences",
    )
