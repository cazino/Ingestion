# -*- coding: utf-8 -*-
from datetime import datetime
from mp3.ingestion.models import DeliveryRelease, DeliveryArtist, DeliveryImage, DeliveryLabel, DeliveryAudioFile, DeliveryTrack
from mp3.ingestion.models import IDOLDelivery
"""
class DataBatch1(object):

        territories = set(['AD', 'BE', 'CH', 'FR', 'GP', 'GY', 'LU', 'MC', 'MQ', 'NC', 'NL', 'PF', 'PM', 'RE', 'YT'])
        release = DeliveryRelease(pk=911, title='Hope & Sorrow', territories=territories,
                                         upc=3596971288129,
                                         publish_date=datetime.strptime('2007-04-02', '%Y-%m-%d').date(),
                                         publish_date_digital=datetime.strptime('2007-04-02', '%Y-%m-%d').date(),)
        artist = DeliveryArtist(pk=None, name='Wax Tailor')
        image = DeliveryImage(format='jpg', name='3596971288129.jpg')
        label = DeliveryLabel(pk=103, name=u"Atmosphériques")
        
        audiofiles1 = {'master': None,
                       'normal': DeliveryAudioFile(format='mp3', bitrate=320, name='FR2DK0680010.mp3', lentype='piste'),
                       'sample': DeliveryAudioFile(format='mp3', bitrate=320, name='FR2DK0680010_preview.mp3', lentype='extrait')
                       }
        track1 = DeliveryTrack(pk=10934, title='Once upon a past', length=287, isrc='FR2DK0680010', disc_number=1,
                               audio_files=audiofiles1)
"""                               

"""
class DataBatch1(object):

    delivery = IDOLDelivey()
    
"""
