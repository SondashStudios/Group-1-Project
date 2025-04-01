from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResumeViewSet, ResumeCreateView  # Import ResumeCreateView

router = DefaultRouter()
router.register(r'resumes', ResumeViewSet, basename="resume")

urlpatterns = [
    path('', include(router.urls)),  # Registers all API endpoints for resumes
    path('create/', ResumeCreateView.as_view(), name='resume-create'),  
]
