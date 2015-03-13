import datetime

from django.contrib.auth.models import User
from django.test import Client, TestCase

from bulletin.models import Issue, Newsletter, Section, Post
from bulletin.views import (get_most_recently_published_issue,
                    get_news_from_most_recent_issue)


class TopLevelTests(TestCase):

    def setUp(self):
        password = 'password'
        self.user = User.objects.create_superuser('user',
                                                  'user@user.com',
                                                  password)

        self.NEWSLETTER_NAME = 'Joanie Does Not Even Like ChaChi'
        self.newsletter = Newsletter(name=self.NEWSLETTER_NAME)
        self.newsletter.save()

        self.client = Client()
        self.client.login(username=self.user.username,
                          password=password)

    def test_get_most_recently_published_issue_none_published(self):
        """Does get_most_..._issue return None if no Issues are published?
        """
        self.assertIsNone(get_most_recently_published_issue())

    def test_get_most_recently_published_issue(self):
        """Does get_most_..._issue return the right Issue?
        """
        far_future = Issue.objects.create(
            newsletter=self.newsletter,
            pub_date=datetime.date(2560, 1, 1))
        most_recent = Issue.objects.create(
            newsletter=self.newsletter,
            pub_date=datetime.date(2015, 1, 1))
        first = Issue.objects.create(
            newsletter=self.newsletter,
            pub_date=datetime.date(2010, 1, 1))

        self.assertEqual(get_most_recently_published_issue().id,
                         most_recent.id)

    def test_get_news_from_most_recent_issue(self):
        """Does get_news_from_most_recent_issue work?
        """
        issue = Issue.objects.create(
            newsletter=self.newsletter,
            pub_date=datetime.date(2001, 1, 1))
        news_section = Section.objects.create(issue=issue,
                                              name="News")
        comics_section = Section.objects.create(issue=issue,
                                                name="Comics")
        issue.sections.add(news_section, comics_section)
        news_post = Post.objects.create(section=news_section,
                                        title='Important!',
                                        submitter=self.user)
        comics_post = Post.objects.create(section=comics_section,
                                          title='Ha!',
                                          submitter=self.user)

        most_recent_news = get_news_from_most_recent_issue()
        self.assertIn(news_post, most_recent_news)
        self.assertNotIn(comics_post, most_recent_news)
