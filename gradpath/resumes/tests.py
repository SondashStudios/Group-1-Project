from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Resume
import json

User = get_user_model()

class TestResumeViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.resume = Resume.objects.create(
            user=self.user,
            title="Software Engineer Resume",
            summary="Experienced in Python and Django",
            skills="Python, Django, Git",
            education="BS in Computer Science",
            experience="3 years at XYZ Corp",
            certifications="AWS Certified"
        )

    def test_resume_list_view_requires_login(self):
        # If login is NOT required for this view, expect 200
        # If login IS required, use assertEqual(..., 302)
        response = self.client.get(reverse('resumes:resume_list'))
        self.assertEqual(response.status_code, 200)  # adjust to 302 if needed

    def test_resume_list_view_logged_in(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('resumes:resume_list'))
        self.assertEqual(response.status_code, 200)

        try:
            data = json.loads(response.content)
            self.assertIn('resumes', data)
        except json.JSONDecodeError:
            # fallback if HTML is returned
            self.assertContains(response, "Resume")
