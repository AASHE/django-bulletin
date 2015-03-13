import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from bulletin.models import Issue, Newsletter, Section, Post


class SectionTests(TestCase):

    def setUp(self):
        password = 'password'
        self.user = User.objects.create_superuser('user',
                                                  'user@user.com',
                                                  password)
        newsletter = Newsletter(name='Test Newsletter')
        newsletter.save()
        self.issue = Issue(newsletter=newsletter,
                           pub_date=datetime.date.today())
        self.issue.save()
        self.client = Client()
        self.client.login(username=self.user.username,
                          password=password)

    def test_create_section(self):
        """Can we create a section?
        """
        section_name = 'Test This'
        url = reverse('bulletin:section-create',
                      kwargs={'pk': self.issue.id})
        response = self.client.post(url,
                                    data={'name': section_name},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content.find(section_name) > -1)

    def test_delete_section(self):
        """Can we delete a section?
        """
        section = Section.objects.create(issue=self.issue,
                                         name='Comics')
        self.assertEqual(1, Section.objects.count())
        url = reverse('bulletin:section-delete',
                      kwargs={'pk': section.id})
        response = self.client.delete(url,
                                      follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(0, Section.objects.count())

    def test_delete_section_with_posts(self):
        """Can we delete a section with posts?
        """
        section = Section.objects.create(issue=self.issue,
                                         name='Comics')
        section.posts.add(
            Post.objects.create(section=section,
                                title='Important!',
                                submitter=self.user),
            Post.objects.create(section=section,
                                title='Ha!',
                                submitter=self.user))
        self.assertEqual(2, section.posts.count())
        url = reverse('bulletin:section-delete',
                      kwargs={'pk': section.id})
        response = self.client.delete(url,
                                      follow=True)
        self.assertEqual(response.status_code, 200)
        # Should remove posts from the section.
        self.assertEqual(0, section.posts.count())
        # But should not delete the posts.
        self.assertEqual(2, Post.objects.count())
