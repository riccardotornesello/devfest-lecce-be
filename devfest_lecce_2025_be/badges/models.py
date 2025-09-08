from django.db import models
from django.db.models.functions import Lower


class Badge(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=100)
    description = models.TextField()
    picture = models.ImageField(upload_to="badges/", null=True, blank=True)
    points = models.IntegerField(default=0)

    category = models.ForeignKey(
        "BadgeCategory", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.name} ({self.points} points)"

    class Meta:
        verbose_name = "Badge"
        verbose_name_plural = "Badges"
        ordering = ["name"]


class BadgeCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Badge Category"
        verbose_name_plural = "Badge Categories"
        ordering = ["name"]


class OwnBadge(models.Model):
    id = models.AutoField(primary_key=True)

    badge = models.ForeignKey(
        Badge, on_delete=models.CASCADE, related_name="own_badges"
    )
    user_id = models.CharField(max_length=100)

    awarded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} - {self.badge.name}"

    class Meta:
        unique_together = ("badge", "user_id")


class BadgeCode(models.Model):
    id = models.AutoField(primary_key=True)
    badges = models.ManyToManyField(Badge, related_name="badge_codes")
    code = models.CharField(max_length=100, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code}"

    class Meta:
        verbose_name = "Badge Code"
        verbose_name_plural = "Badge Codes"
        constraints = [
            models.UniqueConstraint(Lower("code"), name="unique_badge_code"),
        ]


class BadgeCodeLog(models.Model):
    id = models.AutoField(primary_key=True)
    badge_code = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)
    used_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} used {self.badge_code} at {self.used_at}"

    class Meta:
        verbose_name = "Badge Code Log"
        verbose_name_plural = "Badge Code Logs"
        ordering = ["-used_at"]
