from django.db import models


class ContactLead(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    service = models.CharField(max_length=150, blank=True)
    message = models.TextField()
    source = models.CharField(max_length=50, default="website")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.email}"
