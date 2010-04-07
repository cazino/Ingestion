import shutil, os, Image

from django.db.models import ObjectDoesNotExist
from django.test import TestCase, TransactionTestCase
from mp3 import metadata
from mp3.main.models import Artist, Vendor, ArtistVendor, Label, Album, Disc, Track, ImageFile, Prix
from mp3.main.main_localsettings import ALBUMS_DIRECTORY
from mp3.ingestion.models import IDOLDelivery, DeliveryTrack, DeliveryAudioFile, DeliveryImage
from mp3.ingestion.forms import ArtistForm, LabelForm, ReleaseForm
from mp3.ingestion.processors import ReleaseProcessor, TrackProcessor, AudioFileProcessor, ImageFileProcessor
from mp3.ingestion.processors import  ArtistProcessor, LabelProcessor
from mp3.main import main_localsettings
from mp3.ingestion.ingestion_localsettings import TEST_DATA, TEST_COMMON,  ADMIN_LABEL_URL
from mp3.ingestion.ingestion_localsettings import ADMIN_ALBUM_URL, ADMIN_ARTIST_URL
from mp3.ingestion.metadata.idol_prices import price_dic
from mp3.ingestion.metadata import naming
import datapaths


import pdb 

TEST_PROCESSOR = TEST_DATA + '/testprocessor'


class WithImageTest(TransactionTestCase):

    def check_album_images(self, album, disc):
        for size in metadata.IMAGES_SIZES:
            image = ImageFile.objects.get(album=album, disc=disc, 
                                          width=size, height=size,
                                          usage="cover%s" %(size))
            filepath = image.full_path()
            self.assertTrue(os.path.exists(filepath))
            self.assertEqual(os.path.getsize(filepath), image.size)
            im_obj = Image.open(filepath)
            (width, height) = im_obj.size
            self.assertEqual(width, image.width)
            self.assertEqual(height, image.height)


class ArtistProcessorTest(TransactionTestCase):
    
    def setUp(self):
        self.delivery = IDOLDelivery(TEST_COMMON + '/batch1/3596971288129')
        self.vendor = Vendor.objects.create(pk=self.delivery.vendor_id)
        self.artist_name = self.delivery.artist.name
        self.url = 'wax-tailor'
        self.pk = self.delivery.artist.pk

    def _report_check(self, expected_artist, report):
        # Report
        self.assertTrue(report.success)
        expected_admin_url = ADMIN_ARTIST_URL + str(expected_artist.pk)
        self.assertEqual(expected_admin_url, report.admin_url)
        self.assertEqual(expected_artist.name, report.name)
        self.assertEqual(expected_artist.pk, report.mdx_id)
        idol_id = expected_artist.artistvendor_set.get().external_artist_id
        self.assertEqual(idol_id, report.external_id)

    def test_succeed_create(self):
        artist_form = ArtistForm(data={'pk': self.pk, 'create': 1, 'name_hidden': self.artist_name, 
                                  'release_title_hidden': 'release_title', 'url': self.url})
        artist_form.is_valid()
        artist_processor = ArtistProcessor(delivery=self.delivery, artist_form=artist_form, vendor=self.vendor)
        produced_artist = artist_processor.build()
        expected_artist = Artist.objects.get(artistvendor__external_artist_id=self.pk)
        self.assertEquals(expected_artist, produced_artist)
        self. _report_check(expected_artist, artist_form.report)       

    def test_succeed_link(self):
        local_artist = Artist.objects.create(name='artist_name')
        artist_form = ArtistForm(data={'pk': self.pk, 'create': 0, 'name_hidden': self.artist_name, 
                                       'release_title_hidden': 'release_title','mdx_artist_id': local_artist.pk})
        artist_form.is_valid()
        artist_processor = ArtistProcessor(delivery=self.delivery, artist_form=artist_form, vendor=self.vendor)
        artist  = artist_processor.build()
        self.assertEquals(local_artist, artist)
        self. _report_check(local_artist, artist_form.report)
        
    def test_fail_incorrect_pk_type(self):
        delivery_artist = self.delivery.artist
        delivery_artist.pk = 'pk'
        artist_form = ArtistForm(data={'pk': self.pk, 'create': 1, 'name_hidden': self.artist_name, 
                                       'url': self.url, 'release_title_hidden': self.delivery.release.title,})
        artist_form.is_valid()
        artist_processor = ArtistProcessor(delivery=self.delivery, artist_form=artist_form, vendor=self.vendor)
        artist  = artist_processor.build()
        self.assertEquals(None, artist)
        self.assertFalse(artist_form.report.success)
        self.assertTrue(artist_form.report.error)


        
