import datetime

from django.contrib.auth.models import User
from django.test import TestCase
import pytz

from bulletin.tools.plugins.models import Job


class JobTests(TestCase):

    def setUp(self):
        self.job = Job.objects.create(
            # Post fields -- tested in PostTests:
            date_submitted=datetime.datetime.now(pytz.utc),
            title='Blue headline',
            url='http://www.agami.com',
            submitter=User.objects.create(username='Burroughs'),
            approved=True,
            include_in_newsletter=False,
            feature=True,
            pub_date=datetime.datetime.now(pytz.utc),
            image="cleaver_artist.jpg",
            # Job-only fields:
            organization="What a way to store organization")

    def test_clone_handles_simple_fields(self):
        """ Does clone() handle simple fields correctly? """
        clone = self.job.clone()
        self.assertEqual(clone.organization, self.job.organization)
