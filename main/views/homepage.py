# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.template import RequestContext, loader
from mp3 import settings
from mp3.main.models import ActualitesDisque, CoupsDeCoeur, Orders
from mp3.main.helpers import AlbumVignette
from mp3.main.views import common
from mp3.main.context_processors import home_continent_genre_processor, home_continent_processor, home_processor

           
def _tryptique(request, context, tablename, location, vignette_type):
    tryptique = eval("%s.objects.get(localisation=%s)" % (tablename, location))
    albums = []
    for i in range(1,4):
        tmp_dic = {}
        album = eval("tryptique.album%s" % (i,))
        albums.append(AlbumVignette(request, album, vignette_type))
    context.update({tablename : albums})   
        
def _les_tryptiques(request, context, location)        :
    """
    Ajoute au contexte les deux tryptiques de  bas de page
    """
    _tryptique(request, context, 'ActualitesDisque', location, 'ala') #  Boite à la une (bas gauche)
    _tryptique(request, context, 'CoupsDeCoeur', location, 'cc') #  Boite coup de coeur (bas droite)
        
def best_sales(request):
    ref_date = datetime.today().date() - timedelta(days=180)
    orders = Orders.validated_objects.filter(validated__gte=ref_date)
        
def home(request):
    # Homepage view
    context = RequestContext(request, processors=[home_processor])
    location = 999
    context.update({'LOCATION_STRING': 'continent', 'LOCATION_CODE': 999})
    _les_tryptiques(request, context, location)
    best_sales(request)
    t = loader.get_template('home.html')
    return HttpResponse(t.render(context))
    
def continent(request, continent):
    context = RequestContext(request, processors=[home_continent_processor])
    continents = continent.split('|')
    location = continents[0]    
    context.update({'LOCATION_STRING': 'continent', 'LOCATION_CODE': location})
    _les_tryptiques(request, context, location)
    t = loader.get_template('home-continent.html')
    return HttpResponse(t.render(context))




