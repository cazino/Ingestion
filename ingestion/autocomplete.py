# fields.py


# -*- coding: utf-8 -*-
from django import forms
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode 
from django.core.urlresolvers import reverse
from django.forms.util import ErrorList, ValidationError
CLIENT_CODE = """
<input type="text" name="%s_text" id="%s_text"/>
<input type="hidden" name="%s" id="%s" value="" />
<script type="text/javascript">
     $(function(){
	function formatItem(row) {
		return row[1] ;
	}
	function formatResult(row) {
                return row[1];
	}
	$("#%s_text").autocomplete('%s', {
                mustMatch: true,
		formatItem: formatItem,
		formatResult: formatResult
	});
	$("#%s_text").result(function(event, data, formatted) {
              $("#%s").val(data[0]);                         

	});

     });
</script>
"""

class ModelAutoCompleteWidget(forms.widgets.TextInput):
    """ widget autocomplete for text fields
    """
    html_id = ''
    def __init__(self, 
                 lookup_url=None, 
                 *args, **kw):
        super(forms.widgets.TextInput, self).__init__(*args, **kw)
        # url for Datasource
        self.lookup_url = lookup_url
       

    def render(self, name, value, attrs=None):
        if value == None:
            value = ''
        html_id = attrs.get('id', name)
        self.html_id = html_id

        lookup_url = self.lookup_url
        detail_url = reverse('ajax_platos_detail')
        return mark_safe(CLIENT_CODE % (name, html_id, name, html_id, html_id,
                                       lookup_url, html_id, html_id, detail_url))


    def value_from_datadict(self, data, files, name):
        """
        Given a dictionary of data and this widget's name, returns the value
        of this widget. Returns None if it's not provided.
        """

        return data.get(name, None)

    

        
class ModelAutoCompleteField(forms.fields.CharField):
    """
    Autocomplete form field for Model Model
    """
    model = None
    url = None


    def __init__(self, model,  lookup_url, *args, **kwargs):
        self.model, self.url = model, lookup_url
        super(ModelAutoCompleteField, self).__init__(
            widget = ModelAutoCompleteWidget(lookup_url=self.url),
            max_length=255,
            *args, **kwargs)

    def clean(self, value):

        try: 
            obj = self.model.objects.get(pk=value)
        except self.model.DoesNotExist:
            raise ValidationError(u'Invalid item selected')            
        return obj     








