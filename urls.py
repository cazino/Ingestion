from django.conf.urls.defaults import *
import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()



urlpatterns = patterns('',
    # Example:
    
    
    
    (r'^$', 'mp3.main.views.homepage.home'),  # Home page

    (r'^continent_[^_]+_(?P<continent>[^\.]+)\.htm$', 'mp3.main.views.homepage.continent'),  # Home continent



    (r'^carousel', 'mp3.carousel.views.carousel'),  # Carousel
    (r'^highlight', 'mp3.highlight.views.highlight'),  # Highlight
    
    (r'^media/(?P<path>.*)$', 
     'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}), # media files - dev setting 
    (r'^i18n/', include('django.conf.urls.i18n')), # Change language

    (r'^ingestion/', include('mp3.ingestion.urls')), # Admin Ingestion
    #(r'^ingestion/batch-content/', 'mp3.ingestion.views.batch_content'),
    
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)


