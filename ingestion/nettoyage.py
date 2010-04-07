import sys, os
from django.core.management import setup_environ
sys.path.append('/home/kazou/dev')
from mp3 import settings
setup_environ(settings)
from mp3.main import localsettings
from mp3.main.models import ArtistVendor, LabelVendor, AlbumVendor, Album


for alb_id in (28962, 28964):
    try:
        album = Album.objects.get(pk=alb_id)
        for track in album.track_set.all():
             for audiofile in track.audiofile_set.all():
                 audiofile.delete()
             track.delete()
             for imagefile in album.imagefile_set.all():
                 imagefile.delete()
        album.delete()
    except Album.DoesNotExist:
        pass 
