# -*- coding: utf-8 -*-
import os, copy
from datetime import date, datetime
from django.test import TestCase
from mp3.main.models import Artist, Vendor, ArtistVendor, Label
from mp3.ingestion.models import IDOLDelivery, DeliveryRelease, Batch
from mp3.ingestion.models import DeliveryArtist, DeliveryTrack, DeliveryAudioFile
from mp3.ingestion.models import DeliveryImage, DeliveryLabel, DeliveryAudioFiles, DeliveryStyle
from mp3.ingestion.mappers import ArtistMapper, LabelMapper, ReleaseMapper
from mp3.ingestion.ingestion_localsettings import TEST_COMMON
import pdb

class TestDeliveryRelease(TestCase):

    def test_wrong_keyword(self):
        self.assertRaises(TypeError, DeliveryRelease, prout=3)
        
    def test_territories_is_a_tuple(self):
        self.assertRaises(TypeError, DeliveryRelease, territories=['aa'])
        
    def test_equality(self):
        release1 = DeliveryRelease(pk=1, title='aa')
        release2 = DeliveryRelease(pk=1, title='aa')
        self.assertEqual(release1, release2)

    def test_hash(self):
        release1 = DeliveryRelease(pk=1, title='aa')
        self.assert_(hash(release1))
    
    def test_hash_equal(self):
        release1 = DeliveryRelease(pk=1, title='aa')
        release2 = DeliveryRelease(pk=1, title='aa')
        self.assertEqual(hash(release1), hash(release2))
    
    def test_hash_equal_on_same_object(self):
        release1 = DeliveryRelease(pk=1, title='aa')
        self.assertEqual(hash(release1), hash(release1))
        
    
    
class TestDeliveryArtist(TestCase):

    def test_exception(self):
        self.assertRaises(TypeError, DeliveryArtist, prout=3)
        
    def test_equality(self):
        artist1 = DeliveryArtist(pk=1, name='aa')
        artist2 = DeliveryArtist(pk=1, name='aa')
        self.assertEqual(artist1, artist2)

    def test_equal(self):
        artist = DeliveryArtist(pk=1, name='aa')
        release = DeliveryRelease(pk=1, title='aa')
        artist.release = release
        release.artist = artist
        self.assert_(artist == artist)

        
class TestDeliveryStyle(TestCase):

    def test_exception(self):
        self.assertRaises(TypeError, DeliveryStyle, prout=3)

    def test_equality(self):
        style1 = DeliveryStyle(name='aa')
        style2 = DeliveryStyle(name='aa')
        self.assertEqual(style1, style2)


class TestDeliveryTrack(TestCase):

    def test_exception(self):
        self.assertRaises(TypeError, DeliveryTrack, prout=3)
        
    def test_equality(self):
        track1 = DeliveryTrack(pk=1, title='aa')
        track2 = DeliveryTrack(pk=1, title='aa')
        self.assertEqual(track1, track2)

class TestDeliveryAudioFiles(TestCase):

    def test_exception(self):
        self.assertRaises(TypeError, DeliveryAudioFiles, prout=3)
       
    def test_wrongtype_argument(self):
        self.assertRaises(TypeError, DeliveryAudioFiles, master=3)
        
    def test_equality(self):
        audio_file1 = DeliveryAudioFile(content='extrait')
        audio_files1 = DeliveryAudioFiles(master=audio_file1)
        audio_files2 = DeliveryAudioFiles(master=audio_file1)
        self.assertEqual(audio_files1, audio_files2)
        
    def test_hash_stability(self):
        audio_file1 = DeliveryAudioFile(content='extrait')
        audio_files1 = DeliveryAudioFiles(master=audio_file1)
        self.assertEqual(hash(audio_files1), hash(audio_files1))
       
    def test_hash_equality(self):
        audio_file1 = DeliveryAudioFile(content='extrait')
        audio_files1 = DeliveryAudioFiles(master=audio_file1)
        audio_files2 = DeliveryAudioFiles(master=audio_file1)
        self.assertEqual(hash(audio_files1), hash(audio_files2))
 
    def test_hash_difference(self):
        audio_file1 = DeliveryAudioFile(content='extrait')
        audio_file2 = DeliveryAudioFile(content='piste')
        audio_files1 = DeliveryAudioFiles(master=audio_file1)
        audio_files2 = DeliveryAudioFiles(master=audio_file2)
        self.assertNotEqual(hash(audio_files1), hash(audio_files2))
        
        

    
