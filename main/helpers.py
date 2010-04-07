from django.utils.translation import ugettext as _

class Helper(object):
    """
    Abstract class - A helper is designed to be load in a template for rendering content
    """
    
    def __init__(self, request):
        self.request = request
                
    def _lang_field(self, request, field):
    # Return the correct filed name, given the language setting of the request
        if request.LANGUAGE_CODE == 'fr':
            return field
        return field + '_en'
           
class AlbumVignette(Helper):
    """
    Small album vignette
    """
    def __init__(self, request, album, vignette_type=''):
        super(AlbumVignette, self).__init__(request)
        self.album_title = album.title
        self.album_id = album.pk
        self.img_url = album.imagefile_set.filter(ima_usage='cover100').get().full_path()
        self.artist_name = album.artist.name
        self.artist_url = album.artist.art_url_rewriting
        self.artist_id = album.artist.pk
        self.pays = self._country(request, album.artist)
        self.type = vignette_type
        
    def _country(self, request, artist):
        # Renvoie le nom du pays de l'artiste ou 'various countries' s'il y en a plusieurs
        countries = artist.countries
        if countries.count() > 1:
            return _('various countries')
        pays_field = self._lang_field(request, 'cou_name')
        return eval('artist.countries.get().' + pays_field)
   
