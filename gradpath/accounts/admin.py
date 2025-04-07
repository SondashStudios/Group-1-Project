from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
from resumes.models import Resume  # ✅ Import Resume from the correct app

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone_number', 'graduation_year')

    def get_fieldsets(self, request, obj=None):
        """Override default fieldsets to remove password-based authentication toggle."""
        fieldsets = super().get_fieldsets(request, obj)
        return [
            (name, {'fields': [(field for field in data['fields'] if field != 'password_based_authentication')]})
            for name, data in fieldsets
        ]
# Register the Resume model
@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'created_at', 'updated_at')
    search_fields = ('user__username', 'title')
    list_filter = ('created_at', 'updated_at')
