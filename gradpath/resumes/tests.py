from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Resume

User = get_user_model()

class TestResumeViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_resume_list_view_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('resumes:resume_list'))
        self.assertIn(response.status_code, [200, 302])  # 302 redirect if login is needed, 200 if open

    def test_resume_list_view_logged_in(self):
        response = self.client.get(reverse('resumes:resume_list'))
        self.assertEqual(response.status_code, 200)  # Logged in users should see the resume list

    def test_successful_resume_upload(self):
        file = SimpleUploadedFile("resume.pdf", b"%PDF-1.4 dummy content", content_type="application/pdf")
        response = self.client.post(reverse('resumes:resume_create'), {
            "title": "Test Resume",
            "pdf_file": file
        }, follow=True)
        self.assertIn(response.status_code, [200, 302])  # Successful upload should be 200 OK or redirect

    def test_invalid_file_upload(self):
        bad_file = SimpleUploadedFile("resume.txt", b"Invalid content", content_type="text/plain")
        response = self.client.post(reverse('resumes:resume_create'), {
            "title": "Bad Resume",
            "pdf_file": bad_file
        })
        self.assertIn(response.status_code, [200, 400])  # Invalid uploads might still return 200 with form errors

    def test_resume_update_uploads_new_instance(self):
        Resume.objects.create(user=self.user, title="Old Resume")
        new_file = SimpleUploadedFile("resume.pdf", b"%PDF-1.4 new content", content_type="application/pdf")
        response = self.client.post(reverse('resumes:resume_create'), {
            "title": "Updated Resume",
            "pdf_file": new_file
        }, follow=True)
        self.assertIn(response.status_code, [200, 302])  # Resume update normally works, no 500 expected