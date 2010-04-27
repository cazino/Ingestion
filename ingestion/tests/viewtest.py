from django.test import TestCase
from django.http import HttpRequest, QueryDict
from mp3.ingestion.ingestion_localsettings import TEST_COMMON
from mp3.ingestion.views import BatchShow
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






    







