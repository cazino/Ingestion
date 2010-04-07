# -*- coding: utf-8 -*-
import pdb
from django import forms
from django.forms.formsets import formset_factory
from django.test import TestCase
from mp3.main.models import Artist
from mp3.ingestion.models import DeliveryArtist
from mp3.ingestion.forms import DataForm,  ArtistDataForm, LabelDataForm, ReleaseDataForm

   
class DataFormTest(TestCase):

    def setUp(self):
        self.name = 'jojo'

    def test_init_with_data(self):
        artist_form = ArtistDataForm(data={'name_hidden': self.name})
        self.assertEqual(self.name, artist_form.name)

    def test_init_with_initial_data(self):
        artist_form = ArtistDataForm(initial={'name_hidden': self.name})
        self.assertEqual(self.name, artist_form.name)

class ArtistDataFormTest(TestCase):
    
    """
    Traditionnal Validation Tests
    """
    def test_no_field(self):
        artist_data_form = ArtistDataForm({})
        self.assertFalse(artist_data_form.is_valid())
    
    def test_missing_pk(self):
        artist_data_form = ArtistDataForm({'create': 1, 'mdx_artist_id': 72, 'name_hidden': 'jojo'})
        self.assertFalse(artist_data_form.is_valid())
        
    def test_missing_create(self):
        artist_data_form = ArtistDataForm({'pk': 1, 'mdx_artist_id': 72, 'name_hidden': 'jojo'})
        self.assertFalse(artist_data_form.is_valid())
         
    def test_create_with_no_url(self):
        artist_data_form = ArtistDataForm({'pk': 1, 'mdx_artist_id': 72, 'create': 1, 'name_hidden': 'tutu'})
        self.assertFalse(artist_data_form.is_valid())
        self.assertEqual(["Entrez un URL"], artist_data_form._errors['url'])
                
    def test_not_create_with_no_artist_id(self):
        artist_data_form = ArtistDataForm({'pk': 1, 'name': 'jojo', 'create': 0})
        self.assertFalse(artist_data_form.is_valid())
        self.assertEqual(["Vous devez sélectionner un artiste"], artist_data_form._errors['mdx_artist_id'])
        
    def test_not_create_with_wrong_artist_id(self):
        artist_data_form = ArtistDataForm({'pk': 1, 'name': 'jojo', 'create': 0, 'mdx_artist_id': 3})
        self.assertFalse(artist_data_form.is_valid())
        self.assertEqual(["L'artiste n'existe pas"], artist_data_form._errors['mdx_artist_id'])       
    
    """
    Test that display fieds are eqaul ou their corresponding hidden fields
    """
    def test_name(self):
        name_hidden = 'jojo'
        artist_data_form = ArtistDataForm(data={'create': 1, 'mdx_artist_id': 72, 'name_hidden': name_hidden})
        self.assertEqual(name_hidden, artist_data_form.name)

class LabelDataFormTest(TestCase):
    
    def test_no_field(self):
        label_form = LabelDataForm({})
        self.assertFalse(label_form.is_valid())
        
    def test_missing_pk(self):
        label_form = LabelDataForm({'name': 'jojo'})
        self.assertFalse(label_form.is_valid())
    
    """
    def test_create_with_no_name(self):
        label_data_form = LabelDataForm({'pk': 1, 'mdx_label_id': 72, 'create': 1})
        self.assertFalse(label_data_form.is_valid())
        self.assertEqual(["Spécifiez le nom du label"], label_data_form._errors['name'])
    """ 
    def test_link_with_no_label_id(self):
        label_data_form = LabelDataForm({'pk': 1, 'name': 'jojo', 'create': 0})
        self.assertFalse(label_data_form.is_valid())
        self.assertEqual(["Vous devez sélectionner un label"], label_data_form._errors['mdx_label_id'])

    def test_link_with_wrong_label_id(self):
        label_data_form = LabelDataForm({'pk': 1, 'name': 'jojo', 'create': 0, 'mdx_label_id': 3})
        self.assertFalse(label_data_form.is_valid())
        self.assertEqual(["Le label n'existe pas"], label_data_form._errors['mdx_label_id'])

     
class AlbumDataFormTest(TestCase):

    def test_no_field(self):
        release_data_form = ReleaseDataForm({})
        self.assertFalse(release_data_form.is_valid())
           
    def test_no_pk(self):
        release_data_form = ReleaseDataForm({'title': 'eede'})
        self.assertFalse(release_data_form.is_valid())
        
    def test_pk(self):
        release_data_form = ReleaseDataForm({'pk': 412})
        self.assertTrue(release_data_form.is_valid())
        
    def test_pk_wrong_type(self):
        release_data_form = ReleaseDataForm({'pk': 'aaa'})
        self.assertFalse(release_data_form.is_valid())
    
    def test_annuler(self):
        release_data_form = ReleaseDataForm({'pk': 12, 'annuler': True})
        self.assertTrue(release_data_form.is_valid())
