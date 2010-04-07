# -*- coding: utf-8 -*-
import pdb
from django import forms
from django.forms.formsets import formset_factory
from django.test import TestCase
from mp3.main.models import Artist
from mp3.ingestion.models import DeliveryArtist
from mp3.ingestion.forms import ArtLabForm,  ArtistForm, LabelForm, ReleaseForm

   
class ArtLabFormTest(TestCase):

    def setUp(self):
        self.name = 'jojo'
        self.release_title = 'release_title'

    """
    Test tha name and name_hidden are always equal
    """
    def test_init_with_data(self):
        artlab_form = ArtLabForm(data={'name_hidden': self.name, 'release_title_hidden': self.release_title})
        self.assertEqual(self.name, artlab_form.name)
        self.assertEqual(self.release_title, artlab_form.release_title)

    def test_init_with_initial_data(self):
        artlab_form = ArtLabForm(initial={'name_hidden': self.name, 'release_title_hidden': self.release_title})
        self.assertEqual(self.name, artlab_form.name)
        self.assertEqual(self.release_title, artlab_form.release_title)

    """
    Traditionnal form validation tests
    """
    def test_no_field(self):
        artlab_form = ArtLabForm(data={'create': 1, 'name_hidden': 'jojo'})
        self.assertFalse(artlab_form.is_valid())

    def test_missing_pk(self):
        artlab_form = ArtLabForm(data={'create': 1, 'name_hidden': 'jojo'})
        self.assertFalse(artlab_form.is_valid())

    def test_missing_create(self):
        artlab_form = ArtLabForm(data={'pk': 1, 'name_hidden': 'jojo'})
        self.assertFalse(artlab_form.is_valid())

    def test_valid(self):
        artlab_form = ArtLabForm(data={'pk': 1, 'name_hidden': 'jojo', 'release_title_hidden': 'release_title', 
                                       'create': 1})
        self.assertTrue(artlab_form.is_valid())


class ArtistFormtest(TestCase):
    
    """
    Traditionnal Validation Tests
    """
    def test_create_with_no_url(self):
        artist_form = ArtistForm(data={'pk': 1, 'mdx_artist_id': 72, 'create': 1, 'name_hidden': 'tutu'})
        self.assertFalse(artist_form.is_valid())
        self.assertEqual(["Entrez un URL"], artist_form._errors['url'])
                
    def test_not_create_with_no_artist_id(self):
        artist_form = ArtistForm(data={'pk': 1, 'name': 'jojo', 'create': 0})
        self.assertFalse(artist_form.is_valid())
        self.assertEqual(["Vous devez sélectionner un artiste"], artist_form._errors['mdx_artist_id'])
        
    def test_link_with_wrong_artist_id(self):
        artist_form = ArtistForm(data={'pk': 1, 'name': 'jojo', 'create': 0, 'mdx_artist_id': 3})
        self.assertFalse(artist_form.is_valid())
        self.assertEqual(["L'artiste n'existe pas"], artist_form._errors['mdx_artist_id'])       


class LabelFormTest(TestCase):
    """
    Traditionnal Validation Tests
    """    
    def test_link_with_no_label_id(self):
        label_data_form = LabelForm({'pk': 1, 'name': 'jojo', 'create': 0})
        self.assertFalse(label_data_form.is_valid())
        self.assertEqual(["Vous devez sélectionner un label"], label_data_form._errors['mdx_label_id'])

    def test_link_with_wrong_label_id(self):
        label_data_form = LabelForm({'pk': 1, 'name': 'jojo', 'create': 0, 'mdx_label_id': 3})
        self.assertFalse(label_data_form.is_valid())
        self.assertEqual(["Le label n'existe pas"], label_data_form._errors['mdx_label_id'])

     
class ReleaseFormTest(TestCase):

    def setUp(self):
        self.title = 'title'
        self.artist_name = 'artist_name'
        self.label_name = 'label_name'
    """
    Traditionnal Validation Tests
    """
    def test_no_field(self):
        release_form = ReleaseForm(data={})
        self.assertFalse(release_form.is_valid())
           
    def test_no_pk(self):
        release_form = ReleaseForm(data={'title': 'eede'})
        self.assertFalse(release_form.is_valid())
        
    def test_pk_wrong_type(self):
        release_form = ReleaseForm(data={'pk': 'aaa'})
        self.assertFalse(release_form.is_valid())
    
    def test_no_title(self):
        release_form = ReleaseForm(data={'pk': 12, 'annuler': True})
        self.assertFalse(release_form.is_valid())

    def test_valid(self):
        release_form = ReleaseForm(data={'pk': 12, 'title_hidden': 'title', 
                                    'artist_name_hidden': 'artist_name',
                                    'label_name_hidden': 'label_name'})
        self.assertTrue(release_form.is_valid())

    """
    Test tha title and title_hidden are always equal    
    """
    def test_init_with_data(self):
        release_form = ReleaseForm(data={'title_hidden': self.title, 'artist_name_hidden': self.artist_name,
                                         'label_name_hidden': self.label_name})
        self.assertEqual(self.title, release_form.title)
        self.assertEqual(self.artist_name, release_form.artist_name)
        self.assertEqual(self.label_name, release_form.label_name)

    def test_init_with_initial_data(self):
        release_form = ReleaseForm(initial={'title_hidden': self.title, 'artist_name_hidden': self.artist_name,
                                         'label_name_hidden': self.label_name})
        self.assertEqual(self.title, release_form.title)
        self.assertEqual(self.artist_name, release_form.artist_name)
        self.assertEqual(self.label_name, release_form.label_name)

