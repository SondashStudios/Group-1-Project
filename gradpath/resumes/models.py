from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # This gets your CustomUser model

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="resumes")
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
