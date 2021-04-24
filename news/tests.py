from django.test import TestCase
from django.urls import reverse

from .models import Article, Issue


class NewsModelTests(TestCase):
    def setUp(self) -> None:
        """Create a article and an issue."""
        Article.objects.create(title='Test title')
        Issue.objects.create(description='test description', issue_num=1)

    def test_article_str_method(self) -> None:
        """Test the article string representation method."""
        article = Article.objects.get(title='Test title')
        article_str = str(article)
        self.assertEqual(article_str, 'Test title')

    def test_issue_str(self) -> None:
        """Test the issue string representation method."""
        issue = Issue.objects.get(description='test description')
        issue_str = str(issue)
        self.assertEqual(issue_str, 'test description')


class NewsIndexViewTests(TestCase):
    def test_index_page_content(self):
        """Test the content on the home page."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A simple news app')


class NewsListViewTests(TestCase):
    def test_list_articles(self):
        response = self.client.get(reverse('news:articles'))
        self.assertEqual(response.status_code, 200)
