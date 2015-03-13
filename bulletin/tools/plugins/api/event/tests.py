import json

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from bulletin.tools.plugins.models import Event


class EventTests(APITestCase):

    def setUp(self):
        self.new_event_data = {
            'title': 'Test Event Headline',
            'url': 'http://api.aashe.org',
            'location': 'Burlington, MA',
            'start_date': '2014-10-10T23:59Z'
        }
        self.client = APIClient()
        self.staff_user = User.objects.create(username='staff',
                                              is_staff=True)
        self.non_staff_user = User.objects.create(username='non-staff',
                                                  is_staff=False)

        self.events = {
            'blue': Event(title='Blue headline',
                          url='http://www.agami.com',
                          submitter=self.staff_user,
                          start_date=timezone.now(),
                          location='Rabbitville'),
            'red': Event(title='Red headline',
                         url='http://www.red.com',
                         submitter=self.staff_user,
                         start_date=timezone.now(),
                         location='Myopia Inc.'),
            'green': Event(title='Green headline',
                           url='http://www.green.com',
                           submitter=self.staff_user,
                           start_date=timezone.now(),
                           location='Tooney Loonies'),
        }

        for event in self.events.values():
            event.save()

    def login(self, admin=False):
        if admin:
            self.client.force_authenticate(user=self.staff_user)
        else:
            self.client.force_authenticate(user=self.non_staff_user)

    def test_create_event(self):
        """Can we create a Event?
        """
        self.login(admin=True)
        url = reverse('bulletin:plugins:api:event-list')
        response = self.client.post(url,
                                    self.new_event_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_event_only_for_admins(self):
        """Is create a Event for admins only?
        """
        self.login(admin=False)
        url = reverse('bulletin:plugins:api:event-list')
        response = self.client.post(url,
                                    self.new_event_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_events(self):
        self.login(admin=False)
        url = reverse('bulletin:plugins:api:event-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_details(self):
        self.login(admin=False)
        event = self.events.values()[0]
        url = reverse('bulletin:plugins:api:event-detail',
                      kwargs={'pk': event.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_update(self):
        self.login(admin=True)
        event = self.events.values()[0]
        new_organization = (event.organization * 2
                            if event.organization
                            else "Yatcha!")
        url = reverse('bulletin:plugins:api:event-detail',
                      kwargs={'pk': event.id})

        # GET to get all fields:
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        event_json = json.loads(response.content)
        event_json['organization'] = new_organization

        response = self.client.put(url, event_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # We have a dirty event.
        event = Event.objects.get(pk=event.id)
        self.assertEqual(event.organization, new_organization)

    def test_event_update_only_for_admins(self):
        self.login(admin=False)
        event = self.events.values()[0]
        new_organization = (event.organization * 2
                            if event.organization
                            else "Yatcha!")
        url = reverse('bulletin:plugins:api:event-detail',
                      kwargs={'pk': event.id})

        # GET to get all fields:
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        event_json = json.loads(response.content)
        event_json['organization'] = new_organization

        response = self.client.put(url, event_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_event(self):
        self.login(admin=True)
        event = self.events.values()[0]
        url = reverse('bulletin:plugins:api:event-detail',
                      kwargs={'pk': event.id})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertRaises(Event.DoesNotExist,
                          Event.objects.get,
                          pk=event.id)

    def test_delete_event_only_for_admins(self):
        self.login(admin=False)
        event = self.events.values()[0]
        url = reverse('bulletin:plugins:api:event-detail',
                      kwargs={'pk': event.id})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