class TestDeliveryImage(TestCase):

    def test_exception(self):
        self.assertRaises(TypeError, DeliveryImage, prout=3)
        
    def test_equality(self):
        image1 = DeliveryImage(format='extrait')
        image2 = DeliveryImage(format='extrait')
        self.assertEqual(image1, image2)


class TestDeliveryLabel(TestCase):

    def test_exception(self):
        self.assertRaises(TypeError, DeliveryLabel, prout=3)
        
    def test_equality(self):
        label1 = DeliveryLabel(name='aaa')
        label2 = DeliveryLabel(name='aaa')
        self.assertEqual(label1, label2)
        

class TestIDOLDeliveryBatch1(TestCase):
        
    def setUp(self):
        self.path = TEST_COMMON  + '/batch1/3596971288129'
        self.idol_delivery = IDOLDelivery(self.path)
        self._init_expected_data()

    def _init_expected_data(self):
        artist = DeliveryArtist(pk=12, name='Wax Tailor')
        label = DeliveryLabel(pk=103, name=u"Atmosphériques")
        territories = tuple(['AD', 'BE', 'CH', 'FR', 'GP', 'GY', 'LU', 'MC', 'MQ', 'NC', 'NL', 'PF', 'PM', 'RE', 'YT'])
        release = DeliveryRelease(pk=911, title='Hope & Sorrow', territories=territories,
                                  upc=3596971288129, publish_date=datetime.strptime('2007-04-02', '%Y-%m-%d').date(),
                                  publish_date_digital=datetime.strptime('2007-04-02', '%Y-%m-%d').date(), price=u'B0',
                                  compil=False)
        release.label = label
        release.artist = artist
        artist.release = release
        label.release = release
        self.expected_release = release
        self.expected_artist = artist
        self.expected_label = label
        

    def test_path(self):
        self.assertEqual(self.path, self.idol_delivery.path)
            
    def test_release(self):
        self.assertEqual(self.expected_release, self.idol_delivery.release)
        
    def test_artist(self):
        self.assertEqual(self.expected_artist, self.idol_delivery.artist)
    
    def test_image(self):
        ima_name = '3596971288129.jpg'
        expected_image = DeliveryImage(format='jpg', name=ima_name, 
                                       path=os.path.join(self.idol_delivery.path, ima_name))
        self.assertEqual(expected_image, self.idol_delivery.image)
        
    def test_label(self):
        self.assertEqual(self.expected_label, self.idol_delivery.label)

    def test_styles(self):
        expected_styles = [DeliveryStyle(name="Black Music : Hip Hop"), 
                           DeliveryStyle(name="Electronique : Electro Hip Hop, Abstract Hip Hop...")]
        self.assertEquals(self.idol_delivery.styles, expected_styles)
                                                                                  
    def test_track_1(self):
        expected_track = DeliveryTrack(pk=10934, title='Once upon a past', isrc='FR2DK0680010', 
                                       disc_number=1, track_number=1, price='S10', bundle_only=False,
                                       composer='Jean Christophe Le Saout',
                                       author='Nate Harrison')
        produced_track = self.idol_delivery.tracks[0]
        produced_track.audio_files = None
        self.assertEqual(expected_track, produced_track)

    def test_track_2(self):
        expected_track = DeliveryTrack(pk=10935, title='The way we lived (feat. Sharon Jones)', 
                                       isrc='FR2DK0680020', 
                                       disc_number=1, track_number=2, price='S10', bundle_only=False,
                                       composer='Jean Christophe Le Saout',
                                       author='Charlotte Savary')
        produced_track = self.idol_delivery.tracks[1]
        produced_track.audio_files = None
        self.assertEqual(expected_track, produced_track)
    
    def test_audio_file_master(self):
        self.assertEqual(None, (self.idol_delivery.tracks[0].audio_files['master']))            
            
    def test_track_numer(self):
        self.assertEqual(15, len(self.idol_delivery.tracks))
        
    def test_get_track(self):
        expected_track = DeliveryTrack(pk=10934, title='Once upon a past', isrc='FR2DK0680010', 
                                       disc_number=1, track_number=1, price='S10', bundle_only=False,
                                       author='Nate Harrison', composer='Jean Christophe Le Saout')
        produced_track = self.idol_delivery.get_track(pk=10934)
        produced_track.audio_files = None
        self.assertEqual(expected_track, produced_track)
                
    def _audiofile_1(self):
        name = 'FR2DK0680010.mp3'
        return DeliveryAudioFile(format='mp3', bitrate=320, name=name, 
                                                content='piste', duration=287, size=8149497, path=self.path+'/'+name)
    
    def _audiofile_2(self):
        name = 'FR2DK0680010_preview.mp3'
        return DeliveryAudioFile(format='mp3', bitrate=320, name=name,
                                                content='extrait', duration=30, size=2077313, path=self.path+'/'+name)
    
    def test_audio_file_normal(self):
        expected_audio_file = self._audiofile_1()
        self.assertEqual(expected_audio_file, (self.idol_delivery.tracks[0].audio_files['normal']))
        
    def test_audio_file_sample(self):
        expected_audio_file = self._audiofile_2()
        self.assertEqual(expected_audio_file, (self.idol_delivery.tracks[0].audio_files['sample']))
        
    def test_audiofile_list(self):
        produced_audiofiles = self.idol_delivery.audiofiles()
        self.assertTrue(self._audiofile_1() in produced_audiofiles)
        self.assertTrue(self._audiofile_2() in produced_audiofiles)
        
    def test_good_equality(self):
        delivery1 = self.idol_delivery
        delivery2 = self.idol_delivery
        self.assertEqual(delivery1, delivery2)

    def test_false_equality(self):
        delivery1 = self.idol_delivery
        delivery2 = IDOLDelivery(TEST_COMMON  + '/batch2/3300450000368')
        self.assertNotEqual(delivery1, delivery2)
        
    def test_hash_stability(self):
        delivery1 = self.idol_delivery
        self.assertEqual(hash(delivery1), hash(delivery1))
        
    def test_hash_equality(self):
        delivery1 = self.idol_delivery
        delivery2 = self.idol_delivery
        self.assertEqual(hash(delivery1), hash(delivery2))

    def test_equality_with_deep_copy_delivery(self):
        delivery1 = self.idol_delivery
        delivery2 = copy.deepcopy(delivery1)
        self.assertEqual(delivery1, delivery2)


