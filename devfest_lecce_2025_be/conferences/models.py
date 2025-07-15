from django.db import models
from speakers.models import Speaker


class ConferenceTopic(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Conference Topic"
        verbose_name_plural = "Conference Topics"
        ordering = ["name"]


class ConferenceType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Conference Type"
        verbose_name_plural = "Conference Types"
        ordering = ["name"]


class Conference(models.Model):
    class Language(models.TextChoices):
        ENGLISH = "EN", "English"
        ITALIAN = "IT", "Italian"

    class Level(models.TextChoices):
        BEGINNER = "BEGINNER", "Beginner"
        INTERMEDIATE = "INTERMEDIATE", "Intermediate"
        ADVANCED = "ADVANCED", "Advanced"

    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=100)
    note = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to="conferences/", null=True, blank=True)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    speaker = models.ForeignKey(
        Speaker, on_delete=models.CASCADE, related_name="conferences"
    )

    topic = models.ForeignKey(
        ConferenceTopic, on_delete=models.PROTECT, related_name="conferences"
    )
    typology = models.ForeignKey(
        ConferenceType, on_delete=models.PROTECT, related_name="conferences"
    )

    level = models.CharField(
        max_length=20,
        choices=Level.choices,
        default=Level.BEGINNER,
    )
    language = models.CharField(
        max_length=2,
        choices=Language.choices,
        default=Language.ENGLISH,
    )

    def __str__(self):
        return f"{self.name} ({self.start_time.strftime('%Y-%m-%d %H:%M')})"

    class Meta:
        verbose_name = "Conference"
        verbose_name_plural = "Conferences"
        ordering = ["name"]
