from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment


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

        # User created
        self.assertTrue(User.objects.filter(username='tester').exists())

        # Auto-login works
        resp2 = self.client.get(reverse('blog:profile'))
        self.assertEqual(resp2.status_code, 200)

    def test_profile_requires_login(self):
        """Profile page should redirect to login."""
        response = self.client.get(reverse('blog:profile'))
        self.assertEqual(response.status_code, 302)
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
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")

    def test_post_detail_view(self):
        response = self.client.get(reverse('blog:post_detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Content goes here")

    def test_create_post_requires_login(self):
        response = self.client.get(reverse('blog:post_create'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_author_can_create_post(self):
        self.client.login(username='john', password='pass1234')
        response = self.client.post(reverse('blog:post_create'), {
            'title': 'New Created Post',
            'content': 'More content'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title='New Created Post').exists())

    def test_only_author_can_edit(self):
        user2 = User.objects.create_user(username='mark', password='pass456')

        self.client.login(username='mark', password='pass456')
        response = self.client.get(reverse('blog:post_update', args=[self.post.pk]))

        self.assertEqual(response.status_code, 403)

    def test_author_can_edit_post(self):
        self.client.login(username='john', password='pass1234')

        response = self.client.post(
            reverse('blog:post_update', args=[self.post.pk]),
            {'title': 'Updated Title', 'content': 'Updated content'}
        )

        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Updated Title")

    def test_only_author_can_delete(self):
        user2 = User.objects.create_user(username='anna', password='pass789')
        self.client.login(username='anna', password='pass789')

        response = self.client.post(reverse('blog:post_delete', args=[self.post.pk]))
        self.assertEqual(response.status_code, 403)

    def test_author_can_delete(self):
        self.client.login(username='john', password='pass1234')
        response = self.client.post(reverse('blog:post_delete', args=[self.post.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())


# ------------------------------------------------------------
# COMMENT TESTS
# ------------------------------------------------------------

class CommentTests(TestCase):

    def setUp(self):
        """Create users and a post."""
        self.user = User.objects.create_user(username="john", password="pass1234")
        self.user2 = User.objects.create_user(username="mark", password="pass5678")

        self.post = Post.objects.create(
            title="A Post",
            content="Hello world",
            author=self.user
        )

        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content="First comment!"
        )

    def test_comment_create_requires_login(self):
        """Guests cannot post comments."""
        url = reverse("blog:comment_create", args=[self.post.pk])
        response = self.client.post(url, {"content": "test"})
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_user_can_create_comment(self):
        """Logged-in users can comment."""
        self.client.login(username="john", password="pass1234")

        url = reverse("blog:comment_create", args=[self.post.pk])
        response = self.client.post(url, {"content": "New comment"}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Comment.objects.filter(content="New comment").exists())

    def test_only_author_can_edit_comment(self):
        """Non-authors cannot edit comments."""
        self.client.login(username="mark", password="pass5678")

        url = reverse("blog:comment_update", args=[self.comment.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 403)

    def test_author_can_edit_comment(self):
        """Authors can update their comments."""
        self.client.login(username="john", password="pass1234")

        url = reverse("blog:comment_update", args=[self.comment.pk])
        response = self.client.post(url, {"content": "Updated!"})

        self.assertEqual(response.status_code, 302)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, "Updated!")

    def test_only_author_can_delete_comment(self):
        """Non-authors cannot delete comments."""
        self.client.login(username="mark", password="pass5678")

        url = reverse("blog:comment_delete", args=[self.comment.pk])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 403)

    def test_author_can_delete_comment(self):
        """Comment authors can delete."""
        self.client.login(username="john", password="pass1234")

        url = reverse("blog:comment_delete", args=[self.comment.pk])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())
