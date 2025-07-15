from django.db import models


class Speaker(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=100)
    email = models.EmailField()
    country = models.CharField(max_length=100)
    picture = models.ImageField(upload_to="speakers/", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Speaker"
        verbose_name_plural = "Speakers"
        ordering = ["name"]
