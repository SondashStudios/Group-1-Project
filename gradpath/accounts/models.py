from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    graduation_year = models.IntegerField(null=True, blank=True)

    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",
        blank=True
    )
# New Resume Model
class Resume(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="resumes")
    title = models.CharField(max_length=255)  # Resume title
    summary = models.TextField(blank=True, null=True)  # Short professional summary
    skills = models.TextField(blank=True, null=True)  # Comma-separated skills
    education = models.TextField(blank=True, null=True)  # Education details
    experience = models.TextField(blank=True, null=True)  # Work experience details
    certifications = models.TextField(blank=True, null=True)  # Certifications

    created_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"