from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from blogs.models import Blog, Category


class DashboardTests(TestCase):
    def test_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('dashboard'))

    def test_overview_shows_only_current_users_articles(self):
        author = User.objects.create_user(username='writer')
        other = User.objects.create_user(username='other')
        category = Category.objects.create(category_name='Technology')
        for owner, status, slug in (
            (author, 'Published', 'published-story'),
            (author, 'Draft', 'draft-story'),
            (other, 'Draft', 'private-story'),
        ):
            Blog.objects.create(author=owner, category=category, status=status,
                                slug=slug, title=slug)
        self.client.force_login(author)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_posts'], 2)
        self.assertEqual(response.context['published_posts'], 1)
        self.assertEqual(response.context['draft_posts'], 1)
        self.assertContains(response, 'draft-story')
        self.assertNotContains(response, 'private-story')
        self.assertContains(response, reverse('blogs', args=['published-story']))
        self.assertNotContains(response, reverse('blogs', args=['draft-story']))

    def test_new_account_sees_empty_state(self):
        self.client.force_login(User.objects.create_user(username='new-writer'))
        response = self.client.get(reverse('dashboard'))
        self.assertContains(response, 'Your story starts here')
        self.assertEqual(response.context['total_posts'], 0)
