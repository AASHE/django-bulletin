import datetime

from django.contrib.auth.models import User
from django.test import TestCase
import pytz

from bulletin.tools.plugins.models import Event


class EventTests(TestCase):

    def setUp(self):
        self.event = Event.objects.create(
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
            # Event-only fields:
            start_date=datetime.datetime.now(pytz.utc),
            end_date=datetime.datetime.now(pytz.utc),
            time="What a way to store time",
            organization="What a way to store organization",
            location="What a way to store location")

    def test_clone_handles_simple_fields(self):
        """ Does clone() handle simple fields correctly? """
        clone = self.event.clone()
        self.assertEqual(clone.start_date, self.event.start_date)
        self.assertEqual(clone.end_date, self.event.end_date)
        self.assertEqual(clone.time, self.event.time)
        self.assertEqual(clone.organization, self.event.organization)
        self.assertEqual(clone.location, self.event.location)
