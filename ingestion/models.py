# -*- coding: utf-8 -*-
import os, hashlib, pdb
from datetime import datetime
from xml.dom import minidom
from mp3.main.models import Artist, Vendor, ArtistVendor, Label, LabelVendor, Album




class DeliveryData(object):

    def __init__(self, **kwargs):
        for keyword in self.authorized_keywords: # Initialisation with None as default value 
            setattr(self, keyword, kwargs.pop(keyword, None)) # for all authorized keyword
        if set(kwargs.keys()).difference(set(self.authorized_keywords)): # Non authorized keyword
            raise TypeError 
                
    def __eq__(self, other):
        if set(self.__dict__.keys()).difference(other.__dict__.keys()):
            # Difference in the attributes
            return False
        # Check the values of the attributes, excluding DeliveryData attributes
        return all([self.__dict__[key]==other.__dict__[key] for key in self.__dict__.keys()\
                    if not isinstance(self.__dict__[key], DeliveryData)])
            
    def __repr__(self):
        return "%s" % self.__dict__
        
    def __hash__(self):
        hasher = hashlib.md5()
        for value in self.__dict__.values():
            hasher.update(repr(value))
        return int(hasher.hexdigest(), 16)
    
        
                
class DeliveryRelease(DeliveryData):

    authorized_keywords = ['pk', 'upc', 'title', 'territories', 'publish_date', 'publish_date_digital', 
                           'artist', 'label', 'price', 'compil']
    
    def __init__(self, **kwargs):
        super(DeliveryRelease, self).__init__(**kwargs)
        if 'territories' in kwargs and not isinstance(kwargs['territories'], tuple):
            raise TypeError
    
class DeliveryArtist(DeliveryData):
    
    authorized_keywords = ['pk', 'name', 'release']
    
    def __init__(self, **kwargs):
        super(DeliveryArtist, self).__init__(**kwargs)


class DeliveryLabel(DeliveryData):
    
    authorized_keywords = ['pk', 'name', 'realease']
    
    def __init__(self, **kwargs):
        super(DeliveryLabel, self).__init__(**kwargs)         


class DeliveryStyle(DeliveryData):

    authorized_keywords = ['name']
    
    def __init__(self, **kwargs):
        super(DeliveryStyle, self).__init__(**kwargs)         


class DeliveryTrack(DeliveryData):
    
    authorized_keywords = ['pk', 'title', 'length', 'isrc', 'disc_number', 
                           'track_number', 'bundle_only', 'audio_files',
                           'price', 'author', 'composer']
    
    def __init__(self, **kwargs):
        super(DeliveryTrack, self).__init__(**kwargs)
        
        
class DeliveryAudioFiles(DeliveryData):

    authorized_keywords = ['master', 'normal', 'sample']

    def __init__(self, **kwargs):
        super(DeliveryAudioFiles, self).__init__(**kwargs)        
        for value in kwargs.values():
            if not isinstance(value, DeliveryAudioFile):
                raise TypeError
    
    
class DeliveryAudioFile(DeliveryData):
    
    authorized_keywords = ['format', 'bitrate', 'md5', 'name', 'content', 'size', 'duration', 'path']
    
    def __init__(self, **kwargs):
        super(DeliveryAudioFile, self).__init__(**kwargs)
        if not 'size' in kwargs and 'path' in kwargs:
            self.size = int(os.path.getsize(self.path))
            


class DeliveryImage(DeliveryData):
    
    authorized_keywords = ['format', 'width', 'height', 'md5', 'name', 'path']
    
    def __init__(self, **kwargs):
        super(DeliveryImage, self).__init__(**kwargs)
        

class AbstractDelivery(object):
    
    fields = ['vendor_id', 'release', 'artist', 'label', 'image', 'tracks', 'styles', 'action']


    def __init__(self):
        for field in self.fields:
            setattr(self, field, None)


