# -*- coding: utf-8 -*-
import codecs
from django.core import serializers
from mp3.main.models import ActualitesDisque, Album, ArtistCountry, CoupsDeCoeur, Country, ImageFile
from mp3 import settings

actu_disque =  ActualitesDisque.objects.all()
coup_de_coeur = CoupsDeCoeur.objects.all()

albums = []
for i in range(1, 4):
    albums += eval("[ad.album%s for ad in actu_disque]" % (i,))
    albums += eval("[cdp.album%s for cdp in coup_de_coeur]" % (i,))
albums = set(albums)   
artists = set([album.artist for album in albums])
countries= Country.objects.none()
for artist in artists:
    countries =  countries | artist.countries.all()
countries = set(list(countries))
images = ImageFile.objects.none()
for album in albums:
    images = images |  album.imagefile_set.all()
images = set(list(images))

artists_countries = set(list(ArtistCountry.objects.filter(artist__in=[artist.pk for artist in artists])))
actu_disque = set(list(actu_disque))
coup_de_coeur = set(list(coup_de_coeur))

datas = albums.union(artists).union(countries).union(images).union(artists_countries).union(coup_de_coeur).union(actu_disque)
#datas = artists.union(countries).union(images)

"""
data = unicode(serializers.serialize("json", albums, indent=4, ensure_ascii=False))
data += u"\n" + unicode(serializers.serialize("json", artists, indent=4))
data += "\n" + unicode(serializers.serialize("json", countries, indent=4))
data += "\n" + unicode(serializers.serialize("json", images, indent=4))
"""
out = codecs.open(settings.PROJECT_PATH + "/main/fixtures/home.json", "w", "utf-8")
out.write(unicode(serializers.serialize("json", datas, indent=4, ensure_ascii=False)))
out.close()

