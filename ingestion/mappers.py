# -*- coding: utf-8 -*-

from datetime import date
from mp3.main.models import Artist, Vendor, ArtistVendor, Label, LabelVendor, Album
from mp3.main.models import  AlbumVendor, Track, TrackVendor, AudioFile, Disc
from mp3.main.models import ImageFile, Prix, CountryIsoEn
from mp3.ingestion.metadata.idol_prices import price_dic
from mp3.ingestion.utils import latin1_to_ascii



class Mapper(object):

    def __init__(self, delivery):
        self.delivery = delivery
    
    
class ArtistMapper(object):
    
    def __init__(self, delivery, vendor):
        self.delivery = delivery
        self.vendor = vendor
        """
        self.name = name
        self.url = url
        self.pk = pk
        self.mdx_artist = mdx_artist
        """
        
    def _post_init(self, artist):
        artist.created = date.today()
        artist.url = latin1_to_ascii(('-').join(artist.url.split())).lower()

    def create(self, url=None):
        if self.delivery.release.compil:
            artist = Artist(name= "%s (compilation)" % (self.delivery.release.title,), 
                            url=self.delivery.release.title,
                            type='compilation')
            self._post_init(artist)
            artist.save()
        else:
            artist = Artist(name=self.delivery.artist.name, url=url)
            self._post_init(artist)
            artist.save()
            artist_vendor = ArtistVendor.objects.create(artist=artist, vendor=self.vendor, 
                                                    external_artist_id=self.delivery.artist.pk)
        return artist
        
    def link(self, mdx_artist):
        artist_vendor = ArtistVendor.objects.create(artist=mdx_artist, vendor=self.vendor,
                                                    external_artist_id=self.delivery.artist.pk)
        return artist_vendor.artist
        
        
        
class LabelMapper(object):

    def __init__(self, delivery=None, vendor=None):
        self.delivery = delivery
        self.vendor = vendor
        
    def create(self):
        label = Label.objects.create(name=self.delivery.label.name, created=date.today())
        label_vendor = LabelVendor.objects.create(vendor=self.vendor, label=label, external_label_id=self.delivery.label.pk)
        return label  
                
    def link(self, mdx_label):
        label_vendor = LabelVendor.objects.create(vendor=self.vendor, label=mdx_label, 
                                                  external_label_id=self.delivery.label.pk)
        return mdx_label
        
    
class ReleaseMapper(Mapper):

    def __init__(self, delivery, artist, label, vendor):
        super(ReleaseMapper, self).__init__(delivery)
        self.artist = artist
        self.label = label
        self.vendor = vendor
    
    def _build_notes(self):
        notes = (',').join([style.name for style in self.delivery.styles])
        return notes + " - IDOL-ID: %s" % (str(self.delivery.release.pk))
    
    def _build_territories(self):
        """
        Construct the list all territoires
        Transform WW -> all territories avalaible
        """
        delivery_territories = set(self.delivery.release.territories)
        if ('WW' in delivery_territories or 'ww' in delivery_territories):
            return [code for (code, ) in CountryIsoEn.objects.all().values_list('code')]
        else:
            return self.delivery.release.territories

    def create(self):
        prix = Prix.objects.get(code=price_dic[self.delivery.release.price])
        album = Album.objects.create(title=self.delivery.release.title, 
                                     territories=','.join(self._build_territories()),
                                     artist=self.artist, label=self.label, 
                                     publish_date=self.delivery.release.publish_date,
                                     publish_date_digital=self.delivery.release.publish_date_digital,
                                     prix=prix, created=date.today(), domain='boutique',
                                     vendor=self.vendor, upc=self.delivery.release.upc,
                                     notes=self._build_notes())
        album_vendor = AlbumVendor.objects.create(vendor=self.vendor, album=album, external_album_id=self.delivery.release.pk)
        return album
        

class TrackMapper(object):
    
    def __init__(self, album, delivery_track):
        self.album = album
        self.delivery_track = delivery_track
        
    def create(self):
        prix = Prix.objects.get(code=price_dic[self.delivery_track.price])
        track = Track.objects.create(album=self.album, disc_number=self.delivery_track.disc_number, 
                                     track_number=self.delivery_track.track_number,
                                     vente_autitre=not(self.delivery_track.bundle_only),
                                     vente_alalbum=True, prix=prix,
                                     title=self.delivery_track.title, isrc=self.delivery_track.isrc,
                                     author=self.delivery_track.author,
                                     composer=self.delivery_track.composer)
        track_vendor = TrackVendor.objects.create(track=track, external_track_id=self.delivery_track.pk)
        return track
        

class AudioFileMapper(object):

    def __init__(self, delivery_audiofile, track, disc):
        self.delivery_audiofile = delivery_audiofile
        self.track =  track
        self.disc = disc

    def _sub_dir_name(self):
        """
        Return the name of the sub directory tu put the audiofiles
        'mp3' or 'samples'
        """
        if self.delivery_audiofile.content == 'piste':
            return 'mp3'
        elif self.delivery_audiofile.content == 'extrait':
            return 'samples'

    def create(self):
        tmp_filename = "%s_%s_%s.%s" % (self.track.album.artist.name, self.track.album.title, self.track.title, self.delivery_audiofile.format)
        filename = latin1_to_ascii(tmp_filename.replace(" ", "_"))
        path = "/albums/%s/%s/%s" % (self.track.album.pk, self._sub_dir_name(), filename)
        return AudioFile.objects.create(path=path, size=self.delivery_audiofile.size, content=self.delivery_audiofile.content,
                                        bitrate=self.delivery_audiofile.bitrate, duration=self.delivery_audiofile.duration, disc=self.disc,
                                        format=self.delivery_audiofile.format, track=self.track)    


class ImageFileMapper(object):

    def __init__(self, disc, album, path, format, size, width, height, usage):
        self.album =  album
        self.disc = disc
        self.format = format
        self.height = height
        self.path = path
        self.size = size
        self.usage = usage
        self.width = width

    def create(self):
        return ImageFile.objects.create(album=self.album, disc=self.disc, size=self.size,
                                        path=self.path, width=self.width, height=self.height,
                                        usage=self.usage, format=self.format)
        
             
        

    
