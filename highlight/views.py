# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import Context, loader
from mp3.highlight.models import Alaune
from mp3.main.views import common
from mp3.highlight.helpers import HighlightVignette


def highlight(request):
    if 'continent' in request.GET:
        location = request.GET['continent']
    elif 'genre' in request.GET:
        location = request.GET['genre']
    lang = common.db_lang_code(request)
    alaune = Alaune.objects.get(location=location, langue=lang) 
    context = Context({'highlights' : []})
    for i in [2, 3, 4, 1]:
        highlight = alaune.highlights.filter(slide_type=i).latest('creadate')
        context['highlights'].append(HighlightVignette(request, highlight))
    template = loader.get_template('highlight.html')
    response = HttpResponse(template.render(context))
    response['Content-Type'] = 'text/xml'
    return response
    
    
        
