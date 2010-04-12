# -*- coding: utf-8 -*-
from datetime import date
from django.test import TestCase
from django.db.models import ObjectDoesNotExist
from mp3.main.models import Artist, Vendor, ArtistVendor, Label, Track, TrackVendor, Album, AudioFile, Disc, Prix
from mp3.main.models import CountryIsoEn
from mp3.ingestion.models import IDOLDelivery, DeliveryTrack
from mp3.ingestion.mappers import ArtistMapper, LabelMapper, ReleaseMapper, AudioFileMapper, TrackMapper
from mp3.ingestion.mappers import ImageFileMapper
from mp3.ingestion.metadata.idol_prices import price_dic
from mp3.ingestion.ingestion_localsettings import TEST_COMMON
from mp3.ingestion.utils import latin1_to_ascii
import datapaths

import pdb

class ArtistMapperTest(TestCase):
           
    def setUp(self):
        self.delivery = IDOLDelivery(TEST_COMMON + '/batch1/3596971288129')
        self.idol_vendor = Vendor.objects.create(pk=self.delivery.vendor_id)

    def _check_artist_vendor(self, produced_artist):
        artist_vendor = produced_artist.artistvendor_set.get(vendor=self.idol_vendor)
        self.assertEqual(self.idol_vendor, artist_vendor.vendor)
        self.assertEqual(self.delivery.artist.pk, artist_vendor.external_artist_id)

    def _check_commons(self, produced_artist):
        self.assertEqual(date.today(), produced_artist.created)
   
    def test_init(self):
        self.assert_(ArtistMapper(vendor=self.idol_vendor, delivery=self.delivery))

    def test_create(self):
        artist_mapper = ArtistMapper(vendor=self.idol_vendor, delivery=self.delivery)
        produced_artist = artist_mapper.create(url=self.delivery.artist.name)
        self.assertEqual(self.delivery.artist.name, produced_artist.name)
        self.assertEqual('wax-tailor', produced_artist.url)
        self._check_artist_vendor(produced_artist)
        self._check_commons(produced_artist)

    def test_create_clean_url(self):
        artist_mapper = ArtistMapper(vendor=self.idol_vendor, delivery=self.delivery)
        produced_artist = artist_mapper.create(url=u"azé RG")
        self.assertEqual('aze-rg', produced_artist.url)
        
    def test_create_compil(self):
        delivery = IDOLDelivery(datapaths.compil1_path)
        artist_mapper = ArtistMapper(vendor=self.idol_vendor, delivery=delivery)
        produced_artist = artist_mapper.create()
        expected_name = "%s (compilation)" % (delivery.release.title,)
        expected_url = latin1_to_ascii(('-').join(delivery.release.title.split())).lower()
        self.assertEqual(expected_name, produced_artist.name)
        self.assertEqual(expected_url, produced_artist.url)
        self.assertEqual('compilation', produced_artist.type)
        self.assertEqual(0, len(produced_artist.artistvendor_set.all()))
        self._check_commons(produced_artist)
    
    def test_link(self):
        local_artist = Artist.objects.create(pk=56)
        artist_mapper = ArtistMapper(vendor=self.idol_vendor, delivery=self.delivery)
        produced_artist = artist_mapper.link(mdx_artist=local_artist)
        self.assertEqual(local_artist, produced_artist)
        self._check_artist_vendor(produced_artist)

        
class LabelMapperTest(TestCase):

    def setUp(self):
        self.delivery = IDOLDelivery(TEST_COMMON + '/batch1/3596971288129')
        self.vendor = Vendor.objects.create(pk=self.delivery.vendor_id)

    def _check_label_vendor(self, produced_label):
        label_vendor = produced_label.labelvendor_set.get(vendor=self.vendor)
        self.assertEqual(self.vendor, label_vendor.vendor)
        self.assertEqual(self.delivery.label.pk, label_vendor.external_label_id)
       
    def test_init(self):
        self.assert_(LabelMapper(vendor=self.vendor, delivery=self.delivery))
    
    def test_create(self):
        mapper = LabelMapper(delivery=self.delivery, vendor=self.vendor)
        produced_label = mapper.create()
        self.assertEqual(self.delivery.label.name, produced_label.name)
        self.assertEqual(date.today(), produced_label.created)
        self._check_label_vendor(produced_label)
        
    def test_link(self):
        local_label = Label.objects.create(name='label_name')
        mapper = LabelMapper(delivery=self.delivery, vendor=self.vendor)
        produced_label = mapper.link(mdx_label=local_label)
        self.assertEqual(local_label, produced_label)
        self._check_label_vendor(produced_label)

            
 
