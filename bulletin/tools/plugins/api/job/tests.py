import json

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from bulletin.tools.plugins.models import Job


class JobTests(APITestCase):

    def setUp(self):
        self.new_job_data = {
            'title': 'Test Job Headline',
            'url': 'http://api.aashe.org',
            'organization': 'Acme, Inc.'
        }
        self.client = APIClient()
        self.staff_user = User.objects.create(username='staff',
                                              is_staff=True)
        self.non_staff_user = User.objects.create(username='non-staff',
                                                  is_staff=False)

        self.jobs = {
            'blue': Job(title='Blue headline',
                        url='http://www.agami.com',
                        submitter=self.staff_user,
                        organization='Rabbitville'),
            'red': Job(title='Red headline',
                       url='http://www.red.com',
                       submitter=self.staff_user,
                       organization='Myopia Inc.'),
            'green': Job(title='Green headline',
                         url='http://www.green.com',
                         submitter=self.staff_user,
                         organization='Tooney Loonies'),
        }

        for job in self.jobs.values():
            job.save()

    def login(self, admin=False):
        if admin:
            self.client.force_authenticate(user=self.staff_user)
        else:
            self.client.force_authenticate(user=self.non_staff_user)

    def test_create_job(self):
        """Can we create a Job?
        """
        self.login(admin=True)
        url = reverse('bulletin:plugins:api:job-list')
        response = self.client.post(url,
                                    self.new_job_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_job_only_for_admins(self):
        """Can only admins create jobs?
        """
        self.login(admin=False)
        url = reverse('bulletin:plugins:api:job-list')
        response = self.client.post(url,
                                    self.new_job_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_jobs(self):
        self.login(admin=False)
        url = reverse('bulletin:plugins:api:job-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_job_details(self):
        self.login(admin=False)
        job = self.jobs.values()[0]
        url = reverse('bulletin:plugins:api:job-detail',
                      kwargs={'pk': job.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_job_update(self):
        self.login(admin=True)
        job = self.jobs.values()[0]
        new_organization = (job.organization * 2
                            if job.organization
                            else "Yatcha!")
        url = reverse('bulletin:plugins:api:job-detail',
                      kwargs={'pk': job.id})

        # GET to get all fields:
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        job_json = json.loads(response.content)
        job_json['organization'] = new_organization

        response = self.client.put(url, job_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # We have a dirty job.
        job = Job.objects.get(pk=job.id)
        self.assertEqual(job.organization, new_organization)

    def test_job_update_only_for_admins(self):
        self.login(admin=False)
        job = self.jobs.values()[0]
        new_organization = (job.organization * 2
                            if job.organization
                            else "Yatcha!")
        url = reverse('bulletin:plugins:api:job-detail',
                      kwargs={'pk': job.id})

        # GET to get all fields:
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        job_json = json.loads(response.content)
        job_json['organization'] = new_organization

        response = self.client.put(url, job_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_job(self):
        self.login(admin=True)
        job = self.jobs.values()[0]
        url = reverse('bulletin:plugins:api:job-detail',
                      kwargs={'pk': job.id})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertRaises(Job.DoesNotExist,
                          Job.objects.get,
                          pk=job.id)

    def test_delete_job_only_for_admins(self):
        self.login(admin=False)
        job = self.jobs.values()[0]
        url = reverse('bulletin:plugins:api:job-detail',
                      kwargs={'pk': job.id})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
