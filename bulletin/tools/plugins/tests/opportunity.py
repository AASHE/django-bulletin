import datetime

from django.contrib.auth.models import User
from django.test import TestCase
import pytz

from bulletin.tools.plugins.models import Opportunity


class OpportunityTests(TestCase):

    def setUp(self):
        self.opportunity = Opportunity.objects.create(
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
            # Opportunity-only fields:
            blurb="blah blah blah")

    def test_clone_handles_simple_fields(self):
        """ Does clone() handle simple fields correctly? """
        clone = self.opportunity.clone()
        self.assertEqual(clone.blurb, self.opportunity.blurb)