class ReleaseMapperTest(TestCase):

    def setUp(self):
        self.delivery = IDOLDelivery(TEST_COMMON + '/batch1/3596971288129')
        self.vendor = Vendor.objects.create(pk=self.delivery.vendor_id)
        self.label = Label.objects.create(name='aaaa')
        self.artist = Artist.objects.create(name='aaaa')
        self.prix = Prix.objects.create(code=price_dic['B0'])
        self.release_mapper = ReleaseMapper(self.delivery, artist=self.artist, label=self.label, vendor=self.vendor)

    def _check_notes(self, produced_album):
        notes = (',').join([style.name for style in self.delivery.styles])
        notes = notes + " - IDOL-ID: %s" % (str(self.delivery.release.pk),)
        self.assertEqual(notes, produced_album.notes)

    def test_create(self):
        produced_album = self.release_mapper.create()
        self.assertEqual(self.delivery.release.title, produced_album.title)
        self.assertEqual(self.delivery.release.publish_date_digital, produced_album.publish_date_digital)
        self.assertEqual(self.delivery.release.publish_date, produced_album.publish_date)
        self.assertEqual(','.join(self.delivery.release.territories), produced_album.territories)
        self.assertEqual(self.label, produced_album.label)
        self.assertEqual(self.artist, produced_album.artist)
        self.assertEqual(self.prix, produced_album.prix)
        self.assertEqual(date.today(), produced_album.created)
        self.assertEqual('boutique', produced_album.domain)
        self.assertEqual(self.vendor, produced_album.vendor)
        self.assertEqual(self.delivery.release.upc, produced_album.upc)
        self._check_notes(produced_album)
        album_vendor = produced_album.albumvendor_set.get(vendor=self.vendor)
        self.assertEqual(self.delivery.release.pk, album_vendor.external_album_id)
        

class ReleaseWithWorldWideTerritoryMapperTest(TestCase):

    fixtures = ['iso.json',]

    def setUp(self):
        self.delivery = IDOLDelivery(TEST_COMMON + '/batch_similar/3307516706028')
        self.vendor = Vendor.objects.create(pk=self.delivery.vendor_id)
        self.label = Label.objects.create(name='aaaa')
        self.artist = Artist.objects.create(name='aaaa')
        self.prix = Prix.objects.create(code=price_dic['B0'])
        self.release_mapper = ReleaseMapper(self.delivery, artist=self.artist, label=self.label, vendor=self.vendor)

    def _build_expected_territories(self):
        country_codes = CountryIsoEn.objects.all().values_list('code')
        return set([code for (code,) in country_codes])

    def test_create(self):
        produced_album = self.release_mapper.create()
        self.assertEqual(self._build_expected_territories(), set(produced_album.territories.split(',')))
        
        

class TrackMapperTest(TestCase):

    def setUp(self):
        self.vendor = Vendor.objects.create(pk=1)
        self.artist = Artist.objects.create(name='artist_name')
        self.album = Album.objects.create(title='album_title')
        self.prix = Prix.objects.create(code='PCFT')
        
    def test_simple(self):
        #pdb.set_trace()
        delivery_track = DeliveryTrack(pk=1, title='track_title', 
                                       bundle_only=True, isrc="12CVF56", 
                                       track_number=54, disc_number=2, price='S2',
                                       author='Gerard Lambert', composer='toto la praline')
        track_mapper = TrackMapper(album=self.album, delivery_track=delivery_track)
        produced_track = track_mapper.create()
        self.assertEqual(self.album, produced_track.album)
        self.assertEqual(delivery_track.title, produced_track.title)
        self.assertEqual(False, produced_track.vente_autitre)
        self.assertEqual(True, produced_track.vente_alalbum)
        self.assertEqual(delivery_track.isrc, produced_track.isrc)
        self.assertEqual(delivery_track.track_number, produced_track.track_number)
        self.assertEqual(delivery_track.disc_number, produced_track.disc_number)
        self.assertEqual(price_dic[delivery_track.price], produced_track.prix.code)
        self.assertEqual(delivery_track.author, produced_track.author)
        self.assertEqual(delivery_track.composer, produced_track.composer)
        produced_trackvendor = produced_track.trackvendor_set.get()
        self.assertEqual(delivery_track.pk, produced_trackvendor.external_track_id)

    def test_bundle_only(self):
        delivery_track = DeliveryTrack(pk=1, title='track_title', 
                                            bundle_only=False, isrc="12CVF56", 
                                            track_number=54, disc_number=2, price='S2',
                                       author='', composer='')
        track_mapper = TrackMapper(album=self.album, delivery_track=delivery_track)
        produced_track = track_mapper.create()
        self.assertEqual(self.album, produced_track.album)
        self.assertEqual(delivery_track.title, produced_track.title)
        self.assertEqual(True, produced_track.vente_autitre)
        self.assertEqual(True, produced_track.vente_alalbum)
        self.assertEqual(delivery_track.isrc, produced_track.isrc)
        self.assertEqual(delivery_track.track_number, produced_track.track_number)
        self.assertEqual(delivery_track.disc_number, produced_track.disc_number)
        produced_trackvendor = produced_track.trackvendor_set.get()
        self.assertEqual(delivery_track.pk, produced_trackvendor.external_track_id)
        
    def tearDown(self):
        pass
        
        
