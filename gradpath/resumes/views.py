from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Resume
from .serializers import ResumeSerializer

# 🔹 API View for Resume CRUD
class ResumeViewSet(viewsets.ModelViewSet):
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]  # Requires authentication

    def get_queryset(self):
        """ Ensures users can only see their own resumes. """
        return Resume.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """ Automatically assigns the logged-in user when creating a resume. """
        serializer.save(user=self.request.user)

# 🔹 Resume Creation Page (for signed-up users)
class ResumeCreateView(LoginRequiredMixin, CreateView):
    model = Resume
    fields = ['title', 'summary', 'skills', 'education', 'experience', 'certifications']
    template_name = 'resumes/resume_form.html'
    success_url = '/api/v1/resumes/'  # Redirect to resumes API after saving

    def form_valid(self, form):
        form.instance.user = self.request.user  # Assign the logged-in user
        return super().form_valid(form)
