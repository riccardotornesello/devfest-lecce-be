from django.db import models


class Badge(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=100)
    description = models.TextField()
    picture = models.ImageField(upload_to="badges/", null=True, blank=True)