class LabelProcessorTest(TransactionTestCase):

    def setUp(self):
        self.delivery = IDOLDelivery(TEST_COMMON + '/batch1/3596971288129')
        self.vendor = Vendor.objects.create(pk=self.delivery.vendor_id)

    def _report_check(self, expected_label, label_form):
        # Report%
        self.assertTrue(label_form.report.success)
        expected_admin_url = ADMIN_LABEL_URL  + str(expected_label.pk)
        self.assertEqual(expected_admin_url, label_form.report.admin_url)
        self.assertEqual(expected_label.name, label_form.report.name)
        self.assertEqual(expected_label.pk, label_form.report.mdx_id)
        idol_id = expected_label.labelvendor_set.get().external_label_id
        self.assertEqual(idol_id, label_form.report.external_id)
                
    def test_create_label(self):
        label_form = LabelForm(data={'pk': self.delivery.label.pk, 'create': 1, 
                                'name_hidden': 'label_name', 'release_title_hidden': 'release_title'})
        label_form.is_valid()
        label_processor = LabelProcessor(delivery=self.delivery, label_form=label_form, vendor=self.vendor)
        produced_label = label_processor.build()
        expected_label = Label.objects.get(labelvendor__external_label_id=self.delivery.label.pk)
        self.assertEqual(expected_label, produced_label)
        self._report_check(expected_label, label_form)
        
    def test_link_label(self):
        label_id = 12
        local_label = Label.objects.create(pk=label_id)
        label_form = LabelForm({'pk': self.delivery.label.pk, 'create': 0, 
                                'name_hidden': 'label_name', 'release_title_hidden': 'release_title',
                                'mdx_label_id': label_id})
        label_form.is_valid()
        label_processor = LabelProcessor(delivery=self.delivery, label_form=label_form, vendor=self.vendor)
        self.assertEqual(local_label, label_processor.build())
        self._report_check(local_label, label_form)

    def test_fail_incorrect_pk_type(self):
        delivery_label = self.delivery.label
        delivery_label.pk = 'pk'
        label_form = LabelForm(data={'pk': delivery_label.pk, 'create': 1, 
                                'name_hidden': delivery_label.name, 'release_title_hidden': 'release_title'})
        label_form.is_valid()
        label_processor = LabelProcessor(delivery=self.delivery, label_form=label_form, vendor=self.vendor)
        label = label_processor.build()
        self.assertEquals(None, label)
        self.assertFalse(label_form.report.success)
        self.assertTrue(label_form.report.error)


class AbstractReleaseProcessorTest(WithImageTest):

    def setUp(self):
        init_prices()
        # Copy delivery in a special directory an init delivery_object and delivery_processor
        delivery_upc = os.path.split(self.original_delivery_path)[1]
        self.delivery_path = os.path.join(TEST_PROCESSOR, delivery_upc)
        shutil.copytree(self.original_delivery_path, self.delivery_path)
        # Init Delivery
        self.delivery = IDOLDelivery(self.delivery_path)       
        # Init database
        self.disc = Disc.objects.create(status='default', path='disk1')
        self.vendor = Vendor.objects.create(pk=self.delivery.vendor_id)
        self.label = Label.objects.create(pk=self.delivery.label.pk)
        # Init the 'albums' directory
        main_localsettings.DISCOTHEQUE_BASEPATH = TEST_PROCESSOR
        os.mkdir(self.disc.full_path())
        self.album_directory = os.path.join(self.disc.full_path(), ALBUMS_DIRECTORY)
        os.mkdir(self.album_directory)

    def _check_album_report(self, expected_album, report):
        self.assertTrue(report.success)
        expected_admin_url = ADMIN_ALBUM_URL + str(expected_album.pk)
        self.assertEqual(expected_admin_url, report.admin_url)
        self.assertEqual(expected_album.pk, report.mdx_id)
        self.assertEqual(expected_album.albumvendor_set.get().external_album_id, report.external_object_id)
        
    def _check_artist_report(self, artist, report):
        self.assertTrue(report.success)
        expected_admin_url = ADMIN_ARTIST_URL + str(artist.pk)
        self.assertEqual(expected_admin_url, report.admin_url)
        self.assertEqual(artist.pk, report.mdx_id)

    def tearDown(self):
        # Clean all the directories
        for directory_path in (self.delivery_path, self.disc.full_path()):
            if os.path.exists(directory_path):
                shutil.rmtree(directory_path)        

