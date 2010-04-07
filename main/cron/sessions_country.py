import sys, os, pdb
from django.core.management import setup_environ
sys.path.append('/home/kazou/dev/gitted')
from mp3 import settings
setup_environ(settings)
from mp3.main.models import Paniers, ProfilSessions, CountryIp



for session in ProfilSessions.objects.filter(country=''):
    country_ip = CountryIp.objects.extra(
                   where=["ip_from <= INET_ATON(%s) AND INET_ATON(%s) <= ip_to " % (session.user_ip,session.user_ip)])
    session.country = country_ip.get().country_code2
    session.save()
