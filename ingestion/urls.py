from django.conf.urls.defaults import *
from mp3.main.models import Artist

urlpatterns = patterns('',
        
    (r'^batch-view/$', 'mp3.ingestion.views.batch_view'),  # Home page
    (r'^artist-lookup/$', 'mp3.ingestion.views.artist_lookup'),  
    (r'^label-lookup/$', 'mp3.ingestion.views.label_lookup'),
    (r'^url-lookup/$', 'mp3.ingestion.views.url_lookup'),
)