class ReleaseProcessorTest(AbstractReleaseProcessorTest):

    def __init__(self, methodName):
        super(ReleaseProcessorTest, self).__init__(methodName)
        self.original_delivery_path = os.path.join(TEST_COMMON, 'batch1/3596971288129')

    def setUp(self):
        super(ReleaseProcessorTest, self).setUp()
        self.artist = Artist.objects.create(pk=self.delivery.artist.pk) 
        
    def test_build(self):
        release_form = ReleaseForm({'pk': self.delivery.release.pk})
        release_form.is_valid()
        release_processor = ReleaseProcessor(delivery=self.delivery, release_form=release_form, 
                                             artist=self.artist, label=self.label,
                                             disc=self.disc, vendor=self.vendor)
        produced_release = release_processor.build()
        expected_release = Album.objects.get(albumvendor__external_album_id=self.delivery.release.pk)
        self.assertEqual(expected_release, produced_release)
        # Test audiofiles
        produced_tracks = produced_release.track_set.all()
        produced_audiofiles = []
        for track in produced_tracks:
            produced_audiofiles.extend(list(track.audiofile_set.all())) 
        delivery_audiofiles = self.delivery.audiofiles()
        self.assertEqual(len(delivery_audiofiles), len(produced_audiofiles))
        for audiofile in produced_audiofiles:
            self.assertTrue(os.path.exists(audiofile.full_path()))
        # Test images
        self.check_album_images(produced_release, self.disc)
        # No Files Left   
        self.assertFalse(os.path.exists(self.delivery_path))
        # Reports
        self._check_album_report(expected_release, release_form.report)


    def test_annuler(self):
        release_form = ReleaseForm(data={'pk': self.delivery.release.pk, 'annuler': True})
        release_form.is_valid()
        release_processor = ReleaseProcessor(delivery=self.delivery, release_form=release_form, 
                                             artist=self.artist, label=self.label,
                                             disc=self.disc, vendor=self.vendor)
        release_processor.remove()
        self.assertRaises(Album.DoesNotExist, Album.objects.get,
                          albumvendor__external_album_id=self.delivery.release.pk)
        self.assertFalse(os.path.exists(self.delivery.path))
        self.assertTrue(release_form.report.success)

    def test_crash_bad_deliverytrack(self):
        from django.conf import settings
        release_form = ReleaseForm({'pk': self.delivery.release.pk, 'title_hidden': 'release_title',
                                    'artist_name_hidden': 'artist', 'label_name_hidden': 'label'})
        release_form.is_valid()
        # Modify the delivery in order to crash
        self.delivery.tracks[1].pk = 'aaa'
        release_processor = ReleaseProcessor(delivery=self.delivery, release_form=release_form, 
                                             artist=self.artist, label=self.label, disc=self.disc,
                                             vendor=self.vendor)
        # Test
        # No Album
        self.assertEqual(None, release_processor.build())
        self.assertFalse(self.artist.album_set.all())
        # No tracks
        for (index,track) in enumerate(self.delivery.tracks):
            if index != 1:
                self.assertRaises(Track.DoesNotExist, Track.objects.get, trackvendor__external_track_id=track.pk)
        # No imagefile
        self.assertEqual(0, ImageFile.objects.count())
        # No Files
        self.assertFalse(os.listdir(self.album_directory))
        # Error in the release_form
        self.assertFalse(release_form.report.success)
        self.assertTrue(release_form.report.error)
        

    def test_remove(self):
        release_form = ReleaseForm({'pk': self.delivery.release.pk, 'remove': True})
        release_form.is_valid()
        release_processor = ReleaseProcessor(delivery=self.delivery, release_form=release_form, 
                                             artist=self.artist, label=self.label,
                                             disc=self.disc, vendor=self.vendor)
        release_processor.remove()
        self.assertFalse(os.listdir(self.album_directory))


