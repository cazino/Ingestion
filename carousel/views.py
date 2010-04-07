# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import Context, loader
from mp3.main.models import Carrousels
from mp3.main.views import common
from mp3.main.helpers import AlbumVignette

def build_context(request, carousel):
    context = Context({'carousel' : []})
    for i in range(1,21):
        album = eval("carousel.album%s" % (i,))
        context['carousel'].append(AlbumVignette(request, album))
    return context
                
def carousel(request):
    if 'continent' in request.GET:
        location = request.GET['continent']
    elif 'genre' in request.GET:
        location = request.GET['genre']
    lang = common.db_lang_code(request)
    if location in ['999', '10', '20', '30', '50']:
        # Location is Homepage or a continent 
        carousel = Carrousels.objects.get(car_pagecontinent=location, car_langue=lang)
    else:
        # Location is a genre
        carousel = Carrousels.objects.get(car_pagegenre=location, car_langue=lang)
    template = loader.get_template('carousel.html')
    c = build_context(request, carousel)
    response = HttpResponse(template.render(c))
    response['Content-Type'] = 'text/xml'
    return response
