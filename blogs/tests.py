from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Blog, Category


class SearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        author = User.objects.create(username='writer')
        category = Category.objects.create(category_name='Technology')
        for index, field in enumerate(('title', 'short_description', 'blog_body')):
            values = {'title': 'Example', 'short_description': '', 'blog_body': ''}
            values[field] = 'Django tips'
            Blog.objects.create(
                **values, slug=f'post-{index}', author=author,
                category=category, status='Published',
            )
        Blog.objects.create(
            title='Django draft', slug='draft', author=author, category=category,
            status='Draft',
        )

    def test_search_matches_all_text_fields_and_excludes_drafts(self):
        response = self.client.get(reverse('search'), {'q': '  DJANGO  '})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['posts']), 3)
        self.assertNotContains(response, 'Django draft')
        self.assertContains(response, reverse('blogs', args=['post-0']))

    def test_blank_search_prompts_for_term(self):
        for query in ('', '   '):
            response = self.client.get(reverse('search'), {'q': query})
            self.assertContains(response, 'Enter a search term')
            self.assertEqual(len(response.context['posts']), 0)

    def test_no_results(self):
        response = self.client.get(reverse('search'), {'q': 'unmatched'})
        self.assertContains(response, 'No posts found.')