class TestIDOLDeliveryBatch2(TestCase):

    def setUp(self):
        self.delivery_path = TEST_COMMON  + u'/batch2/3300450000368'
        self.idol_delivery = IDOLDelivery(self.delivery_path)
        
    def test_audio_file_normal(self):
        file_name = u'FR1Q30800001.mp3'
        expected_audio_file = DeliveryAudioFile(format=u'mp3', bitrate=320, name=file_name, path=self.delivery_path+'/'+file_name,
                                                content=u'piste', duration=114, size=8149497)
        self.assertEqual(expected_audio_file, (self.idol_delivery.tracks[0].audio_files['normal']))
        
        
class AbstractBatchTest(TestCase):

    def setUp(self):
        self.batch = Batch(self.directory)
        
class BatchComparaison(TestCase):
    
    def test_reflexif(self):
        directory = TEST_COMMON + '/batch0'
        batch = Batch(directory)
        self.assertEquals(batch, batch)
        
    def test_stability(self):
        directory = TEST_COMMON + '/batch0'
        batch1 = Batch(directory)
        batch2 = Batch(directory)
        self.assertEquals(batch1, batch2)
        
    def test_difference(self):
        directory0 = TEST_COMMON + '/batch0'
        directory1 = TEST_COMMON + '/batch1'
        batch0 = Batch(directory0)
        batch1 = Batch(directory1)
        self.assertNotEqual(batch0, batch1)     
        

class TestEmptyBatch(AbstractBatchTest):

    directory = TEST_COMMON + '/batch0'   

    def test_deliveries(self):
        self.assertEqual(set([]), self.batch.deliveries)
    
    def test_releases(self):
        self.assertEqual(set([]), self.batch.releases())
      
    def test_artists(self):
        self.assertEqual(set([]), self.batch.artists())
        
    def test_labels(self):
        self.assertEqual(set([]), self.batch.labels())
        
    def test_get_release(self):
        self.assertEqual(None, self.batch.get_release(pk=12))
        
    def test_to_formset_data(self):
        self.assertEqual({'artist-MAX_NUM_FORMS': u'0', 'artist-TOTAL_FORMS': u'0', 'artist-INITIAL_FORMS': u'0'}, self.batch.artists_formset_data())
        

