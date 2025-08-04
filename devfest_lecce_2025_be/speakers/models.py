from django.db import models


class Speaker(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    picture = models.ImageField(upload_to="speakers/", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Speaker"
        verbose_name_plural = "Speakers"
        ordering = ["name"]
