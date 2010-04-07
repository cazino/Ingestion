"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from datetime import datetime
import sqlparse
from django.db import models
from django.test import TestCase
from django.test.client import Client
from mp3.main.models import Orders, Album, Artist, Label, Vendor, ArtistVendor
from mp3.main.views.common import BestAlbumSellCalculator


"""
class HomapageTest(TestCase):
    
    fixtures = ['home.json',]
    
    def setUp(self):
        self.client = Client()

    def test_actualites_disque_album_name(self):
        response = self.client.post('', {'language': 'en'})
        self.assertEqual("The Intergalactic Slapstick", response.context['ActualitesDisque'][0]['album_title'])

    def test_actualites_disque_pays(self):
        response = self.client.post('', {'language': 'en'})
        self.assertEqual("Etats-Unis", response.context['ActualitesDisque'][0]['pays'])
     

class ValidatedOrders(TestCase):

    def test_validated_order_form1(self):
        order = Orders.objects.create(payment_status='Completed', validation_date=datetime.today())
        self.assertEqual(order, Orders.validated_objects.get())
        
    def test_validated_order_form2(self):
        order = Orders.objects.create(payment_status='Canceled_Reversal', validation_date=datetime.today())
        self.assertEqual(order, Orders.validated_objects.get())
        
        
class UnValidatedOrders(TestCase):

    def test_no_validation_date(self):
        order = Orders.objects.create(validation_date=None)
        self.assertEqual(0, Orders.validated_objects.count())
        
    def test_good_payment_status_but_no_date(self):
        order = Orders.objects.create(payment_status='Completed', validation_date=None)
        self.assertEqual(0, Orders.validated_objects.count())
        
    def test_bad_payment_status_with_date(self):
        order = Orders.objects.create(payment_status='aaaaa', validation_date=datetime.today())
        self.assertEqual(0, Orders.validated_objects.count())
        
        
class BestAlbumSellCalculatorTest(TestCase):

    def setUp(self):
        self.calculator = BestAlbumSellCalculator()

    def test_construct(self):
        self.assert_(self.calculator)
        
    def test_no_sale(self):
        self.assertEqual(list(Album.objects.none()), list(self.calculator.calculate()))
        
    def test_one_sell(self):
        album = Album.objects.create()
        self.assertEqual(album, self.calculator.calculate().get())
        
"""        
    
def print_sql(qs):
    q = qs.query.as_sql()
    statement = q[0] % q[1]
    print sqlparse.format(statement, reindent=True, keyword_case='upper')    

class ArtistManagerGetByPk(TestCase):

    def test_postive(self):
        pk = 5
        vendor = Vendor.objects.create(name='vendor_name')
        artist = Artist.objects.create(name='artist_name')
	artist_vendor = ArtistVendor.objects.create(artist=artist, vendor=vendor, external_artist_id=pk)
	self.assertEquals(artist, Artist.objects.get_by_pk(pk=pk, vendor=vendor))

    def test_negative(self):
        pk = 5
        vendor = Vendor.objects.create(name='vendor_name')
        artist = Artist.objects.create(name='artist_name')
	self.assertRaises(Artist.DoesNotExist, Artist.objects.get_by_pk, pk=pk, vendor=vendor)

class ArtistManagerSimilarName(TestCase):
        
    def test_easy_positive(self):
        artist = Artist.objects.create(name='les machins')
        self.assertTrue(artist in Artist.objects.similar_name('les'))

    def test_easy_negative(self):
        artist = Artist.objects.create(name='les machins')
        self.assertFalse(artist in Artist.objects.similar_name('prout'))
	

    def test_positive(self):
        artist = Artist.objects.create(name='4 Etoiles - Les Quatre Etoiles')
        query_set = Artist.objects.similar_name('Quatre Prout')
        self.assertTrue(artist in query_set)
	
class LabelManagerSimilarName(TestCase):

    def test_easy_positive(self):
        label = Label.objects.create(name='les machins')
        self.assertTrue(label in Label.objects.similar_name('les'))

    def test_easy_negative(self):
        label = Label.objects.create(name='les machins')
        self.assertEqual(0, Label.objects.similar_name('prout').count())

    def test_positive(self):
        label = Label.objects.create(name='4 Etoiles - Les Quatre Etoiles')
        query_set = Label.objects.similar_name('Quatre Prout')
        self.assertTrue(label in query_set)        
	

    