class IDOLDelivery(AbstractDelivery):
    
    date_format = '%Y-%m-%d'
    

    def __init__(self, path):
        super(IDOLDelivery, self).__init__()
        self.path = path
        basename = os.path.basename(path)
        self.xml = minidom.parse(path + '/' + basename + '.xml')
        self.vendor_id = 256
        self.action = self._action()
        if self.is_good():
            self.release = self._release()
            self.artist = self._artist()  
            self.tracks = self._tracks()
            self.image = self._image()
            self.label = self._label()
            self.styles = self._styles()
            self.release.artist = self.artist
            self.release.label = self.label
            self.label.release = self.release
            self._update_artist()
        self.xml.unlink()
        
    def __eq__(self, other):
        res = True
        for field in self.fields:
            res = res and (eval('other.' + field) == eval('self.' + field))
        return res
        
                          
    def __repr__(self):
        res = ""
        for field in ['vendor_id', 'artist', 'image', 'label']:
            try:
                attribute = eval('self.' + field)
                res = res + str(attribute)
            except AttributeError:
                pass
        return res
    
    def __hash__(self):
        hashable_fields = ['release', 'artist', 'tracks', 'image', 'label']
        hashable_string = ''
        for field in hashable_fields:
            try:
                field = eval('self.' + field)
                hashable_string = hashable_string + str(field)
            except AttributeError:
                pass
        hasher = hashlib.md5()
        hasher.update(hashable_string)
        return int(hasher.hexdigest(), 16)

    def is_good(self):
        return self.action.lower() == 'insert'
        
    def _album_node(self):
        return self.xml.getElementsByTagName("album")[0]
    
    def _action(self):
        return self._album_node().getElementsByTagName("action")[0].firstChild.data

    def _album_title(self):
        return self._album_node().getElementsByTagName("title")[0].firstChild.data

    def _release(self):
        pk = int(self.xml.getElementsByTagName("idol_id")[0].firstChild.data)
        title = self._album_title()
        upc = int(self._album_node().getElementsByTagName("upc")[0].firstChild.data)
        price = self._album_node().getElementsByTagName("price")[0]\
                                  .getElementsByTagName("name")[0].firstChild.data
        territories = tuple([node.firstChild.data for node in self.xml.getElementsByTagName("territory")])
        publish_date = datetime.strptime(self.xml.getElementsByTagName("release_date")[0].firstChild.data,
                                         self.date_format).date()
        publish_date_digital = datetime.strptime(self.xml.getElementsByTagName("digital_date")[0].firstChild.data,
                                                 self.date_format).date()
        compil = self._compil()
        return DeliveryRelease(pk=pk, title=title, territories=territories, upc=upc, price=price,
                               publish_date=publish_date, publish_date_digital=publish_date_digital,
                               compil=compil)
         
    def _artist_node(self):
        node = self.xml.getElementsByTagName("artists")[0].getElementsByTagName("artist")
        assert len(node)<=1, "Plusieurs artistes principaux"
        return node[0]
            

    def _artist_name(self):
        return self._artist_node().getElementsByTagName("name")[0].firstChild.data

    def _artist_pk(self):
        return int(self._artist_node().getElementsByTagName("idol_id")[0].firstChild.data)

    def _artist(self):
        try:
            artist_node = self._artist_node()
            return DeliveryArtist(pk=self._artist_pk(), name=self._artist_name())
        except IndexError:
            pass
    
    def _update_artist(self):
        if self.artist:
            self.artist.release = self.release
        
    def _compil(self):
        compil = self.xml.getElementsByTagName("compilation")[0].firstChild.data
        if compil == 'false':
            return False
        elif compil == 'true':
            return True
        
    def _styles(self):
        res = []
        for style in self.xml.getElementsByTagName("genres")[0].getElementsByTagName("genre"):
            res.append(DeliveryStyle(name=style.getElementsByTagName("name")[0].firstChild.data))
        return res
            
    def _image(self):
        format = 'jpg'
        ima_name = self.xml.getElementsByTagName("upc")[0].firstChild.data + '.' + format
        return DeliveryImage(format=format, width=None, height=None, md5=None,
                             name=ima_name, path=os.path.join(self.path, ima_name))

    def _label_node(self):
        return self.xml.getElementsByTagName("label")[0]

    def _label_name(self):
        return self._label_node().getElementsByTagName('name')[0].firstChild.data
                                 
    def _label_pk(self):
        return int(self._label_node().getElementsByTagName('idol_id')[0].firstChild.data)

    def _label(self):
        return DeliveryLabel(pk=self._label_pk(), name=self._label_name())    
    
    def _tracks(self):
        result = []
        for disc_node in self.xml.getElementsByTagName("discs")[0].getElementsByTagName("disc"):
            disc_number =int(disc_node.getElementsByTagName("disc_number")[0].firstChild.data)
            track_list = [self._track(track_node, disc_number)
                          for track_node in disc_node.getElementsByTagName("song")]
            result.extend(track_list)
        return result
        
    def _track(self, track_node, disc_number):
        return DeliveryTrack(pk=int(track_node.getElementsByTagName("idol_id")[0].firstChild.data),
                             title=self._track_title(track_node),
                             isrc=track_node.getElementsByTagName("isrc")[0].firstChild.data,
                             disc_number=disc_number,
                             track_number=int(track_node.getElementsByTagName("track_number")[0].firstChild.data),
                             bundle_only=self._bundle_only(track_node.getElementsByTagName("bundle_only")[0]\
                                                               .firstChild.data),
                             price=track_node.getElementsByTagName("price")[0].getElementsByTagName("name")[0].\
                                   firstChild.data,
                             author = self._role(track_node, 'author'),
                             composer = self._role(track_node, 'composer'),
                             audio_files=self._audio_files(track_node))

    def _track_title(self, track_node):
        raw_title = track_node.getElementsByTagName("title")[0].firstChild.data 
        if not self.release.compil:
            return raw_title
        else:
            return "%s - %s" % (self._track_artists_name(track_node), raw_title)

    def _track_artists_name(self, track_node):
        performers = [artist_node for artist_node in track_node.getElementsByTagName("artists")\
                          if artist_node.getElementsByTagName("artist")[0].getElementsByTagName("role")[0].\
                          firstChild.data.lower() == "performer"]
        performers_name = [performer.getElementsByTagName("artist")[0].getElementsByTagName("name")[0].firstChild.data\
                               for performer in performers]
        last_name = performers_name.pop()
        if performers_name:
            return "%s & %s" % (", ".join(performers_name), last_name)
        else:
            return last_name

    def _bundle_only(self, bundle_string):
        if bundle_string == 'false':
            return False
        elif bundle_string == 'true':
            return True

    def _role(self, track_node, role):
        """
        Rempli le champ 'author' ou composer (aggrégation de tous 'author' attachés au track
        """
        res = []
        for artist in track_node.getElementsByTagName("artists")[0].getElementsByTagName("artist"):
            if artist.getElementsByTagName("role")[0].firstChild.data.lower() == role:
                res .append(artist.getElementsByTagName("name")[0].firstChild.data)
        return ','.join(res)
                 
    def _audio_files(self, track_node):
        format = u'mp3'
        bitrate= 320 
        file_basename = track_node.getElementsByTagName("isrc")[0].firstChild.data 
        normal_filename = file_basename + '.' + format
        sample_filename = file_basename + '_preview.' + format
        
        return {'master': None,
                'normal': DeliveryAudioFile(format=format,
                                bitrate=bitrate,
                                name=normal_filename,
                                path=self.path+'/'+normal_filename,
                                duration=int(track_node.getElementsByTagName("length")[0].firstChild.data),
                                content=u'piste'),        
                'sample': DeliveryAudioFile(format=format,
                                bitrate=bitrate,
                                name=sample_filename,
                                path=self.path+'/'+sample_filename,
                                duration=30,
                                content=u'extrait')}  

    def get_track(self, pk):
        """
        To get a track by pk
        """
        for track in self.tracks:
            if track.pk == pk:
                return track
        return None

    def audiofiles(self):
        """
        Return all a list of the audiofiles of the release
        """
        audiofiles = []
        for track in self.tracks:
            audiofiles.extend([audiofile for audiofile in track.audio_files.values() if audiofile])
        return audiofiles
        
