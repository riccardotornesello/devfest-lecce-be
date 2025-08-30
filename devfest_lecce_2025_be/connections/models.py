from django.db import models
from users.models import User


class Connection(models.Model):
    id = models.AutoField(primary_key=True)

    user_from = models.ForeignKey(
        User, related_name="connections_from", on_delete=models.CASCADE
    )
    user_to = models.ForeignKey(
        User, related_name="connections_to", on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Connection from {self.user_from} to {self.user_to}"

    class Meta:
        verbose_name = "Connection"
        verbose_name_plural = "Connections"
        unique_together = ("user_from", "user_to")
