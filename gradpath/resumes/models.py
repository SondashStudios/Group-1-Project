from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.http import HttpResponse

User = get_user_model()  # This gets your CustomUser model

# Helper function to validate file size (Max 5MB)
def validate_pdf_size(value):
    max_size = 5 * 1024 * 1024  # 5MB limit
    if value.size > max_size:
        raise ValidationError("The uploaded file is too large (max 5MB).")

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="resumes")

    title = models.CharField(max_length=255, blank=True, null=True)  # Title is optional
    summary = models.TextField(blank=True, null=True)  # Short professional summary
    skills = models.TextField(blank=True, null=True)  # Skills list
    education = models.TextField(blank=True, null=True)  # Education details
    experience = models.TextField(blank=True, null=True)  # Work experience
    certifications = models.TextField(blank=True, null=True)  # Certifications

    

    # PDF Upload Field with Validation (Only PDFs, Max 5MB)
    pdf_file = models.FileField(
        upload_to='resumes/', 
        null=True, 
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf']),  # Only allow PDFs
            validate_pdf_size  # Enforce 5MB size limit
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Auto update timestamp

    def __str__(self):
        return f"{self.user.username} - {self.title or 'Untitled Resume'}"

    