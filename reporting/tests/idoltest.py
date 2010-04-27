# -*- coding: utf-8 -*-
from django.test import TestCase
import pdb

class ArtistMapperTest(TestCase):
           
    def setUp(self):
        self.delivery = IDOLDelivery(TEST_COMMON + '/batch1/3596971288129')
        self.idol_vendor = Vendor.objects.create(pk=self.delivery.vendor_id)

    def _check_artist_vendor(self, produced_artist):
        artist_vendor = produced_artist.artistvendor_set.get(vendor=self.idol_vendor)
        self.assertEqual(self.idol_vendor, artist_vendor.vendor)
        self.assertEqual(self.delivery.artist.pk, artist_vendor.external_artist_id)

