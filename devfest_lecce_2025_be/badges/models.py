from django.db import models
from django.db.models.functions import Lower


class Badge(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=100)
    description = models.TextField()
    picture = models.ImageField(upload_to="badges/", null=True, blank=True)
    secret = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Badge"
        verbose_name_plural = "Badges"
        constraints = [
            models.UniqueConstraint(Lower("secret"), name="unique_badge_secret"),
        ]


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
