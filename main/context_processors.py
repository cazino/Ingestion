# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _


def _get_main_logo(request):
    """
    Build the code of the main logo regarding th session language
    """
    if request.LANGUAGE_CODE == 'fr':
        return "<img src=\"media/img/logo_mdx.jpg\" width=\"312\" height=\"81\" alt=\"Logo Mondomix MP3\"/>"
    return "<img width=\"425\" height=\"81\" alt=\"MP3 Mondomix\" src=\"media/img/logo_mondocalabash.jpg\"/>"

def _build_continents(request):
    return  [{'name': _('Africa'),'link':_('continent_africa_10.htm')},
             {'name': _('Americas'),'link':_('continent_americas_50|60.htm')},
             {'name': _('Asia-Oceania'),'link':_('continent_asia_20|40|70.htm')},
             {'name': _('Europe'),'link':_('continent_europe_30.htm')},]
    
def _build_genres(request):
    return  [{'name': _('Afro'),'link':_('genre_afro_1.htm')},
             {'name': _('Creole'),'link': 'genre_creole_2.htm'},
             {'name': 'Reggae','link': 'genre_reggae_3.htm'},
             {'name': 'Latin','link': 'genre_latin_4.htm'},
             {'name': 'Oriental','link': 'genre_oriental_5.htm'},
             {'name':  'Asian Vibe','link': 'genre_asian-bibe_6.htm'},
             {'name': _('Gypsy'),'link': _('genre_gypsy_7.htm')},
             {'name': _('Songs'),'link':_('genre_songs_8.htm')},
             {'name': _('Traditionnal . Folk'),'link':_('genre_traditionnal--folk_9.htm')},
             {'name': 'Jazz . Blues','link': 'genre_jazz--blues_10.htm'},
             {'name': _('Classical . Contemporary'),'link':_('genre_classical--contemporary_17.htm')},
             {'name': 'Precussions','link': 'genre_percussions_11.htm'},
             {'name': _('Sacred'),'link':_('genre_sacred_12.htm')},
             {'name': _('HipHop . Electro . Spoken'),'link':_('genre_hiphop--electro-spoken-words_13.htm')},
             {'name': 'Funk . Soul . Groove','link': 'genre_funk--soul--groove_18.htm'},
             {'name': 'Pop . Rock','link': 'genre_pop--rock_14.htm'},
             {'name': _('Soundtracks . Poetry'),'link':_('genre_soundtracks--poetry_16.htm')}
             ]

def base(request):
    # Base context far the all app
    context = {
        'mdx_mag': _('mondomix magazine'),
        'help' : _('help'),
        'beta' : 'beta',
        'mdx_experience' : _('the mondomix mp3 experience'),
        'drm_free' : _('DRM free - compatible with all digital players'),
        'explore' : _('explore'),
        'genres': _('genres'),
        'my_cart': _('my cart'), 
        'register': _('register'), 
        'my_account': _('my account'),
        'subscribe_news': _('subscribe to the newsletter'),
        'download': _('download'),
        'mdx_logo' : _get_main_logo(request),
        'CONTINENTS' : _build_continents(request),
        'GENRES' : _build_genres(request),
    }
    return context
    
def home_continent_genre_processor(request):
    return {'newreleases': _('New releases'),}
    
def home_continent_processor(request):
    """
    Add to the context, all variable common to all homepages
    """
    dico = home_continent_genre_processor(request)
    dico.update({'highlight' : _('Highlight'),
            'ourpicks' : _('Our Picks'),})
    return dico

def home_processor(request):
    dico = home_continent_processor(request)
    tmp_dic = {}
    if request.LANGUAGE_CODE == 'fr':
        tmp_dic['blabla_title'] = "Depuis 10 ans, Mondomix apporte en images, reportages et témoignages, un regard gourmand sur la multitude d'expressions musicales qui rythment la planète."
        tmp_dic['blabla_text'] = "Ces musiques traditionnelles, contemporaines, enracinées ou métissées qui sont, par souci de simplification, rassemblées sous l'étiquette \"Musiques du Monde\" peuplent de plus en plus de baladeurs MP3 et autres appareils nomades. Il ne manquait plus à Mondomix qu'à sélectionner et offrir ces musiques avec le même souci d'ouverture et la même curiosité ludique.<br>C'est ce rêve en MP3 sans DRM que Mondomix a initié avec une première version de MondomixMusic en 2005, sans barrière technique, ni cloisonnement culturel.<br>C'est ce rêve que nous vous proposons de partager avec plus de maturité, d'exigence de qualité et d'intensité, à travers cette deuxième version rebaptisée <a href=\"http://mp3.mondomix.com\">mp3.mondomix.com</a>.<br>Dans sa nouvelle mouture, <a href=\"http://mp3.mondomix.com\">mp3.mondomix.com</a> s'efforce à travers de nouveaux outils de classification, de recherche, de recommandation et de communauté, de permettre à tous de naviguer sur tous les continents, traversant tous les courants pour parvenir à se concocter sa propre bande son, la partager et la modeler à sa guise. C'est l'expérience Mondomix en MP3."
    else:
        tmp_dic['blabla_title'] = "For the past ten years, Mondomix has been bringing its audience an exclusive look at the sounds and images which are moving and grooving the planet. The sounds, whether traditional or contemporary, rooted in one culture or a mix of many, are, for lack of a better word, known as \"world music\", and can be found on more and more portable media players around the world. It was up to Mondomix to find a way to select the best music and offer it with equal parts openness and curiosity."
        tmp_dic['blabla_text'] = "Mondomix's vision was made into reality in 2005 when it presented MondomixMusic, a new way to download MP3s without the barriers of DRM or cultural pigeonholing.<br>Now with more experience and even higher standards of quality and passion, Mondomix presents its latest vision: <a href=\"http://mp3.mondomix.com\">mp3.mondomix.com</a>. With <a href=\"http://mp3.mondomix.com\">mp3.mondomix.com</a>, Mondomix hopes to offer you new tools for finding, classifying, and recommending new music. Mp3.mondomix.com will allow you to navigate the continents and ride the tradewinds to make your own soundtrack, and to share that soundtrack as you like. Welcome to the MP3 experience, as seen by Mondomix."       
    dico.update(tmp_dic)       
    return dico
    


