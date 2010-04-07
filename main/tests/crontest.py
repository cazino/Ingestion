from django.test import TestCase
from mp3.main.models import Paniers, ProfilSessions, CountryIp



class CronTest(TestCase):
    
    def test_one(self):
        session  = ProfilSessions.objects.create()
        self.assertFalse(ProfilSessions.objects.filter(country='').filter(paniers__pk__isnull=False).count())

    def test_two(self):
        session  = ProfilSessions.objects.create(session_id='azde')
        panier = Paniers.objects.create(session=session)
        self.assertTrue(ProfilSessions.objects.filter(country='').filter(paniers__pk__isnull=False).count())

   
   
     
