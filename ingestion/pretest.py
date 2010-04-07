import sys, os, pdb
from django.core.management import setup_environ

project_path = os.path.split(os.path.split(os.getcwd())[0])[0]
sys.path.append(project_path)
from mp3 import settings
setup_environ(settings)
from mp3.main import main_localsettings
from mp3.main.models import ArtistVendor, Artist, LabelVendor, Label,  AlbumVendor, Album

    

"""
Delete the DEFAULT_BATCH_PATH if exists
Copy the content of 'batch_backup' directory in the 'batch' directory
"""
import shutil, os
from mp3.ingestion.ingestion_localsettings import TEST_APP, DEFAULT_BATCH_PATH
if os.path.exists(DEFAULT_BATCH_PATH):
    shutil.rmtree(DEFAULT_BATCH_PATH)
shutil.copytree(os.path.join(TEST_APP, 'batch_backup'), DEFAULT_BATCH_PATH)


"""
Init DISCOTHEQUE_BASEPATH
"""
from mp3.main.models import Disc
main_localsettings.DISCOTHEQUE_BASEPATH = TEST_APP

"""
Delete the albums_directory if exits and re-create it 
"""
default_disc = Disc.objects.get(status='default')
albums_directory = os.path.join(default_disc.full_path(), main_localsettings.ALBUMS_DIRECTORY)
if os.path.exists(albums_directory):
    """
    Clean the directory
    """
    shutil.rmtree(albums_directory)
if not os.path.exists(albums_directory):
    os.makedirs(albums_directory)


"""
Clean the database of all previous ingestions
"""
from mp3.ingestion.models import Batch
batch = Batch(DEFAULT_BATCH_PATH)
from django.db import connection
for delivery in batch.good_deliveries():
    try:
        album = Album.objects.get(albumvendor__external_album_id=delivery.release.pk)
        artist = album.artist
        album.label.delete()
        artist.delete()
    except Album.DoesNotExist:
        try:
            Artist.objects.get(artistvendor__external_artist_id=delivery.artist.pk).delete()
        except Artist.DoesNotExist:
            pass
        try:
            Label.objects.get(labelvendor__external_label_id=delivery.label.pk).delete()
        except Label.DoesNotExist:
            pass






