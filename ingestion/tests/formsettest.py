import pdb
from django.forms.formsets import formset_factory
from django.test import TestCase
from mp3.ingestion.forms import DataFormSet, ArtLabForm, ArtistForm, LabelForm, ReleaseForm
from mp3.ingestion.models import Batch



class ArtLabFormSetTest(TestCase):
    
    def setUp(self):
        self.name = 'jojo'
        self.release_title = 'release_title'

    def test_construct(self):
        self.assert_(formset_factory(ArtLabForm, formset=DataFormSet, extra=0))

    def test_construct_with_data(self):
        formset = formset_factory(ArtLabForm, formset=DataFormSet, extra=0)\
                                      (data={'data-0-create': 1,
                                             'data-0-name_hidden': self.name,
                                             'data-0-release_title_hidden': self.release_title,
                                             'data-TOTAL_FORMS': u'1',
                                             'data-INITIAL_FORMS': u'0',
                                             'data-MAX_NUM_FORMS': u'0',}, prefix='data')
        self.assertEqual(self.name, formset.forms[0].name)
        self.assertEqual(self.release_title, formset.forms[0].release_title)

    def test_construct_with_initial_data(self):
        formset = formset_factory(ArtLabForm, formset=DataFormSet, extra=0)\
                                    (initial=[{'create': 1,
                                               'name_hidden': self.name,
                                               'release_title_hidden': self.release_title}], prefix='data')
        self.assertEqual(self.name, formset.forms[0].name)
        self.assertEqual(self.release_title, formset.forms[0].release_title)

class ArtistFormSetTest(TestCase):
        
    def test_valid(self):
        formset = formset_factory(ArtistForm, formset=DataFormSet, extra=0)(data={'artist-0-pk': 12,
                                                                 'artist-0-create': 1,
                                                                 'artist-0-name_hidden': 'jojo',
                                                                 'artist-0-release_title_hidden': 'title',
                                                                 'artist-0-url': 'jojo',
                                                                 'artist-TOTAL_FORMS': u'1',
                                                                 'artist-INITIAL_FORMS': u'0',
                                                                 'artist-MAX_NUM_FORMS': u'0',
                                                                 }, prefix='artist')
        self.assertTrue(formset.is_valid())
                                                                                         
    def test_get_by_pk_artist(self):
        formset = formset_factory(ArtistForm, formset=DataFormSet, extra=0)(data={'artist-0-pk': 12,
                                                                 'artist-0-create': 1,
                                                                 'artist-0-name_hidden': 'jojo',
                                                                 'artist-0-release_title_hidden': 'title',
                                                                 'artist-0-url': 'jojo',
                                                                 'artist-TOTAL_FORMS': u'1',
                                                                 'artist-INITIAL_FORMS': u'0',
                                                                 'artist-MAX_NUM_FORMS': u'0',
                                                                 }, prefix='artist')
        if formset.is_valid():
            self.assertEqual(12, formset.get_by_pk(12).cleaned_data['pk'])
        else:
            self.fail()
        
    def test_get_by_pk_artist_missing(self):
        formset = formset_factory(ArtistForm, formset=DataFormSet, extra=0)(data={'artist-0-pk': 12,
                                                                 'artist-0-create': 1,
                                                                 'artist-0-name_hidden': 'jojo',
                                                                 'artist-0-release_title_hidden': 'title',
                                                                 'artist-0-url': 'jojo',
                                                                 'artist-TOTAL_FORMS': u'1',
                                                                 'artist-INITIAL_FORMS': u'0',
                                                                 'artist-MAX_NUM_FORMS': u'0',
                                                                 }, prefix='artist')
        if formset.is_valid():
            self.assertEqual(None, formset.get_by_pk(13))
        else:
            self.fail()
        

    def test_get_by_pk_label(self):
        formset = formset_factory(LabelForm, formset=DataFormSet, extra=0)(data={'label-0-pk': 12,
                                                                 'label-0-name_hidden': 'jojo',
                                                                 'label-0-release_title_hidden': 'title',
                                                                 'label-0-create': 1,
                                                                 'label-TOTAL_FORMS': u'1',
                                                                 'label-INITIAL_FORMS': u'0',
                                                                 'label-MAX_NUM_FORMS': u'0',
                                                                 }, prefix='label')
        self.assertTrue(formset.is_valid())
        self.assertEqual(12, formset.get_by_pk(12).cleaned_data['pk'])
        
    def test_get_by_pk_label_missing(self):
        formset = formset_factory(LabelForm, formset=DataFormSet, extra=0)(data={'label-0-pk': 12,
                                                                 'label-0-name_hidden': 'jojo',
                                                                 'label-0-release_title_hidden': 'title',
                                                                 'label-0-create': 1,
                                                                 'label-TOTAL_FORMS': u'1',
                                                                 'label-INITIAL_FORMS': u'0',
                                                                 'label-MAX_NUM_FORMS': u'0',
                                                                 }, prefix='label')
        self.assertTrue(formset.is_valid())
        self.assertEqual(None, formset.get_by_pk(22))
        

    def test_get_by_pk_release(self):
        formset = formset_factory(ReleaseForm, formset=DataFormSet, extra=0)\
                                 (data={'release-0-pk': 12,
                                        'release-0-title_hidden': 'jojo',
                                        'release-0-artist_name_hidden': 'jojo',
                                        'release-0-label_name_hidden': 'jojo',
                                        'release-TOTAL_FORMS': u'1',
                                        'release-INITIAL_FORMS': u'0',
                                        'release-MAX_NUM_FORMS': u'0'}, prefix='release')
        formset.is_valid()
        self.assertEqual(12, formset.get_by_pk(12).cleaned_data['pk'])
        
    def test_get_by_pk_release_missing(self):
        formset = formset_factory(ReleaseForm, formset=DataFormSet, extra=0)\
                                 (data={'release-0-pk': 12,
                                        'release-0-title_hidden': 'jojo',
                                        'release-0-artist_name_hidden': 'jojo',
                                        'release-0-label_name_hidden': 'jojo',
                                        'release-TOTAL_FORMS': u'1',
                                        'release-INITIAL_FORMS': u'0',
                                        'release-MAX_NUM_FORMS': u'0'}, prefix='release')
        formset.is_valid()
        self.assertEqual(None, formset.get_by_pk(1))
