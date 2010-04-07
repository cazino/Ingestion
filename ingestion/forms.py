# -*- coding: utf-8 -*-
import re, unicodedata
from django import forms
from django.forms.widgets import Input
from django.db.models import ObjectDoesNotExist
from django.forms.formsets import BaseFormSet
from django.forms.util import ErrorList
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.forms.util import flatatt
from django.forms.widgets import Input
from mp3.main.models import Artist, Label
from mp3.ingestion.autocomplete import ModelAutoCompleteWidget
from mp3.ingestion.utils import similar_artist
from mp3.ingestion.reports import Report

import pdb


class DivErrorList(ErrorList):
    def __unicode__(self):
        return self.as_divs()

    def as_divs(self):
        if not self: return u''
        return u'<div class="errorlist">%s</div>' % ''.join([u'<div class="error">%s</div>' % e for e in self])
       
class MyChoiceField(forms.TypedChoiceField):
   
    def valid_value(self, value):
       return True


class URLInput(Input):
    """
    Simple autocomplete input
    """
    def _get_id_int(self, final_attrs):
        """
        Return the number contained in the id 
        """
        pattern = re.compile('([0-9]+)')
        str_id = final_attrs['id']
        return int(pattern.search(str_id).group(1))
        
    def _render_js(self, final_attrs):
       return u'''<script type="text/javascript">$(document).ready(function(){
     $("#id_artist-%(id)s-url").autocomplete("../url-lookup");
       });</script>''' % {'id': self._get_id_int(final_attrs)}
        
    def render(self, name, value, attrs=None):
        html = super(URLInput, self).render(name, value, attrs)
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        js = mark_safe(self._render_js(final_attrs))
        return html + js
 

class MyHiddenInput(forms.HiddenInput):
    """
    Abstract Base class for ArtistHiddenInput and LabelHiddenInput
    Add a javscript in html output
    The javascript rendeering has to be defines ind subclass in _render_js method
    """
    def _get_id_int(self, final_attrs):
        """
        Return the number contained in the id 
        """
        pattern = re.compile('([0-9]+)')
        str_id = final_attrs['id']
        return int(pattern.search(str_id).group(1))

    def render(self, name, value, attrs=None):
        html = super(MyHiddenInput, self).render(name, value, attrs)
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        js = mark_safe(self._render_js(final_attrs))
        return html + js    
    
class ArtistHiddenInput(MyHiddenInput):
    """
    Add an autocomplete capabilities to the field with id: "id_artist-X-name_auto"
    Autocomplete selection cnage the value of this field (id: "id_artist-X-mdx_artist_id")
    Horrible implementation
    """
            
    def _render_js(self, final_attrs):
       return u'''<script type="text/javascript">$(document).ready(function(){
     $("#id_artist-%(id)s-name_auto").autocomplete("../artist-lookup");
     $("#id_artist-%(id)s-name_auto").result(function(event, data, formatted){
         if(data){
           var name = data[0];
           var id = data[1];
           $("#id_artist-%(id)s-mdx_artist_id").val(id);
         }   
       }     
     );
  });</script>''' % {'id': self._get_id_int(final_attrs)}
        
        
class LabelHiddenInput(MyHiddenInput):
    """
    Add an autocomplete capabilities to the field with id: "id_label-X-name_auto"
    Autocomplete selection cnage the value of this field (id: "id_label-X-mdx_label_id")
    Horrible implementation
    """
        
    def _render_js(self, final_attrs):
       return u'''<script type="text/javascript">$(document).ready(function(){
     $("#id_label-%(id)s-name_auto").autocomplete("../label-lookup");
     $("#id_label-%(id)s-name_auto").result(function(event, data, formatted){
         if(data){
           var name = data[0];
           var id = data[1];
           $("#id_label-%(id)s-mdx_label_id").val(id);
         }   
       }     
     );
  });</script>''' % {'id': self._get_id_int(final_attrs)}
        

class ReadOnlyCharField(forms.CharField):

    pass
	

class DataForm(forms.Form):

    """
    Abstract base class
    """
    pk = forms.IntegerField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(DataForm, self).__init__(*args, **kwargs)
        self.report = None
        # For each ReadOnlyCharField, create an attibute with the same value
        for name, field in self.fields.items():
            if isinstance(field, ReadOnlyCharField):
                display_field_name = re.sub(r'_hidden$', '', name)
                if kwargs.get('data'):
                    setattr(self, display_field_name, self._raw_value(name))
                else:
                    setattr(self, display_field_name, kwargs.get('initial') and kwargs.get('initial').get(name))
                    

class ArtLabForm(DataForm):

    name_hidden = ReadOnlyCharField(widget=forms.HiddenInput)
    release_title_hidden = ReadOnlyCharField(widget=forms.HiddenInput)
    name_auto = forms.CharField(required=False, widget=Input)
    create = forms.TypedChoiceField(choices=((0, 'Lier'), (1, 'Créer')), widget=forms.Select, coerce=int)

            
class ArtistForm(ArtLabForm):

    mdx_artist_id = forms.IntegerField(required=False, widget=ArtistHiddenInput)
    url = forms.CharField(required=False, widget= URLInput)

    def __init__(self, *args, **kwargs):
        super(ArtistForm, self).__init__(error_class=DivErrorList, **kwargs)
    
    def clean(self):
        create = self.cleaned_data.get('create')
        if create:
            url = self.cleaned_data.get('url')
            if not url:
                self._errors.setdefault('url', ErrorList()).append("Entrez un URL")
        else: 
            mdx_artist_id = self.cleaned_data.get('mdx_artist_id')
            if mdx_artist_id:
                try:
                    Artist.objects.get(pk=mdx_artist_id)
                except ObjectDoesNotExist:
                    self._errors.setdefault('mdx_artist_id', ErrorList()).append("L'artiste n'existe pas")
                    del self.cleaned_data['mdx_artist_id']
            else:
                self._errors.setdefault('mdx_artist_id', ErrorList()).append("Vous devez sélectionner un artiste")
        return self.cleaned_data
             
            
class LabelForm(ArtLabForm):
    
    mdx_label_id = forms.IntegerField(required=False, widget=LabelHiddenInput)
        
    def clean(self):
        create = self.cleaned_data.get('create')
        if not create:
            mdx_label_id = self.cleaned_data.get('mdx_label_id')
            if mdx_label_id:
                try:
                    Label.objects.get(pk=mdx_label_id)
                except Label.DoesNotExist:
                    self._errors.setdefault('mdx_label_id', ErrorList()).append("Le label n'existe pas")
                    del self.cleaned_data['mdx_label_id']
            else:
                self._errors.setdefault('mdx_label_id', ErrorList()).append("Vous devez sélectionner un label")
        return self.cleaned_data

        
class ReleaseForm(DataForm):
    
    annuler = forms.BooleanField(required=False)
    title_hidden = ReadOnlyCharField(widget=forms.HiddenInput)
    artist_name_hidden = ReadOnlyCharField(widget=forms.HiddenInput)
    label_name_hidden = ReadOnlyCharField(widget=forms.HiddenInput)

    def report_list():
        return (rapport for rapport in (self.report, self.artist_report) if rapport)

   
class DataFormSet(BaseFormSet):
    
    def get_by_pk(self, pk):
        for form in self.forms:
            if form.cleaned_data['pk'] == pk:
                return form
        

    
    
