# -*- coding: utf-8 -*-
import datetime, pdb
import simplejson as json
from django.db import transaction
from django.db.models import Q
from django.forms.formsets import formset_factory
from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render_to_response
from mp3.main.models import Artist, Label, Disc, Vendor
from mp3.ingestion.models import Batch
from mp3.ingestion.processors import ArtistProcessor, LabelProcessor, ReleaseProcessor
from mp3.ingestion.forms import ArtistForm, LabelForm, ReleaseForm, DataFormSet
from mp3.ingestion.utils import similar_artist, similar_artist_ajax, similar_label_ajax, similar_url_ajax
from mp3.ingestion.utils import latin1_to_ascii, propose_url
from mp3.ingestion.ingestion_localsettings import DEFAULT_BATCH_PATH
from mp3.ingestion.metadata import naming

class BatchView(object):
    
    def __init__(self, request):
        if request.method == 'GET':
            self.batchpath = request.GET.get('batchpath')
        elif request.method == 'POST':
            self.batchpath = request.POST.get('batchpath')
        if 'batchpath' not in self.__dict__:
            self.batchpath = DEFAULT_BATCH_PATH
        self.batch = Batch(self.batchpath)
        self.ArtistFormSet = formset_factory(ArtistForm, formset=DataFormSet, extra=0)
        self.LabelFormSet = formset_factory(LabelForm, formset=DataFormSet, extra=0)
        self.ReleaseFormSet = formset_factory(ReleaseForm, formset=DataFormSet, extra=0)
        self.bad_deliveries = list(self.batch.bad_deliveries())
    

class BatchShow(BatchView):

    def __init__(self, request):
        super(BatchShow, self).__init__(request)
        self.artist_formset = self.ArtistFormSet(initial=[{'pk': artist.pk, 
                                                           'name_hidden': artist.name,
                                                           'release_title_hidden': artist.release.title,
                                                           'url': propose_url(artist.name)}
                                                     for artist in self.batch.unknown_artists()], prefix='artist')
        self.label_formset = self.LabelFormSet(initial=[{'pk': label.pk, 
                                                         'name_hidden': label.name,
                                                         'release_title_hidden': label.release.title,}
                                                for label in self.batch.unknown_labels()], prefix='label')
        self.release_formset = self.ReleaseFormSet(initial=[{'pk': release.pk, 
                                                             'title_hidden': release.title,
                                                             'artist_name_hidden':\
                                                              release.artist and release.artist.name or 'Compilation',
                                                             'label_name_hidden': release.label.name,}
                                               for release in self.batch.releases()], prefix='release')
        
        
        
class BatchProcessor(BatchView):

    def __init__(self, request):
        super(BatchProcessor, self).__init__(request)
        self.artist_formset = self.ArtistFormSet(request.POST, prefix='artist')
        self.label_formset = self.LabelFormSet(request.POST, prefix='label')
        self.release_formset = self.ReleaseFormSet(request.POST, prefix='release')
        
    def process(self):
        if self.artist_formset.is_valid() \
            and self.label_formset.is_valid() \
            and self.release_formset.is_valid():
            for form in self.release_formset.forms:
                delivery = self.batch.get_delivery(release_pk=form.cleaned_data['pk'])
                vendor = Vendor.objects.get(pk=delivery.vendor_id)
                artist = None # Pour pouvoir passer None au ReleaseProcessor dans le cas d'une compil
                # Process Artist
                if delivery.artist:
                    try:
                        # Artiste déjà connu
                        artist = Artist.objects.get(artistvendor__external_artist_id=delivery.artist.pk)
                    except Artist.DoesNotExist:
                        artist_form = self.artist_formset.get_by_pk(delivery.artist.pk)
                        if artist_form:
                            artist_processor = ArtistProcessor(delivery=delivery, artist_form=artist_form, 
                                                           vendor=vendor)
                            artist = artist_processor.build()
                        else:
                            # Si pas de formulaire et artiste inconnu -> compilation, c'est le release processor 
                            # qui créera l'artiste
                            pass
                # Process Label
                try:
                    label = Label.objects.get(labelvendor__external_label_id=delivery.label.pk)
                except Label.DoesNotExist:
                    label_form = self.label_formset.get_by_pk(delivery.label.pk)
                    delivery_label = delivery.label
                    label_processor = LabelProcessor(delivery=delivery, label_form=label_form, vendor=vendor)
                    label = label_processor.build()
                # Process Release                    
                if label:
                    disc = Disc.objects.get(status='default')
                    release_processor = ReleaseProcessor(delivery=delivery, release_form=form, artist=artist,
                                                         label=label, disc=disc, vendor=vendor)
                    album = release_processor.build()
                    

                
def batch_view(request):
    if request.method == 'POST':
        my_view = BatchProcessor(request)
        my_view.process()        
    else:
        my_view = BatchShow(request)
    return render_to_response('batch-view.html', {'artist_formset': my_view.artist_formset,
                                                  'label_formset': my_view.label_formset,
                                                  'release_formset': my_view.release_formset,
                                                  'bad_deliveries': my_view.bad_deliveries,
                                                  })
"""      
def batch_process(request):
    my_view = BatchProcessor(request)  
    my_view.process()
    return render_to_response('batch-view.html', {'artist_formset': my_view.artist_formset,
                                                  'label_formset': my_view.label_formset,
                                                  'release_formset': my_view.release_formset,
                                                  'post': str(request.POST)})

def artist_lookup(request):
    string= request.GET.get('q')
    data = json.dumps(similar_artist(string))
    return HttpResponse(data, mimetype="application/json")
"""
def artist_lookup(request):
    string= request.GET.get('q')
    return HttpResponse(similar_artist_ajax(string))

def label_lookup(request):
    string= request.GET.get('q')
    return HttpResponse(similar_label_ajax(string))

def url_lookup(request):
    string= request.GET.get('q')
    return HttpResponse(similar_url_ajax(string))
 
def autocomplete(request):
    return render_to_response('autocomplete.html')

def autocomplete_artist(request):
    artist_form1 =  ArtistDataForm()
    artist_form2 =  ArtistDataForm()
    return render_to_response('autocomplete_artist.html', {'artist_form1': artist_form1,
                                                           'artist_form2': artist_form2,
                                                           })
