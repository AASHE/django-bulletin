import datetime

from django.test import TestCase

from bulletin.models import Ad, AdSize


class AdTests(TestCase):

    def test_ads_for_works(self):
        """Does ads_for work?
        """
        ad_size = AdSize.objects.create(name="Who cares",
                                        height=1,
                                        width=1)
        current_ad = Ad.objects.create(name="Current",
                                       size=ad_size,
                                       start=datetime.date(1000, 1, 1),
                                       end=datetime.date(3000, 1, 1),
                                       show_on_website=True)
        ads_for_today = Ad.ads_for(date=datetime.date.today(),
                                   show_on_website=True,
                                   include_in_newsletter=True)
        self.assertEqual(current_ad.id,
                         ads_for_today.first().id)
