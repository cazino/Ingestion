# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django.db.models import Count
from mp3.main.models import Album, Orders, PanierItems
       
def db_lang_code(request):
    # Renvoie le code lang utilisé par la db
        if request.LANGUAGE_CODE == 'fr':
            return 1
        return 3
        
class Location(object):
    """
    Value object - Une 'location' est une des homep ge du site ('home' ou 'continent' ou 'genre')
    """
    pass
    
    
class BestAlbumSellCalculator(object):

    def __init__(self, period=6):
        self.ref_date = datetime.today() - timedelta(days=period*30)
        
    def calculate(self):
        validated_oders = Orders.validated_objects.filter(validation_date__gte=self.ref_date)
        best_sold_albums_id = PanierItems.objects.filter(object_type=2, panier_id__in=validated_oders.values_list('panier_id'))\
                                  .values('object_id').annotate(ventes=Count('object_id')).order_by('-ventes')[:7].values_list('object_id')
        return Album.objects.filter(pk__in=best_sold_albums_id)
        
    
    
    

    
