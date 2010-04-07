from django.test import TransactionTestCase
from mp3.main.models import Artist
from mp3.ingestion.transaction import artist_insert


class TransactionTest(TransactionTestCase):

    def test(self):        
        artist_insert()
        Artist.objects.get(pk=2)

        