class Batch(object):

    def __init__(self, directory):
        self.directory = directory
        sub_directories = [f for f in os.listdir(self.directory) 
                                 if os.path.isdir(os.path.join(self.directory, f))]
        self.deliveries = set([IDOLDelivery(os.path.join(self.directory, sub_directory))
                               for sub_directory in sub_directories])
                               
    def __eq__(self, other):
        return (self.directory == other.directory 
                and self.deliveries == other.deliveries) 

    def good_deliveries(self):
        return set([delivery for delivery in self.deliveries if delivery.is_good()])
    
    def bad_deliveries(self):
        return set([delivery for delivery in self.deliveries if not delivery.is_good()])

    def releases(self):        
        return set([delivery.release for delivery in list(self.good_deliveries())])
        
    def artists(self):        
        return set([delivery.artist for delivery in list(self.good_deliveries())])
        
    def labels(self):        
        return set([delivery.label for delivery in list(self.good_deliveries())])
        
    def get_release(self, pk):
        for delivery in list(self.good_deliveries()):
            if delivery.release.pk == pk:
                return delivery.release

    def get_delivery(self, release_pk):
        for delivery in list(self.good_deliveries()):
            if delivery.release.pk == release_pk:
                return delivery
                
    def artists_formset_data(self):
        res = {'artist-TOTAL_FORMS': unicode(len(self.good_deliveries())), 'artist-INITIAL_FORMS': u'0', 'artist-MAX_NUM_FORMS': u'0'}
        for index, delivery in enumerate(self.good_deliveries()):
            prefix =  "artist-%s-" % index
            res[prefix + 'pk'] = unicode(delivery.artist.pk)
            res[prefix + 'name'] = unicode(delivery.artist.name)
        return res
        
    def unknown_artists(self):
        res = []
        for delivery in list(self.good_deliveries()):
            try:
                if delivery.artist:
                    Artist.objects.get(artistvendor__external_artist_id=delivery.artist.pk)
            except Artist.DoesNotExist:
                res.append(delivery.artist)                
        return set(res)

    def unknown_labels(self):
        res = []
        for delivery in list(self.good_deliveries()):
            try:
                Label.objects.get(labelvendor__external_label_id=delivery.label.pk)
            except Label.DoesNotExist:
                res.append(delivery.label)                
        return set(res)