class ReleaseProcessorCompilTest(AbstractReleaseProcessorTest):

    def __init__(self, methodName):
        super(ReleaseProcessorCompilTest, self).__init__(methodName)
        self.original_delivery_path = datapaths.compil1_path

    def setUp(self):
        super(ReleaseProcessorCompilTest, self).setUp()

    def test_build_(self):
        release_form = ReleaseForm({'pk': self.delivery.release.pk})
        release_form.is_valid()
        release_processor = ReleaseProcessor(delivery=self.delivery, release_form=release_form, 
                                             label=self.label, disc=self.disc, vendor=self.vendor)
        produced_release = release_processor.build()
        expected_release = Album.objects.get(albumvendor__external_album_id=self.delivery.release.pk)
        # Test album
        self.assertEqual(expected_release, produced_release)
        produced_abumvendor = produced_release.albumvendor_set.get()
        # Test album_vendor
        self.assertEqual(self.delivery.release.pk, produced_abumvendor.external_album_id)
        self.assertEqual(self.vendor, produced_abumvendor.vendor)
        # Test artist
        produced_artist = produced_release.artist
        self.assertEqual(naming.COMPIL_FLAG, produced_artist.type)
        self.assertEqual("%s %s" % (produced_release.title, naming.COMPIL_POSTFIX), produced_artist.name)
        # No Files Left   
        self.assertFalse(os.path.exists(self.delivery_path))
        # Reports
        self._check_album_report(expected_release, release_form.report)
        self._check_artist_report(produced_artist, release_form.artist_report)
        expected_admin_artist_url = ADMIN_ARTIST_URL + str(produced_release.artist.pk)
        self.assertEqual(expected_admin_artist_url, release_form.report.admin_artist_url)

        
class TrackProcessorTest(TestCase):

    def setUp(self):
        init_prices()
        self.discpath = os.path.join(TEST_PROCESSOR, 'disc')
        audiofile_directory = os.path.join(TEST_COMMON, 'batch1/3596971288129')
        piste_filename = 'FR2DK0680020.mp3'
        extrait_filename = 'FR2DK0680020_preview.mp3'
        piste_filepath = os.path.join(audiofile_directory, piste_filename)
        extrait_filepath = os.path.join(audiofile_directory, extrait_filename)
        self.piste_filepath = os.path.join(TEST_PROCESSOR, piste_filename)
        self.extrait_filepath = os.path.join(TEST_PROCESSOR, extrait_filename)
        shutil.copy(piste_filepath, self.piste_filepath)
        shutil.copy(extrait_filepath, self.extrait_filepath)
        main_localsettings.DISCOTHEQUE_BASEPATH = TEST_PROCESSOR
        self.disc = Disc.objects.create(path='disc1')

    def test(self):
        # Database initialisation        
        vendor = Vendor.objects.create(pk=1)
        artist = Artist.objects.create(name='artist_name')
        album = Album.objects.create(title='album_title', artist=artist, vendor=vendor)
        
        # Files initialisation
        piste_directory = os.path.join(album.full_path(self.disc), 'mp3')
        extrait_directory = os.path.join(album.full_path(self.disc), 'samples')
        os.makedirs(piste_directory)
        os.makedirs(extrait_directory)
        # Delvery data an processor initialisation
        delivery_audiofile_piste = DeliveryAudioFile(format='mp3', content='piste', path=self.piste_filepath)
        delivery_audiofile_extrait = DeliveryAudioFile(format='mp3', content='extrait', path=self.extrait_filepath)
        delivery_track_title = 'track_title'
        delivery_track = DeliveryTrack(pk=1, track_number=1, title=delivery_track_title, 
                                       audio_files={'normal': delivery_audiofile_piste,
                                                    'sample': delivery_audiofile_extrait},
                                       price='S10', author='', composer='')
        # Expected filepath
        base_filename = "%s_%s_%s" % (artist.name, album.title, delivery_track_title)
        piste_filename = base_filename + '.mp3'
        extrait_filename = base_filename + '_sample.mp3'
        piste_filepath = os.path.join(piste_directory, piste_filename)
        extrait_filepath = os.path.join(extrait_directory, extrait_filename)
        # Process
        track_processor = TrackProcessor(delivery_track=delivery_track, album=album, disc=self.disc)
        track = track_processor.build()
        self.assert_(track)
        for audiofile in track.audiofile_set.all():
            self.assertTrue(os.path.exists(audiofile.full_path()))
        
    def tearDown(self):
        for filepath in (self.piste_filepath, self.extrait_filepath):
            if os.path.exists(filepath):
                os.remove(filepath)
        if os.path.exists(self.disc.full_path()):
            shutil.rmtree(self.disc.full_path())
            
            
