from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from bulletin.models import Newsletter


class NewsletterTests(TestCase):

    def setUp(self):
        password = 'password'
        user = User.objects.create_superuser('user',
                                             'user@user.com',
                                             password)

        self.NEWSLETTER_NAME = 'Bob and Bill Go To Heaven'
        self.newsletter = Newsletter(name=self.NEWSLETTER_NAME)
        self.newsletter.save()

        self.client = Client()
        self.client.login(username=user.username,
                          password=password)

    def test_newsletter_list(self):
        """Can we pull up a list of newsletters?
        """
        response = self.client.get(reverse('bulletin:newsletter-list'))
        # Did the list come up?
        self.assertEqual(response.status_code, 200)
        # Does the list include our newsletter?
        self.assertTrue(response.content.find(self.NEWSLETTER_NAME) > -1)

    def test_newsletter_editor(self):
        """Can we pull up the newsletter editor?
        """
        response = self.client.get(reverse('bulletin:newsletter-update',
                                           kwargs={'pk': self.newsletter.id}),
                                   follow=True)
        # Did the editor come up?
        self.assertEqual(response.status_code, 200)
        # Does it include the name of our newsletter?
        self.assertTrue(response.content.find(self.NEWSLETTER_NAME) > -1)
