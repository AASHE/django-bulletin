import json

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from bulletin.tools.plugins.models import NewResource


def create_staff_user():
    staff_user = User(username='staff',
                      is_staff=True)
    staff_user.save()
    return staff_user


class NewResourceTests(APITestCase):

    def setUp(self):
        self.new_new_resource_data = {
            'title': 'Test NewResource Headline',
            'url': 'http://api.aashe.org',
            'blurb': 'Really excellent stuff happening here.'
        }
        self.client = APIClient()
        self.staff_user = create_staff_user()
        self.non_staff_user = User.objects.create(username='non-staff',
                                                  is_staff=False)

        self.stories = {
            'blue': NewResource(title='Blue headline',
                                url='http://www.agami.com',
                                submitter=self.staff_user,
                                blurb='And so it goes . . .'),
            'red': NewResource(title='Red headline',
                               url='http://www.red.com',
                               submitter=self.staff_user,
                               blurb='For scorez and muy years ago . . .'),
            'green': NewResource(title='Green headline',
                                 url='http://www.green.com',
                                 submitter=self.staff_user,
                                 blurb='For every season, turn . . . ')
        }

        for new_resource in self.stories.values():
            new_resource.save()

    def login(self, admin=False):
        if admin:
            self.client.force_authenticate(user=self.staff_user)
        else:
            self.client.force_authenticate(user=self.non_staff_user)

    def test_create_new_resource(self):
        """Can we create a NewResource?
        """
        self.login(admin=True)
        url = reverse('bulletin:plugins:api:new-resource-list')
        response = self.client.post(url,
                                    self.new_new_resource_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_new_resource_only_for_admins(self):
        """Is create a NewResource only for admins?
        """
        self.login(admin=False)
        url = reverse('bulletin:plugins:api:new-resource-list')
        response = self.client.post(url,
                                    self.new_new_resource_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_stories(self):
        self.login(admin=False)
        url = reverse('bulletin:plugins:api:new-resource-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_new_resource_details(self):
        self.login(admin=False)
        new_resource = self.stories.values()[0]
        url = reverse('bulletin:plugins:api:new-resource-detail',
                      kwargs={'pk': new_resource.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_new_resource_update(self):
        self.login(admin=True)
        new_resource = self.stories.values()[0]
        new_blurb = (new_resource.blurb * 2
                     if new_resource.blurb
                     else "Yatcha!")
        url = reverse('bulletin:plugins:api:new-resource-detail',
                      kwargs={'pk': new_resource.id})

        # GET to get all fields:
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        new_resource_json = json.loads(response.content)
        new_resource_json['blurb'] = new_blurb

        response = self.client.put(url, new_resource_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # We have a dirty new_resource.
        new_resource = NewResource.objects.get(pk=new_resource.id)
        self.assertEqual(new_resource.blurb, new_blurb)

    def test_new_resource_update_only_for_admins(self):
        self.login(admin=False)
        new_resource = self.stories.values()[0]
        new_blurb = (new_resource.blurb * 2
                     if new_resource.blurb
                     else "Yatcha!")
        url = reverse('bulletin:plugins:api:new-resource-detail',
                      kwargs={'pk': new_resource.id})

        # GET to get all fields:
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        new_resource_json = json.loads(response.content)
        new_resource_json['blurb'] = new_blurb

        response = self.client.put(url, new_resource_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_new_resource(self):
        self.login(admin=True)
        new_resource = self.stories.values()[0]
        url = reverse('bulletin:plugins:api:new-resource-detail',
                      kwargs={'pk': new_resource.id})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertRaises(NewResource.DoesNotExist,
                          NewResource.objects.get,
                          pk=new_resource.id)

    def test_delete_new_resource_only_for_admins(self):
        self.login(admin=False)
        new_resource = self.stories.values()[0]
        url = reverse('bulletin:plugins:api:new-resource-detail',
                      kwargs={'pk': new_resource.id})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
