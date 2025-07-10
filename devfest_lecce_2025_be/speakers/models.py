from django.db import models


class Speaker(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=100)
    email = models.EmailField()
    country = models.CharField(max_length=100)  # TODO: should be the country code?
    picture = models.ImageField(upload_to="speakers/", null=True, blank=True)