class AudioFileProcessorTest(TestCase):

    def setUp(self):
        # File initialization
        file_path = os.path.join(TEST_COMMON, 'batch1/3596971288129/FR2DK0680020.mp3')
        self.file_path = os.path.join(TEST_PROCESSOR, 'FR2DK0680020.mp3')
        shutil.copy(file_path, self.file_path)
        self.disc = Disc.objects.create(path='disc')
        
    def test_process_audiofile(self):
        # Database initialisation        
        artist = Artist.objects.create(name='artist_name')
        album = Album.objects.create(title='album_title', artist=artist)
        track = Track.objects.create(title='track_title', album=album)
        # Delvery data an processor initialisation
        delivery_audiofile = DeliveryAudioFile(format='mp3', content='piste', path=self.file_path)
        audiofile_processor = AudioFileProcessor(disc=self.disc, track=track, delivery_audiofile=delivery_audiofile)
        # Expected filepath
        expected_filename = "%s_%s_%s.mp3" % (artist.name, album.title, track.title)
        expected_audiofile_directory = os.path.join(album.full_path(self.disc), 'mp3')
        expected_audiofile_path = os.path.join(expected_audiofile_directory, expected_filename)
        #Build the directory
        if not os.path.exists(expected_audiofile_directory):
            os.makedirs(expected_audiofile_directory)
        audiofile_processor.build()
        self.assertTrue(os.path.exists(expected_audiofile_path))

    def test_process_audiofile_extrait(self):
        # Database initialisation        
        artist = Artist.objects.create(name='artist_name')
        album = Album.objects.create(title='album_title', artist=artist)
        track = Track.objects.create(title='track_title', album=album)
        # Delvery data an processor initialisation
        delivery_audiofile = DeliveryAudioFile(format='mp3', content='extrait', path=self.file_path)
        audiofile_processor = AudioFileProcessor(disc=self.disc, track=track, delivery_audiofile=delivery_audiofile)
        # Expected filepath
        expected_filename = "%s_%s_%s.mp3" % (artist.name, album.title, track.title)
        expected_audiofile_directory = os.path.join(album.full_path(self.disc), 'samples')
        expected_audiofile_path = os.path.join(expected_audiofile_directory, expected_filename)
        #Build the directory
        if not os.path.exists(expected_audiofile_directory):
            os.makedirs(expected_audiofile_directory)
        audiofile_processor.build()
        self.assertTrue(os.path.exists(expected_audiofile_path))
        
    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
        if os.path.exists(self.disc.full_path()):
            shutil.rmtree(self.disc.full_path())
        

class ImageFileProcessorTest(WithImageTest):

    def setUp(self):
        # File initialization
        main_localsettings.DISCOTHEQUE_BASEPATH = TEST_PROCESSOR
        ima_name = '3596971288129.jpg'
        file_path = os.path.join(TEST_COMMON, 'batch1/3596971288129', ima_name)
        self.file_path = os.path.join(main_localsettings.DISCOTHEQUE_BASEPATH, ima_name)
        shutil.copy(file_path, self.file_path)
        self.delivery_image = DeliveryImage(name=ima_name, path=self.file_path, format='jpg')
        self.disc = Disc.objects.create(status='default', path='disk1')
        self.album = Album.objects.create(title='album_title')
        os.makedirs(os.path.join(self.album.full_path(self.disc), main_localsettings.IMAGES_DIRECTORY))

    def test_process(self):
        ima_processor = ImageFileProcessor(delivery_image=self.delivery_image, album=self.album, disc=self.disc)
        images = ima_processor.build()
        self.check_album_images(self.album, self.disc)
   
    def tearDown(self):
        to_delete_files = (self.file_path, self.disc.full_path())
        for path in to_delete_files:
            if os.path.exists(path):
                if os.path.isfile(path):
                    os.remove(path)
                else:
                    shutil.rmtree(path)
        
    
    
        
def init_prices():
    for code in list(set(price_dic.values())):
        Prix.objects.create(code=code)
