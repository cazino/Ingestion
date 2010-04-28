import pdb
import os, shutil
from django.test import TestCase
from django.test.client import Client
from django.http import HttpRequest, QueryDict
from mp3.main.models import  Vendor, Disc, Album, Prix, Artist
from mp3.ingestion.ingestion_localsettings import TEST_COMMON
from mp3.ingestion.views import BatchShow, BatchProcessor
from mp3.ingestion.models import IDOLDelivery



class BatchShowTest(TestCase):

    def setUp(self):
        self.batch_path = TEST_COMMON + '/batch_delete'

    def test(self):
        request = HttpRequest()
        request.method= 'GET'
        request.GET = QueryDict('batchpath=%s' % (self.batch_path))
        batch_show = BatchShow(request)
        self.assertEqual([IDOLDelivery(self.batch_path + '/3300450000368'),], batch_show.bad_deliveries)


class BatchPocessorTest(TestCase):
    """
    Abstract base class 
    Copy the content of the batch path in a tmp directory
    Erase that directory after the test
    """
    def setUp(self):
        self.tmp_batch_path = TEST_COMMON + '/tmp'
        shutil.copytree(self.batch_path, self.tmp_batch_path)
    
    def tearDown(self):
        if os.path.exists(self.tmp_batch_path):
            shutil.rmtree(self.tmp_batch_path)
    
        
class BatchPocessorCompilTest(BatchPocessorTest):

    def setUp(self):
        self.batch_path = TEST_COMMON + '/batch_compil3'
        super(BatchPocessorCompilTest, self).setUp()

    def test(self):
        Vendor.objects.create(pk=256)
        disc = Disc.objects.create(status='default')
        prix = Prix.objects.create(code='PCFA')
        request = HttpRequest()
        request.method= 'POST'
        query_dict = QueryDict('batchpath=%s' % (self.tmp_batch_path)).copy()
        query_dict.update({'label-0-release_title_hidden' : u"N'ayons pas peur! - Hommage \xe0 l'homme de paix",
                           'release-0-pk' : u'1591',
                           'release-0-artist_name_hidden' : u'Varioust Artists',
                           'label-0-mdx_label_id': u'2345',
                           'release-TOTAL_FORMS' : u'1',
                           'label-0-name_hidden' : u'Ad Vitam records',
                           'label-INITIAL_FORMS' : u'1',
                           'release-INITIAL_FORMS': u'1',
                           'release-0-label_name_hidden': u'Ad Vitam records',
                           'label-0-name_auto' : u'AD VITAM Records',
                           'label-TOTAL_FORMS': u'1',
                           'label-0-pk': u'84', 
                           'artist-TOTAL_FORMS': u'0',
                           'label-0-create': u'1',
                           'release-0-title_hidden': u"N'ayons pas peur! - Hommage \xe0 l'homme de paix",
                           'artist-INITIAL_FORMS': u'0'
                           })
        request.POST = query_dict
        batch_process = BatchProcessor(request)
        batch_process.process()
        album = Album.objects.get()
        artist = Artist.objects.get()
        self.assertEqual('compilation', artist.type)
        
        





    







