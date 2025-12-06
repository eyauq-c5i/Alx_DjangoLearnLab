from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthTests(TestCase):
    def test_register_view(self):
        response = self.client.get(reverse('blog:register'))
        self.assertEqual(response.status_code, 200)

    def test_register_and_login(self):
        # Register
        resp = self.client.post(reverse('blog:register'), {
            'username': 'tester',
            'email': 'test@example.com',
            'password1': 'complex-password-123',
            'password2': 'complex-password-123'
        }, follow=True)
        self.assertTrue(User.objects.filter(username='tester').exists())

        # Now try login (client is already logged in by auth_login in register view)
        resp2 = self.client.get(reverse('blog:profile'))
        self.assertEqual(resp2.status_code, 200)