class TestOneDeliveryBatch(AbstractBatchTest):

    directory = TEST_COMMON + '/batch1'
    
    def setUp(self):
        super(TestOneDeliveryBatch, self).setUp()
        self.delivery = IDOLDelivery(self.directory + '/3596971288129')
    
    def test_deliveries(self):
        self.assertEqual(set([self.delivery]), self.batch.deliveries)
    
    def test_releases(self):
        self.assertEqual(set([self.delivery.release]), self.batch.releases())
        
    def test_artists(self):
        self.assertEqual(set([self.delivery.artist]), self.batch.artists())

    def test_unknown_artists(self):
        self.assertEquals(set([self.delivery.artist]), self.batch.unknown_artists())

    def test_unknown_artists_empty(self):
        vendor = Vendor.objects.create(pk=self.delivery.vendor_id)
        artist = Artist.objects.create(name=self.delivery.artist.name)
        artist_vendor = ArtistVendor.objects.create(artist=artist, vendor=vendor, 
                                                    external_artist_id=self.delivery.artist.pk)
        self.assertEquals(set(), self.batch.unknown_artists())

    def test_labels(self):
        self.assertEqual(set([self.delivery.label]), self.batch.labels())
     
    def test_get_release_ok(self):
        self.assertEqual(self.delivery.release, self.batch.get_release(pk=911))   
    
    def test_get_release_wrong(self):
        self.assertEqual(None, self.batch.get_release(pk=91))
        
    def test_artists_formset_data(self):
        expected_data = {'artist-TOTAL_FORMS': u'1', 'artist-INITIAL_FORMS': u'0', 'artist-MAX_NUM_FORMS': u'0',
                         'artist-0-pk': u'12',
                         'artist-0-name': u'Wax Tailor'}
        self.assertEqual(expected_data, self.batch.artists_formset_data())

    """
    def test_hide_known_artist(self):
        artist = Artist.objects.create(name=self.delivery.artist.name)
        artist_vendor = ArtistVendor.objects.create(artist=artist, external_artist_id=self.delivery.artist.pk,
                                                    vendor=))
        self.assertEqual(set([self.delivery.artist]), self.batch.artists())
    """

class TestTwoDeliveryBatch(AbstractBatchTest):

    directory = TEST_COMMON + '/batch2'
    
    def setUp(self):
        super(TestTwoDeliveryBatch, self).setUp()
        self.delivery1 = IDOLDelivery(self.directory + '/3300450000368')
        self.delivery2 = IDOLDelivery(self.directory + '/3760153640047')
    
    def test_deliveries(self):
        self.assertEqual(set([self.delivery1, self.delivery2]), self.batch.deliveries)
    
    def test_releases(self):
        self.assertEqual(set([self.delivery1.release, self.delivery2.release]), self.batch.releases())
    
    def test_artists(self):
        self.assertEqual(set([self.delivery1.artist, self.delivery2.artist]), self.batch.artists())

    def test_unknown_artists(self):
        self.assertEquals(set([self.delivery1.artist,self.delivery2.artist]), self.batch.unknown_artists())

    def test_unknown_artists_one(self):
        vendor = Vendor.objects.create(pk=self.delivery1.vendor_id)
        artist = Artist.objects.create(name=self.delivery1.artist.name)
        artist_vendor = ArtistVendor.objects.create(artist=artist, vendor=vendor, 
                                                    external_artist_id=self.delivery1.artist.pk)
        self.assertEquals(set([self.delivery2.artist]), self.batch.unknown_artists())

    def test_labels(self):
        self.assertEqual(set([self.delivery1.label, self.delivery2.label]), self.batch.labels())
        
    def test_get_release_ok_1(self):
        self.assertEqual(self.delivery1.release, self.batch.get_release(pk=2867))
        
    def test_get_release_ok_2(self):
        self.assertEqual(self.delivery2.release, self.batch.get_release(pk=4007))      
    
    def test_get_release_wrong(self):
        self.assertEqual(None, self.batch.get_release(pk=91))   


class TestBatchDelete(AbstractBatchTest):
    """
    Test that the bath detects if ther is a 'update' or 'delete' flag
    """
    directory = TEST_COMMON + '/batch_delete'
    
    def setUp(self):
        super(TestBatchDelete, self).setUp()
            
    def test_good_deliveries(self):
        self.assertEqual(set(), self.batch.good_deliveries())

    def test_bad_deliveries(self):
        self.assertEqual(set([IDOLDelivery(self.directory + '/3300450000368'),]), self.batch.bad_deliveries())

