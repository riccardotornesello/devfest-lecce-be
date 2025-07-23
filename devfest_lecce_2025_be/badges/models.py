from django.db import models


class Badge(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=100)
    description = models.TextField()
    picture = models.ImageField(upload_to="badges/", null=True, blank=True)

    def __str__(self):
        return self.name


class OwnBadge(models.Model):
    id = models.AutoField(primary_key=True)

    badge = models.ForeignKey(
        Badge, on_delete=models.CASCADE, related_name="own_badges"
    )
    user_id = models.CharField(max_length=100)
    date_awarded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} - {self.badge.name}"

    class Meta:
        unique_together = ("badge", "user_id")
