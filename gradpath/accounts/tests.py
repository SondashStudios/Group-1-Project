from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class AccountViewsTestCase(TestCase):

    def setUp(self):
        """Setup test user."""
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_signup_view(self):
        """Test signup page loads."""
        url = reverse('signup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Check if the page loads with status 200
        self.assertTemplateUsed(response, 'accounts/signup.html')  # Check if the correct template is used

    def test_login_view(self):
        """Test login page loads."""
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_logout_view(self):
        """Test logout redirects to login page."""
        self.client.login(username='testuser', password='testpassword')
        url = reverse('logout')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login'))  # Check if the user is redirected to the login page

    def test_welcome_view(self):
        """Test if the welcome page loads after login."""
        self.client.login(username='testuser', password='testpassword')
        url = reverse('welcome')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/welcome.html')

    def test_account_settings_view(self):
        """Test if the account settings page is accessible."""
        self.client.login(username='testuser', password='testpassword')
        url = reverse('account_settings')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account_settings.html')

   