class AudioFileMapperTest(TestCase):

    def setUp(self):
        self.delivery = IDOLDelivery(TEST_COMMON + '/batch2/3300450000368')
        self.disc = Disc.objects.create(status=u'default')
        self.delivery_audiofile = self.delivery.tracks[0].audio_files['normal']
        
    def test_main(self):
        artist = Artist.objects.create(name='tutu')
        album = Album.objects.create(title='tata', artist=artist)
        track = Track.objects.create(title='my_track', album=album)
        audiofile_mapper = AudioFileMapper(delivery_audiofile=self.delivery_audiofile, track=track, disc=self.disc)
    
        filename = artist.name + '_' + album.title + '_' + track.title + '.mp3'
        path = "/albums/%s/mp3/%s" % (album.pk, filename)
        produced_audiofile = audiofile_mapper.create()
        self.assertEqual(path, produced_audiofile.path)
        self.assertEqual('piste', produced_audiofile.content)
        self.assertEqual('mp3', produced_audiofile.format)
        self.assertEqual(self.disc, produced_audiofile.disc)
        self.assertEqual(114, produced_audiofile.duration)
        self.assertEqual(8149497, produced_audiofile.size)
        self.assertEqual(320, produced_audiofile.bitrate)
        
    def test_filename_remove_spaces(self):
        artist = Artist.objects.create(name='tutu tutu')
        album = Album.objects.create(title='tata tata', artist=artist)
        track = Track.objects.create(title='my track', album=album)
        path = "/albums/%s/mp3/tutu_tutu_tata_tata_my_track.mp3" % (album.pk,)
        audiofile_mapper = AudioFileMapper(delivery_audiofile=self.delivery_audiofile, track=track, disc=self.disc)
        produced_audiofile = audiofile_mapper.create()
        self.assertEqual(path, produced_audiofile.path)

    def test_filename_remove_non_ascii(self):
        artist = Artist.objects.create(name='tutu tutu')
        album = Album.objects.create(title=u'téta tata', artist=artist)
        track = Track.objects.create(title='my track', album=album)
        path = "/albums/%s/mp3/tutu_tutu_teta_tata_my_track.mp3" % (album.pk,)
        audiofile_mapper = AudioFileMapper(delivery_audiofile=self.delivery_audiofile, track=track, disc=self.disc)
        produced_audiofile = audiofile_mapper.create()
        self.assertEqual(path, produced_audiofile.path)

class ImageFileMapperTest(TestCase):

    def setUp(self):
        self.delivery = IDOLDelivery(TEST_COMMON + '/batch2/3300450000368')
        self.disc = Disc.objects.create(status=u'default')
        self.album = Album.objects.create(title='album_title')
        self.name = "image_file"
        self.format = "jpg"
        self.size=12
        self.width=63
        self.height=63
        self.usage="cover63"

    def test_success(self):
        expected_path = image_path = "/albums/%s/images/%s.%s" % (self.album.pk, self.name, self.format)
        imagefile_mapper = ImageFileMapper(disc=self.disc, album=self.album,
                                           path=expected_path, format=self.format,
                                           size=self.size, width=self.width, 
                                           height=self.height, usage=self.usage)
        image_file = imagefile_mapper.create()
        self.assertEqual(self.album, image_file.album)
        self.assertEqual(self.disc, image_file.disc)
        self.assertEqual(expected_path, image_file.path)
        self.assertEqual(self.width, image_file.width)
        self.assertEqual(self.height, image_file.height)
        self.assertEqual(self.format, image_file.format)
        self.assertEqual(self.usage, image_file.usage)

        
