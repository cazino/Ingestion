from django.db import transaction
from mp3.main.models import Artist


@transaction.commit_manually
def artist_insert():
    try:
        artist1 = Artist.objects.create(pk=2,name='aa')
        artist2 = Artist.objects.create(pk=3, name='az')
        transaction.commit()
    except:
        transaction.rollback()
        
        
