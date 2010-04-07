# -*- coding: utf-8 -*-
from mp3.ingestion.mappers import ArtistMapper, LabelMapper, ReleaseMapper

"""
class DeliveryProcessor(object):
    """"
    Prend en charge les opérations de base de données (délègue à des 'mappers')
    et de déplacement de fichier d'une Delivery
    """"
    def __init__(self, delivery):
        self.delivery = delivery
        
    def _process_artist(self, artist_form):
        create = artist_form.cleaned_data['create']
        artist = self.delivery.artist
        if create: # Création d'un nouvel artiste
            mapper = ArtistMapper(name=artist.name, url=artist_form.cleaned_data['url'],
                                  external_id=artist.pk, vendor_id=self.delivery.vendor_id)
            return mapper.create()
        else: # Liaison avec un artiste existant
            mapper = ArtistMapper(artist_id=artist_form.cleaned_data['mdx_artist_id'], external_id=artist.pk, vendor_id=self.delivery.vendor_id)
            return mapper.link()
            
    def _process_label(self, label_form):
        create = label_form.cleaned_data['create']
        label = self.delivery.label
        if create: # Création d'un nouvel artiste
            mapper = LabelMapper(name=label.name,  external_id=label.pk, vendor_id=self.delivery.vendor_id)
            return mapper.create()
        else: # Liaison avec un artiste existant
            mapper = LabelMapper(label_id=label_form.cleaned_data['mdx_label_id'], external_id=label.pk, vendor_id=self.delivery.vendor_id)
            return mapper.link()
"""         


class BatchBase(object):
    
    def __init__(self, request):
        self.batchpath = request.GET.get('batchpath', DEFAULT_BATCH_PATH)
        self.batch = Batch(self.batchpath)
        self.ArtistDataFormSet = formset_factory(ArtistDataForm, formset=DataFormSet, extra=0)
        self.LabelDataFormSet = formset_factory(LabelDataForm, formset=DataFormSet, extra=0)
        self.ReleaseDataFormSet = formset_factory(ReleaseDataForm, formset=DataFormSet, extra=0)
        

class BatchView(BatchBase):

    def __init__(self, request):
        super(BatchView, self).__init__(request)
        self.artist_formset = self.ArtistDataFormSet(initial=[{'pk': artist.pk, 'name': artist.name}
                                                     for artist in self.batch.artists()], prefix='artist')
        self.label_formset = self.LabelDataFormSet(initial=[{'pk': label.pk, 'name': label.name}
                                                for label in self.batch.labels()], prefix='label')
        self.release_formset = self.ReleaseDataFormSet(initial=[{'pk': release.pk, 'title': release.title}
                                               for release in self.batch.releases()], prefix='release')                                                 

        
class BatchProcessor(BatchBase):

    def __init__(self, request):
        super(BatchProcessor, self).__init__(request)
        self.artist_formset = self.ArtistDataFormSet(request.POST, prefix='artist')
        self.label_formset = self.LabelDataFormSet(request.POST, prefix='label')
        self.release_formset = self.ReleaseDataFormSet(request.POST, prefix='release')
        self.artist_tracker = {}
        self.label_tracker = {}
        
    def process(self):
        if self.artist_formset.is_valid() \
                and self.label_formset.is_valid() \
                and self.release_formset.is_valid():
            for form in self.release_formset.forms:
                release = self.batch.get_release(form.cleaned_data['pk'])
                if not release.artist_pk in self.artist_tracker:
                    self._process_artist(release.artist_pk)
                if not release.label_pk in self.label_tracker:
                    self._process_label(release.label_pk)
                self._process_release()
        
    @transaction.commit_on_success
    def _process_artist(self, artist_pk):
        artist_form = self.artist_formset.get_by_pk(artist_pk)
        #Artist.objects.create(name='ppaappaa')
        #Artist.objects.create(pk='aaa')

    @transaction.commit_on_success                    
    def _process_label(self, label_pk):
        pass

    @transaction.commit_on_success        
    def _process_release(self):
        pass


