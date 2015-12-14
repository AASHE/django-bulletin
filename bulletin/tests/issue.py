import datetime

from bs4 import BeautifulSoup
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from bulletin.models import Issue, IssueTemplate, Newsletter, Section, Post


class IssueTests(TestCase):

    def setUp(self):
        password = 'password'
        self.user = User.objects.create_superuser('user',
                                                  'user@user.com',
                                                  password)
        self.newsletter = Newsletter(name='Test Newsletter')
        self.newsletter.save()
        self.client = Client()
        self.client.login(username=self.user.username,
                          password=password)

    def test_get_most_recently_published_issue_none_published(self):
        """Does get_most_..._issue return None if no Issues are published?
        """
        self.assertIsNone(Issue.get_most_recently_published_issue())

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

        self.assertEqual(Issue.get_most_recently_published_issue().id,
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

        most_recent_news = Issue.get_news_from_most_recent_issue()
        self.assertIn(news_post, most_recent_news)
        self.assertNotIn(comics_post, most_recent_news)

    def test_create_an_issue(self):
        """Can we create an issue?
        """
        url = reverse('bulletin:issue-create',
                      kwargs={'pk': self.newsletter.id})
        response = self.client.get(url,
                                   follow=True)
        self.assertEqual(response.status_code, 200)

        initial_num_newsletter_issues = self.newsletter.issues.count()
        url = reverse('bulletin:issue-create',
                      kwargs={'pk': self.newsletter.id})
        response = self.client.post(url,
                                    data={'pub_date': '2014-10-04',
                                          'name': 'Excellent issue'},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.newsletter.issues.count(),
                         initial_num_newsletter_issues + 1)

    def test_issue_update(self):
        """Can we pull up the issue update page?
        """
        issue = Issue.objects.create(newsletter=self.newsletter,
                                     pub_date=datetime.date.today())
        response = self.client.get(reverse('bulletin:issue-update',
                                           kwargs={'pk': issue.id}),
                                   follow=True)
        # Did the editor come up?
        self.assertEqual(response.status_code, 200)

    def test_render_to_html(self):
        """Does render_to_html work?
        """
        issue = Issue.objects.create(newsletter=self.newsletter,
                                     pub_date=datetime.date.today())
        html = issue.render_to_html(
            html_template_name='bulletin/api/test/html_template.html')

        soup = BeautifulSoup(html)
        self.assertTrue(soup.find('html').find('body'))

    def test_render_to_html_valid_variables(self):
        """Are all template variables in html valid?
        """
        marker = "TEMPLATESTRINGINVALID"
        settings.TEMPLATE_STRING_IF_INVALID = marker

        issue = Issue.objects.create(newsletter=self.newsletter,
                                     pub_date=datetime.date.today())
        html = issue.render_to_html(
            html_template_name='bulletin/api/test/html_template.html')

        self.assertEqual(html.find(marker), -1)

    def test_init_from_issue_template(self):
        """Does init_from_issue_template() work?
        """
        issue_template = IssueTemplate.objects.create(
            newsletter=self.newsletter,
            subject='Test Issue Template',
            from_name='Gregory Polanco',
            from_email='elcoffee@bucs.com',
            reply_to_email='out@of.com',
            organization_name='I Guess',
            address_line_1='Though Who',
            address_line_2='Couldn\'t?',
            address_line_3='Even this',
            city='Is Getting',
            state='Tiring',
            postal_code='16159',
            country='US',
            html_template_name='pretty_email.html',
            text_template_name='utilitarian_email.html')
        issue = Issue.objects.create(newsletter=self.newsletter,
                                     pub_date=datetime.date.today())
        issue.init_from_issue_template(issue_template)

        for field_name in ['subject',
                           'from_name',
                           'from_email',
                           'reply_to_email',
                           'organization_name',
                           'address_line_1',
                           'address_line_2',
                           'address_line_3',
                           'city',
                           'state',
                           'postal_code',
                           'country',
                           'html_template_name',
                           'text_template_name']:
            self.assertEqual(getattr(issue_template, field_name),
                             getattr(issue, field_name))

    def test_available_for_newsletter_includes_correctly(self):
        approved_post = Post.objects.create(
            title='Blue headline',
            url='http://www.blue.com',
            submitter=self.user,
            approved=True,
            include_in_newsletter=True)
        available_posts = Post.available_for_newsletter()
        self.assertIn(approved_post, available_posts)

    def test_available_for_newsletter_excludes_unapproved(self):
        unapproved_post = Post.objects.create(
            title='Red headline',
            url='http://www.red.com',
            submitter=self.user,
            include_in_newsletter=False)
        available_posts = Post.available_for_newsletter()
        self.assertNotIn(unapproved_post, available_posts)

    def test_available_for_newsletter_excludes_already_included(self):
        issue = Issue.objects.create(newsletter=self.newsletter,
                                     pub_date=datetime.date.today())
        section = Section.objects.create(issue=issue,
                                         name='Not Too Bad')

        already_included_post = Post.objects.create(
            title='Green headline',
            url='http://www.green.com',
            submitter=self.user,
            include_in_newsletter=True,
            section=section)
        available_posts = Post.available_for_newsletter()
        self.assertNotIn(already_included_post, available_posts)
