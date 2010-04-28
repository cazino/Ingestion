# -*- coding: utf-8 -*-
import os, shutil, pdb, re
import Image
from django.db import transaction
from mp3 import metadata
from mp3.ingestion.ingestion_localsettings import ADMIN_ARTIST_URL, ADMIN_LABEL_URL, ADMIN_ALBUM_URL
from mp3.main import main_localsettings 
from mp3.ingestion.ingestion_localsettings import album_image_directory
from mp3.ingestion.mappers import ArtistMapper, LabelMapper, ReleaseMapper, TrackMapper, AudioFileMapper, ImageFileMapper
from mp3.main.models import Disc, Album, Vendor, Label, Artist
from mp3.ingestion.reports import Report
from mp3.ingestion.metadata import naming



class ArtistProcessor(object):

    def __init__(self, delivery, vendor, artist_form):
        self.delivery = delivery
        self.artist_form = artist_form
        self.vendor = vendor

    def build(self):
        self.artist_form.report = Report()
        try:
            artist = self._build()
            self.artist_form.report.success = True
            self.artist_form.report.admin_url =  ADMIN_ARTIST_URL + str(artist.pk)
            self.artist_form.report.name = artist.name
            self.artist_form.report.mdx_id = artist.pk
            self.artist_form.report.external_id = artist.artistvendor_set.get().external_artist_id
            return artist
        except Exception, e:
            self.artist_form.report.error = str(e)
            self.artist_form.report.success = False
        

    @transaction.commit_on_success    
    def _build(self):
        mapper = ArtistMapper(delivery=self.delivery, vendor=self.vendor)
        """
        if not self.artist_form:
            assert self.delivery.release.compil, "Formulaire artiste absent"
            return mapper.create()
        """
        create = self.artist_form.cleaned_data['create']
        if create: # Création d'un nouvel artist            
            return mapper.create(url=self.artist_form.cleaned_data['url'])
        else: # Liaison avec un artiste existant
            return mapper.link(mdx_artist=Artist.objects.get(pk=self.artist_form.cleaned_data['mdx_artist_id']))
             

class LabelProcessor(object):

    def __init__(self, delivery, label_form, vendor):
        self.delivery = delivery
        self.label_form = label_form
        self.vendor = vendor

    def build(self):
        self.label_form.report = Report()
        try:
            label = self._build()
            self.label_form.report.success = True
            self.label_form.report.admin_url =  ADMIN_LABEL_URL + str(label.pk)
            self.label_form.report.name = label.name
            self.label_form.report.external_id = label.labelvendor_set.get().external_label_id
            self.label_form.report.mdx_id = label.pk
            return label
        except Exception, e:
            self.label_form.report.error = str(e)
            self.label_form.report.success = False
            pass

    @transaction.commit_on_success    
    def _build(self):
        mapper = LabelMapper(delivery=self.delivery, vendor=self.vendor)
        create = self.label_form.cleaned_data['create']
        if create: # Création d'un nouvel artiste
            return mapper.create()
        else: # Liaison avec un artiste existant
            mdx_label = Label.objects.get(pk=self.label_form.cleaned_data['mdx_label_id'])
            return mapper.link(mdx_label=mdx_label)

            



