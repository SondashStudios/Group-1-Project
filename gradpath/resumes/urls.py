from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ResumeViewSet,
    ResumeCreateView,
    resume_create,
    generate_pdf,
    delete_resume,
    resume_list,
    resume_detail,
    resume_edit,
)

app_name = 'resumes'  # ✅ Required for namespacing (fixes 'not a registered namespace')

router = DefaultRouter()
router.register(r'resumes', ResumeViewSet, basename="resume")

urlpatterns = [
    # API endpoints
    path('', include(router.urls)),

    # Form-based views
    path('create/', ResumeCreateView.as_view(), name='resume_create'),
    path('create-fallback/', resume_create, name='resume_create_alt'),

    # Resume CRUD + PDF
    path('generate_pdf/<int:resume_id>/', generate_pdf, name='generate_pdf'),
    path('delete/<int:resume_id>/', delete_resume, name='delete_resume'),
    path('', resume_list, name='resume_list'),
    path('<int:resume_id>/', resume_detail, name='resume_detail'),
    path('edit/<int:resume_id>/', resume_edit, name='resume_edit'),
]