class TestBatchUpdate(AbstractBatchTest):
    """
    Test that the bath detects if ther is a 'update' or 'delete' flag
    """
    directory = TEST_COMMON + '/batch_update'
    
    def setUp(self):
        super(TestBatchUpdate, self).setUp()
            
    def test_good_deliveries(self):
        self.assertEqual(set(), self.batch.good_deliveries())

    def test_bad_deliveries(self):
        self.assertEqual(set([IDOLDelivery(self.directory + '/3300450000368'),]), self.batch.bad_deliveries())
    

class TestCompil1DeliveryBatch(TestCase):

    def setUp(self):
        self.delivery_path = TEST_COMMON  + u'/batch_compil1/3700360703968'
        self.delivery = IDOLDelivery(self.delivery_path)

        # Expected datas
        artist = None
        label = DeliveryLabel(pk=44, name=u"Kitsuné")
        territories = tuple(['AD', 'AL', 'AT', 'AZ', 'BA', 'BE', 'BG', 'BY', 'CH', 'CZ', 'DE', 'DK', 'EE', 'ES', 'FI',
                             'FO', 'FR', 'GB', 'GI', 'GR', 'HR', 'HU', 'IE', 'IS', 'IT', 'LI', 'LT', 'LU', 'LV', 'MC', 
                             'MD', 'MK', 'MT', 'NL', 'NO', 'PL', 'PT', 'RO', 'RU', 'SE', 'SI', 'SJ', 'SK', 'SM', 'UA', 
                             'VA'])
        release = DeliveryRelease(pk=774, title=u'Kitsuné Maison Compilation', territories=territories,
                                  upc=3700360703968, publish_date=datetime.strptime('2005-10-03', '%Y-%m-%d').date(),
                                  publish_date_digital=datetime.strptime('2007-03-05', '%Y-%m-%d').date(), price=u'B0',
                                  compil=True)
        release.label = label
        release.artist = artist
        label.release = release
        self.expected_release = release
        self.expected_artist = artist
        self.expected_label = label
        self.expected_styles = [DeliveryStyle(name="Electronique : Electro, House"),]

    def test_artist(self):
        self.assertEqual(self.expected_artist, self.delivery.artist)

    def test_label(self):
        self.assertEqual(self.expected_label, self.delivery.label)
        
    def test_styles(self):
        self.assertEqual(self.expected_styles, self.delivery.styles)

    def test_release(self):
        self.assertEqual(self.expected_release, self.delivery.release)

    def test_track_1(self):
        expected_track = DeliveryTrack(pk=9113, title=u'Au revoir Simone - Backyards of our neighbors', 
                                       isrc='FRU700500022', 
                                       disc_number=1, track_number=1, price='S10', bundle_only=True,
                                       composer='Au revoir Simone',
                                       author='Au revoir Simone')
        produced_track = self.delivery.tracks[0]
        produced_track.audio_files = None
        self.assertEqual(expected_track, produced_track)


"""
class TestCompil2DeliveryBatch(TestCase):

    def setUp(self):
        self.delivery_path = TEST_COMMON  + u'/batch_compil2/3760153645387'
        self.delivery = IDOLDelivery(self.delivery_path)

        # Expected datas
        artist = DeliveryArtist(pk=19240, name="Dj Gero")
        label = DeliveryLabel(pk=101, name=u"Folistar")
        territories = ('WW',)
        release = DeliveryRelease(pk=3870, title=u'Auguste, Vol. 1', territories=territories,
                                  upc=3760153645387, publish_date=datetime.strptime('2008-10-29', '%Y-%m-%d').date(),
                                  publish_date_digital=datetime.strptime('2008-11-24', '%Y-%m-%d').date(), price=u'B0',
                                  compil=True)
        release.label = label
        release.artist = artist
        label.release = release
        artist.release = release
        self.expected_release = release
        self.expected_artist = artist
        self.expected_label = label       
    
    def test_artist(self):
        self.assertEqual(self.expected_artist, self.delivery.artist)

    def test_label(self):
        self.assertEqual(self.expected_label, self.delivery.label)

    
    def test_release(self):
        self.assertEqual(self.expected_release, self.delivery.release)

    def test_track_1(self):
        expected_track = DeliveryTrack(pk=9113, title=u'Au revoir Simone - Backyards of our neighbors', 
                                       isrc='FRU700500022', 
                                       disc_number=1, track_number=1, price='S10', bundle_only=True,
                                       composer='Au revoir Simone',
                                       author='Au revoir Simone')
        produced_track = self.delivery.tracks[0]
        produced_track.audio_files = None
        self.assertEqual(expected_track, produced_track)
    

    
"""