class ReleaseProcessor(object):
    """
    Process a collection of Tracks
    """
    def __init__(self, delivery, release_form, label, disc, vendor, artist=None):
        self.delivery = delivery
        self.release_form = release_form
        self.artist = artist
        self.label = label
        self.disc = disc
        self.vendor = vendor
     
    def album_path(self, album):
        """
        Ex: disk2/albums/4452
        """
        return os.path.join(self.disc.full_path(), "albums/%s" % album.pk) 
        
    def remove(self):
        shutil.rmtree(self.delivery.path)
        self.release_form.report = Report()
        self.release_form.report.success = True

    def build(self):
        self.release_form.report = Report()            
        try:
            album = self._build()
            self.release_form.report.success = True
            self.release_form.report.admin_url = ADMIN_ALBUM_URL + str(album.pk)
            self.release_form.report.admin_artist_url = ADMIN_ARTIST_URL + str(album.artist.pk)
            self.release_form.report.mdx_id = album.pk
            self.release_form.report.external_object_id = album.albumvendor_set.get().external_album_id
            # Artist report
            if album.artist.type == naming.COMPIL_FLAG:
                self.release_form.artist_report = Report()
                self.release_form.artist_report.success = True
                self.release_form.artist_report.admin_url = ADMIN_ARTIST_URL + str(album.artist.pk)
                self.release_form.artist_report.mdx_id = album.artist.pk
        except Exception, e:
            self.release_form.report.success = False
            self.release_form.report.error = str(e)
        else:
            try:
                shutil.rmtree(self.delivery.path)
            except:
                pass
            return album

    @transaction.commit_on_success    
    def _build(self):
        try:
            return self._build_aux()
        except:
            try:
                album = Album.objects.get(albumvendor__external_album_id=self.release_form.cleaned_data['pk'])
                album_path = self.album_path(album)
                pattern = re.compile("/%s/[0-9]*$" % (main_localsettings.ALBUMS_DIRECTORY,))
                if os.path.exists(album_path) and pattern.search(album_path):
                    shutil.rmtree(album_path)
            except Album.DoesNotExist:
                pass
            finally:
                raise
    
    def _build_aux(self):
        if not self.artist:
            assert self.delivery.release.compil, "Artiste absent, impossible créer album"
            artist_mapper = ArtistMapper(delivery=self.delivery, vendor=self.vendor)
            self.artist = artist_mapper.create()
        # Create album
        release_mapper = ReleaseMapper(delivery=self.delivery, artist=self.artist, label=self.label, vendor=self.vendor)
        album = release_mapper.create() 
        # Create directory
        album_path = self.album_path(album)
        mp3_path = os.path.join(album_path, 'mp3')
        samples_path = os.path.join(album_path, 'samples')
        images_path = os.path.join(album_path, 'images')
        os.mkdir(album_path)
        os.mkdir(mp3_path)
        os.mkdir(samples_path)
        os.mkdir(images_path)
        # Process Tracks
        for delivery_track in self.delivery.tracks:
            track_processor = TrackProcessor(disc=self.disc, album=album, delivery_track=delivery_track)
            track = track_processor.build()
        #Process Images
        imagefile_processor = ImageFileProcessor(delivery_image=self.delivery.image,
                                                 album=album, disc=self.disc)
        imagefile_processor.build()
        return album
    
    
class TrackProcessor(object):
    """
    Process one Track
    """
    def __init__(self, disc, album, delivery_track):
        self.disc = disc
        self.album = album
        self.delivery_track = delivery_track
        
    def build(self):
        track_mapper = TrackMapper(album=self.album, delivery_track=self.delivery_track)
        track = track_mapper.create()
        for delivery_audiofile in self.delivery_track.audio_files.values():
                if delivery_audiofile:
                    audiofile_processor = AudioFileProcessor(delivery_audiofile=delivery_audiofile, track=track, disc=self.disc)
                    audiofile_processor.build()
        return track
        
class AudioFileProcessor(object):
    """
    Process one audiofile
    """
    def __init__(self, disc, track, delivery_audiofile):
        self.disc = disc
        self.track = track
        self.delivery_audiofile = delivery_audiofile
    
    def build(self):
        audiofile_mapper = AudioFileMapper(delivery_audiofile=self.delivery_audiofile, track=self.track, disc=self.disc)
        audiofile = audiofile_mapper.create()
        shutil.copy(self.delivery_audiofile.path, audiofile.full_path())


class ImageFileProcessor(object):
    """
    Process an image file (copy files and modify database)
    """
    
    def __init__(self, delivery_image, album, disc):
        self.delivery_image = delivery_image
        self.album = album
        self.disc = disc

    def build(self):
        src_image = Image.open(self.delivery_image.path)
        format = self.delivery_image.format
        res = []
        # Ex /home/mondomx/disk3/albums/542/images
        #images_directory = os.path.join(self.disc.full_path(),
        #                               album_image_directory(self.album.pk))
        images_directory = os.path.join(self.album.full_path(self.disc), main_localsettings.IMAGES_DIRECTORY)
        for size in metadata.IMAGES_SIZES:
            # Resize images
            im = src_image.resize((size, size))
            usage = "cover%s" % (size)
            filename = "%s.%s" % (usage, self.delivery_image.format)
            filepath = os.path.join(images_directory, filename)
            im.save(filepath)
            size = os.path.getsize(filepath)
            (width, height) = im.size
            # Mapping to database
            imagefile_mapper = ImageFileMapper(usage=usage, path=os.path.join("/", 
                                                                              main_localsettings.ALBUMS_DIRECTORY,
                                                                              str(self.album.pk),
                                                                              main_localsettings.IMAGES_DIRECTORY,
                                                                              filename),
                                               size=size, width=width, height=height, 
                                               disc=self.disc, album=self.album, format=self.delivery_image.format)
        
            res.append(imagefile_mapper.create())
        return res
            
