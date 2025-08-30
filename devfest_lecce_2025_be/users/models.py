from django.db import models


class User(models.Model):
    id = models.CharField(max_length=100, primary_key=True)

    name = models.CharField(max_length=100, blank=True, null=True)
    surname = models.CharField(max_length=100, blank=True, null=True)
    linked_in = models.CharField(max_length=100, blank=True, null=True)
    instagram = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} {self.surname} ({self.id})"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
