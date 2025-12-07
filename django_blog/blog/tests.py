from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post


class AuthTests(TestCase):

    def test_register_view(self):
        """Register page should load successfully."""
        response = self.client.get(reverse('blog:register'))
        self.assertEqual(response.status_code, 200)

    def test_register_and_login(self):
        """User should be able to register and automatically log in."""
        resp = self.client.post(reverse('blog:register'), {
            'username': 'tester',
            'email': 'test@example.com',
            'password1': 'complex-password-123',
            'password2': 'complex-password-123'
        }, follow=True)

        # User should be created
        self.assertTrue(User.objects.filter(username='tester').exists())

        # User should be logged in (profile page accessible)
        resp2 = self.client.get(reverse('blog:profile'))
        self.assertEqual(resp2.status_code, 200)

    def test_profile_requires_login(self):
        """Profile page should redirect anonymous users."""
        response = self.client.get(reverse('blog:profile'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertIn('/login/', response.url)


class BlogPostTests(TestCase):

    def setUp(self):
        """Create a user and a sample post."""
        self.user = User.objects.create_user(username='john', password='pass1234')
        self.post = Post.objects.create(
            title="Test Post",
            content="Content goes here",
            author=self.user
        )

    def test_post_list_view(self):
        """List page should load successfully."""
        response = self.client.get(reverse('blog:post-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")

    def test_post_detail_view(self):
        """Detail page should load successfully."""
        response = self.client.get(reverse('blog:post-detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Content goes here")

    def test_create_post_requires_login(self):
        """Anonymous users should not access post creation."""
        response = self.client.get(reverse('blog:post-create'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_author_can_create_post(self):
        """Logged-in users should create a post successfully."""
        self.client.login(username='john', password='pass1234')
        response = self.client.post(reverse('blog:post-create'), {
            'title': 'New Created Post',
            'content': 'More content'
        })

        # Redirect to detail view after successful creation
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title='New Created Post').exists())

    def test_only_author_can_edit(self):
        """Only the author should be able to edit the post."""
        # Another user
        user2 = User.objects.create_user(username='mark', password='pass456')

        self.client.login(username='mark', password='pass456')
        response = self.client.get(reverse('blog:post-edit', args=[self.post.pk]))

        # Should be forbidden (UserPassesTestMixin → 403)
        self.assertEqual(response.status_code, 403)

    def test_author_can_edit_post(self):
        """Author should be able to edit their post."""
        self.client.login(username='john', password='pass1234')
        response = self.client.post(
            reverse('blog:post-edit', args=[self.post.pk]),
            {'title': 'Updated Title', 'content': 'Updated content'}
        )

        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Updated Title")

    def test_only_author_can_delete(self):
        """Non-authors cannot delete posts."""
        user2 = User.objects.create_user(username='anna', password='pass789')

        self.client.login(username='anna', password='pass789')
        response = self.client.post(reverse('blog:post-delete', args=[self.post.pk]))

        # Should be forbidden
        self.assertEqual(response.status_code, 403)

    def test_author_can_delete(self):
        """Author can delete the post."""
        self.client.login(username='john', password='pass1234')
        response = self.client.post(reverse('blog:post-delete', args=[self.post.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())
