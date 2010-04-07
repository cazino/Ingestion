# -*- coding: utf-8 -*-
from django.test import TestCase
from mp3.ingestion.utils import propose_url
from mp3.main.models import Artist


class TestUtils(TestCase):

    def test_url_proposal_1(self):
        self.assertEqual('jojo', propose_url('jojo'))

    def test_url_proposal_2(self):
        # Remplace les espaces par '-' et enlève les accents
        self.assertEqual(u'jojo-le-demago', propose_url(u'jojo le démago'))

    def test_url_proposal_3(self):
        #To lower case
        self.assertEqual(u'jojo-le-demago', propose_url(u'joJo le démago'))

    def test_url_proposal_4(self):
        # Renvoie uen string vide quand l'url existe déjà
        artist = Artist.objects.create(name=u'jojo', url='jojo-le-demago')
        self.assertEqual("", propose_url(u'jojo le démago'))

