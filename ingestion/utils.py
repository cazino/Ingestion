from django.db.models import Q
from django import forms
from mp3.main.models import Artist, Label


        
def similar_artist(artist_name):
    """
    Return a tuple of (artist_id, artist_name)
    """
    artists_list = Artist.objects.similar_name(artist_name).order_by('name').values('artist', 'name')
    return tuple([(artist['artist'], artist['name']) for artist in artists_list])


def similar_artist_ajax(artist_name):
    """
    Return a tuple of (artist_id, artist_name)
    """
    artists_list = Artist.objects.similar_name(artist_name).order_by('name').values('artist', 'name')
    return "\n".join(["%s|%s" % (artist['name'], artist['artist'])for artist in artists_list])
    

def similar_label_ajax(label_name):
    """
    Return a tuple of (label_id, label_name)
    """
    label_list = Label.objects.similar_name(label_name).order_by('name').values('label', 'name')
    return "\n".join(["%s|%s" % (label['name'], label['label']) for label in label_list])


def similar_url_ajax(url):
    """
    Return a list of urls similar the given URL
    """
    artist_list = Artist.objects.similar_url(url).order_by('url').values('url')
    return "\n".join([artist['url'] for artist in artist_list])

def latin1_to_ascii(unicrap):
    """This replaces UNICODE Latin-1 characters with
    something equivalent in 7-bit ASCII. All characters in the standard
    7-bit ASCII range are preserved. In the 8th bit range all the Latin-1
    accented letters are stripped of their accents. Most symbol characters
    are converted to something meaninful. Anything not converted is deleted.
    """
    xlate={0xc0:'A', 0xc1:'A', 0xc2:'A', 0xc3:'A', 0xc4:'A', 0xc5:'A',
        0xc6:'Ae', 0xc7:'C',
        0xc8:'E', 0xc9:'E', 0xca:'E', 0xcb:'E',
        0xcc:'I', 0xcd:'I', 0xce:'I', 0xcf:'I',
        0xd0:'Th', 0xd1:'N',
        0xd2:'O', 0xd3:'O', 0xd4:'O', 0xd5:'O', 0xd6:'O', 0xd8:'O',
        0xd9:'U', 0xda:'U', 0xdb:'U', 0xdc:'U',
        0xdd:'Y', 0xde:'th', 0xdf:'ss',
        0xe0:'a', 0xe1:'a', 0xe2:'a', 0xe3:'a', 0xe4:'a', 0xe5:'a',
        0xe6:'ae', 0xe7:'c',
        0xe8:'e', 0xe9:'e', 0xea:'e', 0xeb:'e',
        0xec:'i', 0xed:'i', 0xee:'i', 0xef:'i',
        0xf0:'th', 0xf1:'n',
        0xf2:'o', 0xf3:'o', 0xf4:'o', 0xf5:'o', 0xf6:'o', 0xf8:'o',
        0xf9:'u', 0xfa:'u', 0xfb:'u', 0xfc:'u',
        0xfd:'y', 0xfe:'th', 0xff:'y',
        0xa1:'!', 0xa2:'{cent}', 0xa3:'{pound}', 0xa4:'{currency}',
        0xa5:'{yen}', 0xa6:'|', 0xa7:'{section}', 0xa8:'{umlaut}',
        0xa9:'{C}', 0xaa:'{^a}', 0xab:'<<', 0xac:'{not}',
        0xad:'-', 0xae:'{R}', 0xaf:'_', 0xb0:'{degrees}',
        0xb1:'{+/-}', 0xb2:'{^2}', 0xb3:'{^3}', 0xb4:"'",
        0xb5:'{micro}', 0xb6:'{paragraph}', 0xb7:'*', 0xb8:'{cedilla}',
        0xb9:'{^1}', 0xba:'{^o}', 0xbb:'>>',
        0xbc:'{1/4}', 0xbd:'{1/2}', 0xbe:'{3/4}', 0xbf:'?',
        0xd7:'*', 0xf7:'/'
        }

    r = ''
    for i in unicrap:
        if xlate.has_key(ord(i)):
            r += xlate[ord(i)]
        elif ord(i) >= 0x80:
            pass
        else:
            r += i
    return r


def propose_url(artist_name):
    """
    Propose un URL en fonction du nom de l'artiste
    """
    url = ("-".join(latin1_to_ascii(artist_name).split())).lower()
    nb_sim = Artist.objects.similar_url(url).count()
    if nb_sim:
        return ""
    else:
        return url
