import json

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from bulletin.tools.plugins.models import Story


class StoryTests(APITestCase):

    def setUp(self):
        self.new_story_data = {
            'title': 'Test Story Headline',
            'url': 'http://api.aashe.org',
            'blurb': 'Really excellent stuff happening here.',
            'date': '2014-10-10T23:59Z'
        }
        self.client = APIClient()
        self.staff_user = User.objects.create(username='staff',
                                              is_staff=True)
        self.non_staff_user = User.objects.create(username='non-staff',
                                                  is_staff=False)

        self.stories = {
            'blue': Story.objects.create(
                title='Blue headline',
                url='http://www.agami.com',
                submitter=self.staff_user,
                blurb='And so it goes . . .',
                date='2015-11-11T23:59Z'),
            'red': Story.objects.create(
                title='Red headline',
                url='http://www.red.com',
                submitter=self.staff_user,
                blurb='For scorez and muy years ago . . .',
                date='1972-09-07T23:59Z'),
            'green': Story.objects.create(
                title='Green headline',
                url='http://www.green.com',
                submitter=self.staff_user,
                blurb='For every season, turn . . . ',
                date='1969-06-09T23:59Z')
        }

    def login(self, admin=False):
        if admin:
            self.client.force_authenticate(user=self.staff_user)
        else:
            self.client.force_authenticate(user=self.non_staff_user)

    def test_create_story(self):
        """Can we create a Story?
        """
        self.login(admin=True)
        url = reverse('bulletin:plugins:api:story-list')
        response = self.client.post(url,
                                    self.new_story_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_story_only_for_admins(self):
        """Is create a story only for admins?
        """
        self.login(admin=False)
        url = reverse('bulletin:plugins:api:story-list')
        response = self.client.post(url,
                                    self.new_story_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_stories(self):
        self.login(admin=False)
        url = reverse('bulletin:plugins:api:story-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_story_details(self):
        self.login(admin=False)
        story = self.stories.values()[0]
        url = reverse('bulletin:plugins:api:story-detail',
                      kwargs={'pk': story.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_story_update(self):
        """Can we update a Story?
        """
        self.login(admin=True)
        story = self.stories.values()[0]
        new_blurb = story.blurb * 2 if story.blurb else "Yatcha!"
        url = reverse('bulletin:plugins:api:story-detail',
                      kwargs={'pk': story.id})

        # GET to get all fields:
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        story_json = json.loads(response.content)
        story_json['blurb'] = new_blurb

        response = self.client.put(url, story_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # We have a dirty story.
        story = Story.objects.get(pk=story.id)
        self.assertEqual(story.blurb, new_blurb)

    def test_story_update_only_for_admins(self):
        """Are non-admins prevented from updating a Story?
        """
        self.login(admin=False)
        story = self.stories.values()[0]
        new_blurb = story.blurb * 2 if story.blurb else "Yatcha!"
        url = reverse('bulletin:plugins:api:story-detail',
                      kwargs={'pk': story.id})

        # GET to get all fields:
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        story_json = json.loads(response.content)
        story_json['blurb'] = new_blurb

        response = self.client.put(url, story_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_story(self):
        self.login(admin=True)
        story = self.stories.values()[0]
        url = reverse('bulletin:plugins:api:story-detail',
                      kwargs={'pk': story.id})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertRaises(Story.DoesNotExist,
                          Story.objects.get,
                          pk=story.id)

    def test_delete_story_only_for_admins(self):
        """Have to be an admin to delete a Story?
        """
        self.login(admin=False)
        story = self.stories.values()[0]
        url = reverse('bulletin:plugins:api:story-detail',
                      kwargs={'pk': story.id})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
