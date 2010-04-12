# -*- coding: utf-8 -*-

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
import re, os, pdb
from django.db import models
from mp3.main import main_localsettings

class WithPath(models.Model):

    class Meta:
        abstract = True


    def normalized_path(self):
        """
        Return the path without leading slash (if ther is one) of the audiofile
        """
        pattern = re.compile('/')
        if pattern.match(self.path):
            return self.path.replace('/', '', 1)
        return self.path

class Vendor(models.Model):
    vendor = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255, db_column='ven_name')
    ven_website = models.CharField(max_length=255, blank=True)
    ven_business = models.CharField(max_length=255, blank=True)
    ven_address = models.TextField(blank=True)
    ven_country_id = models.IntegerField(null=True, blank=True)
    ven_email = models.CharField(max_length=255, blank=True)
    ven_telephone = models.CharField(max_length=255, blank=True)
    ven_fax = models.CharField(max_length=255, blank=True)
    ven_mondomixcontact = models.CharField(max_length=255, db_column='ven_mondomixContact', blank=True) # Field name made lowercase.
    ven_followup = models.TextField(db_column='ven_followUp', blank=True) # Field name made lowercase.
    ven_dmdsigned = models.IntegerField(null=True, db_column='ven_DMDsigned', blank=True) # Field name made lowercase.
    ven_calabashid = models.CharField(max_length=255, db_column='ven_calabashID', blank=True) # Field name made lowercase.
    ven_calabashpassword = models.CharField(max_length=255, db_column='ven_calabashPassword', blank=True) # Field name made lowercase.
    ven_notes = models.TextField(blank=True)
    ven_created = models.DateField(null=True, blank=True)
    ven_modified = models.DateField(null=True, blank=True)
    mdb = models.IntegerField(db_column='MDB', default=0) # Field name made lowercase.
    mdb2 = models.IntegerField(db_column='MDB2', default=0) # Field name made lowercase.
    ven_language = models.CharField(max_length=6, blank=True)
    ven_territoires = models.CharField(max_length=255, blank=True)
    ven_cp = models.CharField(max_length=150, blank=True)
    ven_ville = models.CharField(max_length=255, blank=True)
    ven_isdistrib_on_mdx = models.IntegerField(null=True, blank=True)
    ven_isdistrib_on_mediatheque = models.IntegerField(null=True, blank=True)
    ven_isdistrib_on_ioda = models.IntegerField(null=True, blank=True)
    ven_reporting_periodicite = models.IntegerField(null=True, blank=True)
    ven_magasin_mdx_rate = models.IntegerField(null=True, blank=True)
    ven_distrib_mdx_rate = models.IntegerField(null=True, blank=True)
    ven_distrib_mediatheque_rate = models.IntegerField(null=True, blank=True)
    ven_distrib_ioda_rate = models.IntegerField(null=True, blank=True)
    ven_deduction_sacem = models.IntegerField(null=True, blank=True)
    ven_contrat_date_signature = models.DateField(null=True, blank=True)
    ven_contrat_length = models.CharField(max_length=255, blank=True)
    ven_password = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'vendor'
  
class Prix(models.Model):
    prix = models.AutoField(primary_key=True)
    pri_condition = models.CharField(max_length=255, blank=True)
    code = models.CharField(max_length=255, blank=True, db_column='pri_code')
    pri_libelle = models.CharField(max_length=255, blank=True)
    pri_prix_eur = models.IntegerField(null=True, blank=True)
    pri_note = models.TextField(blank=True)
    pri_object_type = models.IntegerField(null=True, blank=True)
    pri_prix_usd = models.IntegerField(null=True, blank=True)
    pri_prix_gbp = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'prix'
  
class Country(models.Model):
    country = models.IntegerField(primary_key=True)
    cou_name = models.CharField(max_length=255)
    cou_code = models.CharField(max_length=12, null=True, blank=True)
    cou_iso_code = models.CharField(max_length=6, blank=True, null=True)
    cou_continent = models.CharField(max_length=150, blank=True, null=True)
    cou_currency_zone = models.IntegerField(null=True, blank=True)
    cou_name_en = models.CharField(max_length=255)
    cou_continent_en = models.CharField(max_length=150, blank=True, null=True)
    cou_taxe_zone = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u'country'


class AbstractManager(models.Manager):
    """
    Abstract BaseClass for ArtistManager and LabelManager
    """
    def _build_filter(self, searched_text, search_fields):
        """
        Returns a 'OR' filter of case insensitive search of every word of the searched_text
        against every search_fields
        """
        searched_words = searched_text.split(' ')
        search_tuples = []
        for searched_word in searched_words:
            for search_field in search_fields:
                search_tuples.append((search_field, searched_word))

        last_index = len(search_tuples) - 1
        filter = ''
        for index, (search_field, searched_word) in enumerate(search_tuples):
            filter = filter + "models.Q(%s__icontains='%s')" % (search_field, searched_word)
            if index < last_index:
                filter = filter + " | "
        return eval(filter)


class LabelManager(AbstractManager):
    
    def similar_name(self, label_name):
        filter = self._build_filter(label_name, ('name',))
        return self.filter(filter)

              
class ArtistManager(AbstractManager):

    def similar_name(self, artist_name):
        filter = self._build_filter(artist_name, ('name', 'alias'))
        return self.filter(filter)

    def similar_url(self, url):
        return self.filter(url__icontains=url)

    def get_by_pk(self, pk, vendor):
        return self.get(artistvendor__external_artist_id=pk, artistvendor__vendor=vendor)


class Artist(models.Model):
    artist = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255, db_column='art_name')
    art_biography = models.TextField(null=True, blank=True, )
    art_header = models.TextField(null=True, blank=True)
    url = models.CharField(null=True, blank=True, unique=True, max_length=255, db_column='art_url_rewriting')
    art_mondomixcom_fr = models.CharField(null=True, max_length=255, blank=True)
    art_mondomixcom_en = models.CharField(null=True, max_length=255, blank=True)
    art_mondomix_id = models.IntegerField(null=True, blank=True)
    art_image = models.CharField(null=True, max_length=255, blank=True)
    art_thumbnail = models.CharField(null=True, max_length=255, blank=True)
    art_keywords = models.TextField(null=True, blank=True)
    art_website = models.CharField(null=True, max_length=255, blank=True)
    art_links_fr = models.TextField(null=True, blank=True)
    art_links_en = models.TextField(null=True, blank=True)
    art_notes = models.TextField(null=True, blank=True)
    created = models.DateField(null=True, blank=True, db_column='art_created')
    art_modified = models.DateField(null=True, blank=True)
    mdb = models.IntegerField(default=0, db_column='MDB') # Field name made lowercase.
    mdb2 = models.IntegerField(default=0, db_column='MDB2') # Field name made lowercase.
    excel = models.IntegerField(default=0, db_column='EXCEL') # Field name made lowercase.
    type = models.CharField(null=True, max_length=33, blank=True, db_column='art_type')
    art_birth_date = models.DateField(null=True, blank=True)
    art_death_date = models.DateField(null=True, blank=True)
    art_header_fr = models.TextField(null=True, blank=True)
    art_biography_fr = models.TextField(null=True, blank=True)
    art_header_en = models.TextField(null=True, blank=True)
    art_biography_en = models.TextField(null=True, blank=True)
    art_calabash_url = models.CharField(null=True, max_length=255, blank=True)
    art_calabash_genre = models.IntegerField(null=True, blank=True)
    art_calabashgenres = models.CharField(null=True, max_length=255, db_column='art_calabashGenres', blank=True) # Field name made lowercase.
    art_calabashsituation = models.TextField(null=True, db_column='art_calabashSituation', blank=True) # Field name made lowercase.
    art_calabashgenre = models.TextField(null=True, db_column='art_calabashGenre', blank=True) # Field name made lowercase.
    alias = models.TextField(null=True, blank=True, db_column='art_alias')
    art_url_rewriting2 = models.CharField(null=True, max_length=255, blank=True)
    art_ioda_id = models.IntegerField(null=True, blank=True)
    art_calimp_url_calabash = models.CharField(default='', max_length=255)
    art_calimp_id_calabash = models.IntegerField(null=True, blank=True)
    art_calimp_noteimport = models.TextField(default='')
    art_calimp_artcal_id = models.IntegerField(null=True, blank=True)
    countries = models.ManyToManyField(Country, through='ArtistCountry', null=True)
    vendors = models.ManyToManyField(Vendor, through='ArtistVendor', null=True)
    
    objects = ArtistManager()
    
    
    class Meta:
        db_table = u'artist'

    """
    def serialize(self):
        return "{\"artist\": %s, \"name\": \"%s\"}" % (self.artist, self.name)
    """
    
    
class ArtistVendor(models.Model):
    artist_vendor = models.AutoField(primary_key=True)
    artist = models.ForeignKey(Artist, db_column='artist_id')
    vendor = models.ForeignKey(Vendor, db_column='vendor_id')
    external_artist_id = models.IntegerField()
    class Meta:
        db_table = u'artist_vendor'
        unique_together = ("vendor", "external_artist_id")


class ArtistCountry(models.Model):
    artist_country = models.AutoField(primary_key=True)
    artist = models.ForeignKey(Artist, null=True, db_column='ac_artist_id')
    country = models.ForeignKey(Country, null=True, db_column='ac_country_id')
    class Meta:
        db_table = u'artist_country'


class Label(models.Model):
    label = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255, db_column='lab_name')
    created = models.DateField(null=True, blank=True, db_column='lab_created')
    lab_modified = models.DateField(null=True, blank=True)
    lab_website = models.CharField(null=True, max_length=255, blank=True)
    mdb = models.IntegerField(default=0, db_column='MDB') # Field name made lowercase.
    excel = models.IntegerField(default=0, db_column='EXCEL') # Field name made lowercase.
    lab_notes = models.TextField(blank=True, null=True)
    lab_ioda_id = models.CharField(max_length=150, null=True, blank=True)
    
    objects = LabelManager()
    
    class Meta:
        db_table = u'label'        


class LabelVendor(models.Model):
    label_vendor = models.AutoField(primary_key=True)
    label = models.ForeignKey(Label, db_column='label_id')
    vendor = models.ForeignKey(Vendor, db_column='vendor_id')
    external_label_id = models.IntegerField()
    class Meta:
        db_table = u'label_vendor'
        unique_together = ("vendor", "external_label_id")     
        
        
class Album(models.Model):
    album = models.AutoField(primary_key=True)
    title = models.CharField(default='', max_length=255, db_column='alb_title')
    alb_other_artists = models.TextField(null=True, blank=True)
    label = models.ForeignKey(Label, null=True, db_column='alb_label_id')
    alb_reference = models.CharField(null=True, max_length=255, blank=True)
    alb_record_year = models.CharField(null=True, max_length=255, blank=True)
    notes = models.TextField(null=True, blank=True, db_column='alb_notes')
    created = models.DateField(null=True, blank=True, db_column='alb_created')
    alb_modified = models.DateField(null=True, blank=True)
    mdb = models.IntegerField(default=0, db_column='MDB') # Field name made lowercase.
    mdb2 = models.IntegerField(default=0, db_column='MDB2') # Field name made lowercase.
    excel = models.PositiveIntegerField(default=0, db_column='EXCEL') # Field name made lowercase.
    alb_location_media = models.CharField(null=True, max_length=255, blank=True)
    alb_location_shop = models.CharField(null=True, max_length=255, blank=True)
    upc = models.CharField(null=True, max_length=255, blank=True, db_column='alb_barcode')
    alb_paperarticle = models.IntegerField(null=True, blank=True)
    alb_webarticle = models.CharField(null=True, max_length=255, blank=True)
    alb_calabash_url = models.CharField(null=True, max_length=255, blank=True)
    alb_calabash_online = models.DateField(null=True, blank=True)
    alb_status_indexation = models.CharField(null=True, max_length=9, blank=True)
    alb_status_files = models.CharField(null=True, max_length=9, blank=True)
    alb_status_shop = models.CharField(null=True, max_length=24, blank=True)
    alb_status_media = models.CharField(null=True, max_length=24, blank=True)
    alb_collection_id = models.IntegerField(null=True, blank=True)
    domain = models.CharField(null=True, max_length=24, blank=True, db_column='alb_domain')
    vendor = models.ForeignKey(Vendor, null=True, db_column='alb_vendor_id')
    alb_distributor_id = models.IntegerField(null=True, blank=True)
    alb_nbitems_shop = models.IntegerField(null=True, blank=True)
    alb_nbitems_media = models.IntegerField(null=True, blank=True)
    alb_publish_date = models.CharField(null=True, max_length=30, blank=True)
    alb_country_id = models.IntegerField(null=True, blank=True)
    alb_text_en = models.TextField(null=True, blank=True)
    alb_text_fr = models.TextField(null=True, blank=True)
    alb_press = models.IntegerField(null=True, blank=True)
    alb_keywords = models.TextField(null=True, blank=True)
    alb_volume = models.IntegerField(null=True, blank=True)
    alb_oldstyle = models.CharField(null=True, max_length=255, blank=True)
    alb_status_indexation_en = models.CharField(null=True, max_length=9, blank=True)
    alb_status_indexation_fr = models.CharField(null=True, max_length=9, blank=True)
    alb_calabash_status = models.CharField(null=True, max_length=21, blank=True)
    artist = models.ForeignKey(Artist, null=True, db_column='alb_artist_id')
    multiartist = models.IntegerField(default=0)
    alb_arrival_date_media = models.DateField(null=True, blank=True)
    alb_arrival_date_shop = models.DateField(null=True, blank=True)
    alb_infos_media = models.CharField(null=True, max_length=255, blank=True)
    alb_infos_shop = models.CharField(null=True, max_length=255, blank=True)
    alb_type_media = models.CharField(null=True, max_length=330, blank=True)
    alb_type_shop = models.CharField(null=True, max_length=330, blank=True)
    alb_support_type_media = models.CharField(null=True, max_length=27, blank=True)
    alb_support_type_shop = models.CharField(null=True, max_length=27, blank=True)
    alb_nb_supports_media = models.IntegerField(null=True, blank=True)
    alb_nb_supports_shop = models.IntegerField(null=True, blank=True)
    prix = models.ForeignKey(Prix, null=True, blank=True, db_column='alb_prix')
    territories = models.TextField(null=True, blank=True, db_column='alb_territoires')
    publish_date_digital = models.DateField(null=True, db_column='alb_publish_date_digital')
    publish_date = models.DateField(null=True, blank=True, db_column='alb_publish_date2')
    alb_ioda_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'album'

    def full_path(self, disc):
        return os.path.join(disc.full_path(), main_localsettings.ALBUMS_DIRECTORY, str(self.pk))

class AlbumVendor(models.Model):
    album_vendor = models.AutoField(primary_key=True)
    album = models.ForeignKey(Album, db_column='album_id')
    vendor = models.ForeignKey(Vendor, db_column='vendor_id')
    external_album_id = models.IntegerField()
    class Meta:
        db_table = u'album_vendor'
        unique_together = ("vendor", "external_album_id")     

class Disc(WithPath):
    disc = models.AutoField(primary_key=True, db_column='disk')
    name = models.CharField(max_length=255, blank=True, null=True, db_column='dik_name')
    status = models.CharField(max_length=21, blank=True, null=True, choices= ((u'default', u'default'),(u'', u''),), db_column='dik_status')
    path = models.CharField(max_length=255, blank=True, null=True, db_column='dik_path')
    mountpoint = models.CharField(max_length=255, blank=True,null=True, db_column='dik_mountpoint')
    dik_description = models.TextField(blank=True, null=True)
    class Meta:
        db_table = u'disk'

    def full_path(self):
        """
        Full path on ripmix
        """
        return os.path.join(main_localsettings.DISCOTHEQUE_BASEPATH, 
                            self.normalized_path())


class ImageFile(WithPath):
    image_file = models.AutoField(primary_key=True)
    album = models.ForeignKey(Album, null=True, db_column='ima_album_id')
    artist = models.ForeignKey(Artist, null=True, db_column='ima_artist_id')
    path = models.CharField(max_length=255, null=True, blank=True, db_column='ima_filepath')
    disc = models.ForeignKey(Disc, db_column='ima_disk_id')
    format = models.CharField(max_length=9, blank=True, db_column='ima_format')
    size = models.IntegerField(null=True, blank=True, db_column='ima_filesize')
    width = models.IntegerField(null=True, blank=True, db_column='ima_width')
    height = models.IntegerField(null=True, blank=True, db_column='ima_height')
    quality = models.IntegerField(null=True, blank=True, db_column='ima_quality')
    usage = models.CharField(max_length=60, blank=True, db_column='ima_usage')
    
    class Meta:
        db_table = u'image_file'
        

    def full_path(self):
        """
        Full path on ripmix
        """
        return os.path.join(self.disc.full_path(),
                            self.normalized_path())
        

class Track(models.Model):
    track = models.AutoField(primary_key=True)
    album = models.ForeignKey(Album, db_column='tra_album_id')
    disc_number = models.IntegerField(null=True, blank=True, db_column='tra_support_number')
    track_number = models.IntegerField(null=True, blank=True, db_column='tra_track_number')
    title = models.CharField(max_length=255, db_column="tra_title")
    tra_price = models.IntegerField(null=True, blank=True)
    isrc = models.CharField(max_length=36, null=True, blank=True, db_column='tra_ISRC') # Field name made lowercase.
    tra_status = models.CharField(max_length=27, blank=True)
    tra_created = models.DateField(null=True, blank=True)
    tra_modified = models.DateField(null=True, blank=True)
    mdb = models.IntegerField(db_column='MDB', default=0) # Field name made lowercase.
    mdb2 = models.IntegerField(db_column='MDB2', default=0) # Field name made lowercase.
    tra_artist_id = models.IntegerField(null=True, blank=True)
    prix = models.ForeignKey(Prix, null=True, blank=True, db_column="tr_prix")
    tra_mdxteam_rating = models.IntegerField(null=True, blank=True)
    vente_alalbum = models.IntegerField(null=True, blank=True, db_column="tra_vente_albumbundle_only")
    vente_autitre = models.IntegerField(null=True, blank=True, db_column="tra_vente_track_only")
    tr_notes = models.TextField(blank=True)
    tra_ioda_id = models.IntegerField(null=True, blank=True)
    author = models.CharField(default='', max_length=255, db_column="tra_author")
    composer = models.CharField(default='', max_length=255, db_column="tra_composer")
    class Meta:
        db_table = u'track'


class TrackVendor(models.Model):
    track_vendor = models.AutoField(primary_key=True)
    track = models.ForeignKey(Track, unique=True, db_column='track_id')
    external_track_id = models.IntegerField()
    
    class Meta:
        db_table = u'track_vendor'



class AudioFile(WithPath):
    audio_file = models.AutoField(primary_key=True)
    path = models.CharField(max_length=255, blank=True, db_column='aud_filepath')
    disc = models.ForeignKey(Disc, null=True, db_column='aud_disk_id')
    content = models.CharField(max_length=21, null=True, blank=True, db_column='aud_content')
    format = models.CharField(max_length=12, null=True, blank=True, db_column='aud_format')
    size = models.IntegerField(null=True, blank=True, db_column='aud_filesize')
    duration = models.IntegerField(null=True, blank=True, db_column='aud_duration')
    bitrate = models.IntegerField(null=True, blank=True, db_column='aud_bitrate')
    aud_frequency = models.IntegerField(null=True, blank=True)
    aud_mode = models.CharField(max_length=36, null=True, blank=True)
    track = models.ForeignKey(Track, null=True, blank=True, db_column='aud_track_id')
    aud_tags = models.IntegerField(null=True, blank=True)
    aud_iodaimp_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'audio_file'
    """
    def normalized_path(self):
        
        Return the path without leading slash (if ther is one) of the audiofile
        
        pattern = re.compile('/')
        if pattern.match(self.path):
            return self.path.replace('/', '', 1)
        return self.path
    """
    def full_path(self):
        return os.path.join(self.disc.full_path(), self.normalized_path())
 
class ActualitesDisque(models.Model):
    actualites_disque = models.IntegerField(primary_key=True)
    ad_semaine = models.CharField(max_length=255, blank=True)
    ad_date_creation = models.DateTimeField(null=True, blank=True)
    album1 = models.ForeignKey(Album, related_name='actu_disque1', db_column='ad_album1')
    album2 = models.ForeignKey(Album, related_name='actu_disque2', db_column='ad_album2')
    album3 = models.ForeignKey(Album, related_name='actu_disque3', db_column='ad_album3')
    localisation = models.IntegerField(null=True, blank=True, db_column='ad_localisation')
    class Meta:
        db_table = u'actualites_disque'
        
class CoupsDeCoeur(models.Model):
    coups_de_coeur = models.IntegerField(primary_key=True)
    cdc_label = models.CharField(max_length=255, blank=True)
    album1 = models.ForeignKey(Album, related_name='cdp1', db_column='cdc_album1')
    album2 = models.ForeignKey(Album, related_name='cdp2', db_column='cdc_album2')
    album3 = models.ForeignKey(Album, related_name='cdp3', db_column='cdc_album3')
    cdc_date_creation = models.DateField(null=True, blank=True)
    localisation = models.IntegerField(null=True, blank=True, db_column='cdc_localisation')
    class Meta:
        db_table = u'coups_de_coeur'

class Carrousels(models.Model):
    carrousels = models.IntegerField(primary_key=True)
    car_titre = models.CharField(max_length=255, blank=True)
    car_langue = models.IntegerField(null=True, blank=True)
    car_pagegenre = models.IntegerField(null=True, blank=True)
    car_pagecontinent = models.IntegerField(null=True, blank=True)
    album1 = models.ForeignKey(Album, related_name='carousel1', db_column='car_album1')
    album2 = models.ForeignKey(Album, related_name='carousel2', db_column='car_album2')
    album3 = models.ForeignKey(Album, related_name='carousel3', db_column='car_album3')
    album4 = models.ForeignKey(Album, related_name='carousel4', db_column='car_album4')
    album5 = models.ForeignKey(Album, related_name='carousel5', db_column='car_album5')
    album6 = models.ForeignKey(Album, related_name='carousel6', db_column='car_album6')
    album7 = models.ForeignKey(Album, related_name='carousel7', db_column='car_album7')
    album8 = models.ForeignKey(Album, related_name='carousel8', db_column='car_album8')
    album9 = models.ForeignKey(Album, related_name='carousel9', db_column='car_album9')
    album10 = models.ForeignKey(Album, related_name='carousel10', db_column='car_album10')
    album11 = models.ForeignKey(Album, related_name='carousel11', db_column='car_album11')
    album13 = models.ForeignKey(Album, related_name='carousel12', db_column='car_album12')
    album12 = models.ForeignKey(Album, related_name='carousel13', db_column='car_album13')
    album15 = models.ForeignKey(Album, related_name='carousel14', db_column='car_album14')
    album14 = models.ForeignKey(Album, related_name='carousel15', db_column='car_album15')
    album17 = models.ForeignKey(Album, related_name='carousel16', db_column='car_album16')
    album16 = models.ForeignKey(Album, related_name='carousel17', db_column='car_album17')
    album19 = models.ForeignKey(Album, related_name='carousel18', db_column='car_album18')
    album18 = models.ForeignKey(Album, related_name='carousel19', db_column='car_album19')
    album20 = models.ForeignKey(Album, related_name='carousel20', db_column='car_album20')
    car_date_creation = models.DateField(null=True, blank=True)
    car_date_maj = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'carrousels'

class Affiliate(models.Model):
    affiliate = models.IntegerField(primary_key=True)
    aff_nom = models.CharField(max_length=255, blank=True)
    aff_url = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'affiliate'

class Aidefaq(models.Model):
    aidefaq = models.IntegerField(primary_key=True)
    aid_categorieaide = models.IntegerField(null=True, blank=True)
    aid_order = models.IntegerField(null=True, blank=True)
    aid_texte = models.TextField(blank=True)
    aid_titre = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'aidefaq'




class AlbumArtist(models.Model):
    album_artist = models.IntegerField(primary_key=True)
    aa_album_id = models.IntegerField(null=True, blank=True)
    aa_artist_id = models.IntegerField(null=True, blank=True)
    excel = models.IntegerField(db_column='EXCEL') # Field name made lowercase.
    class Meta:
        db_table = u'album_artist'

class AlbumCountry(models.Model):
    album_country = models.IntegerField(primary_key=True)
    alco_album_id = models.IntegerField(null=True, blank=True)
    alco_country_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'album_country'

class AlbumInstrument(models.Model):
    album_instrument = models.IntegerField(primary_key=True)
    alin_album_id = models.IntegerField(null=True, blank=True)
    alin_instrument_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'album_instrument'

class AlbumStyle(models.Model):
    album_style = models.IntegerField(primary_key=True)
    as_style_id = models.IntegerField(null=True, blank=True)
    as_album_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'album_style'

class Article(models.Model):
    article = models.IntegerField(primary_key=True)
    atc_type = models.CharField(max_length=27, blank=True)
    atc_language_id = models.CharField(max_length=255, blank=True)
    atc_title = models.CharField(max_length=255, blank=True)
    atc_header = models.TextField(blank=True)
    atc_text = models.TextField(blank=True)
    atc_author = models.CharField(max_length=255, blank=True)
    atc_origin = models.CharField(max_length=255, blank=True)
    atc_publishing_date = models.DateField(null=True, blank=True)
    atc_created = models.DateField(null=True, blank=True)
    atc_modified = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'article'




class ArtistNoimportcalabash(models.Model):
    artist = models.IntegerField(primary_key=True)
    art_name = models.CharField(unique=True, max_length=255)
    art_biography = models.TextField(blank=True)
    art_header = models.TextField(blank=True)
    art_url_rewriting = models.CharField(max_length=255, blank=True)
    art_mondomixcom_fr = models.CharField(max_length=255, blank=True)
    art_mondomixcom_en = models.CharField(max_length=255, blank=True)
    art_mondomix_id = models.IntegerField(null=True, blank=True)
    art_image = models.CharField(max_length=255, blank=True)
    art_thumbnail = models.CharField(max_length=255, blank=True)
    art_keywords = models.TextField(blank=True)
    art_website = models.CharField(max_length=255, blank=True)
    art_links_fr = models.TextField(blank=True)
    art_links_en = models.TextField(blank=True)# -*- coding: utf-8 -*-
    art_notes = models.TextField(blank=True)
    art_created = models.DateField(null=True, blank=True)
    art_modified = models.DateField(null=True, blank=True)
    mdb = models.IntegerField(db_column='MDB') # Field name made lowercase.
    mdb2 = models.IntegerField(db_column='MDB2') # Field name made lowercase.
    excel = models.IntegerField(db_column='EXCEL') # Field name made lowercase.
    art_type = models.CharField(max_length=33, blank=True)
    art_birth_date = models.DateField(null=True, blank=True)
    art_death_date = models.DateField(null=True, blank=True)
    art_header_fr = models.TextField(blank=True)
    art_biography_fr = models.TextField(blank=True)
    art_header_en = models.TextField(blank=True)
    art_biography_en = models.TextField(blank=True)
    art_calabash_url = models.CharField(max_length=255, blank=True)
    art_calabash_genre = models.IntegerField(null=True, blank=True)
    art_calabashgenres = models.CharField(max_length=255, db_column='art_calabashGenres', blank=True) # Field name made lowercase.
    art_calabashsituation = models.TextField(db_column='art_calabashSituation', blank=True) # Field name made lowercase.
    art_calabashgenre = models.TextField(db_column='art_calabashGenre', blank=True) # Field name made lowercase.
    art_alias = models.TextField(blank=True)
    art_url_rewriting2 = models.CharField(max_length=255, blank=True)
    art_ioda_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'artist_noimportcalabash'



class Auteur(models.Model):
    auteur = models.IntegerField(primary_key=True)
    aut_login = models.CharField(unique=True, max_length=60)
    aut_lastname = models.CharField(max_length=75, blank=True)
    aut_firstname = models.CharField(max_length=75, blank=True)
    aut_pwd = models.CharField(max_length=150, blank=True)
    aut_privilege = models.IntegerField(null=True, blank=True)
    aut_email = models.CharField(max_length=240)
    aut_active = models.CharField(max_length=3, blank=True)
    aut_type = models.CharField(max_length=21)
    aut_reportto = models.CharField(max_length=60, blank=True)
    class Meta:
        db_table = u'auteur'

class BugTracking(models.Model):
    bug_tracking = models.IntegerField(primary_key=True)
    bt_raw_datas = models.TextField()
    bt_timestamp = models.DateTimeField()
    class Meta:
        db_table = u'bug_tracking'

class Cadi007(models.Model):
    cadi_007 = models.IntegerField(primary_key=True)
    cadi_jstag = models.CharField(max_length=255)
    cadi_ip = models.CharField(max_length=255)
    cadi_session = models.CharField(max_length=255)
    cadi_cookie = models.CharField(max_length=255)
    cadi_url = models.CharField(max_length=255)
    cadi_datetime = models.DateTimeField()
    class Meta:
        db_table = u'cadi_007'

class CalabashGenre(models.Model):
    calabash_genre = models.IntegerField(primary_key=True)
    cag_name = models.CharField(max_length=255, blank=True)
    cag_number = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'calabash_genre'

class Calabashdownloads(models.Model):
    calabashdownloads = models.IntegerField(primary_key=True)
    cdw_track_item_id = models.IntegerField()
    cdw_album_item_id = models.IntegerField()
    cdw_artist_item_id = models.IntegerField()
    cdw_tracktitle = models.TextField()
    cdw_albumname = models.TextField()
    cdw_artistname = models.TextField()
    cdw_artist_url_calabash = models.CharField(max_length=255)
    cdw_artist_url_mondomix = models.CharField(max_length=255)
    cdw_pathmp3 = models.TextField()
    cdw_filesize = models.CharField(max_length=255)
    cdw_mimetype = models.CharField(max_length=255)
    class Meta:
        db_table = u'calabashdownloads'

class CalabashdownloadsAccount(models.Model):
    account_calabashdownloads = models.IntegerField(primary_key=True)
    adl_account = models.IntegerField()
    adl_calabashdownloads = models.IntegerField()
    adl_orderdate = models.DateTimeField()
    class Meta:
        db_table = u'calabashdownloads_account'

class Categorieaide(models.Model):
    categorieaide = models.IntegerField(primary_key=True)
    cat_version = models.IntegerField(null=True, blank=True)
    cat_order = models.IntegerField(null=True, blank=True)
    cat_titremenu = models.CharField(max_length=255, blank=True)
    cat_titrelong = models.TextField(blank=True)
    class Meta:
        db_table = u'categorieaide'

class Category(models.Model):
    category = models.IntegerField(primary_key=True)
    cat_name = models.CharField(unique=True, max_length=255)
    cat_order = models.IntegerField(unique=True, null=True, blank=True)
    cat_created = models.DateField(null=True, blank=True)
    cat_modified = models.DateField(null=True, blank=True)
    cat_name_en = models.CharField(max_length=255)
    class Meta:
        db_table = u'category'

class CategoryStyle(models.Model):
    category_style = models.IntegerField(primary_key=True)
    cs_style_id = models.IntegerField(null=True, blank=True)
    cs_category_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'category_style'

class Collection(models.Model):
    collection = models.IntegerField()
    col_name = models.CharField(max_length=255, blank=True)
    excel = models.IntegerField(db_column='EXCEL') # Field name made lowercase.
    col_notes = models.TextField(blank=True)
    col_created = models.DateField(null=True, blank=True)
    col_modified = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'collection'

class Commentaires(models.Model):
    commentaires = models.IntegerField(primary_key=True)
    com_user_id = models.CharField(max_length=255, blank=True)
    com_titre = models.CharField(max_length=255, blank=True)
    com_texte = models.TextField(blank=True)
    com_date_creation = models.DateTimeField(null=True, blank=True)
    com_ispublished = models.IntegerField(null=True, db_column='com_isPublished', blank=True) # Field name made lowercase.
    com_album_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'commentaires'

class Contact(models.Model):
    contact = models.IntegerField(primary_key=True)
    con_name = models.CharField(max_length=255, blank=True)
    con_position = models.CharField(max_length=255, blank=True)
    con_address = models.TextField(blank=True)
    con_country_id = models.IntegerField(null=True, blank=True)
    con_phone = models.CharField(max_length=255, blank=True)
    con_mobile = models.CharField(max_length=255, blank=True)
    con_fax = models.CharField(max_length=255, blank=True)
    con_email = models.CharField(max_length=255, blank=True)
    con_vendor_id = models.IntegerField(null=True, blank=True)
    con_distributor_id = models.IntegerField(null=True, blank=True)
    con_label_id = models.IntegerField(null=True, blank=True)
    con_artist_id = models.IntegerField(null=True, blank=True)
    con_notes = models.TextField(blank=True)
    con_created = models.DateField(null=True, blank=True)
    con_modified = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'contact'



class CountryBackup(models.Model):
    country = models.IntegerField(primary_key=True)
    cou_name = models.CharField(max_length=255)
    cou_code = models.CharField(max_length=12, blank=True)
    cou_iso_code = models.CharField(max_length=6, blank=True)
    cou_created = models.DateField(null=True, blank=True)
    cou_modified = models.DateField(null=True, blank=True)
    image = models.TextField(blank=True)
    class Meta:
        db_table = u'country_backup'


class ProfilSessions(models.Model):
    profil_sessions = models.AutoField(primary_key=True)
    session_id = models.CharField(max_length=255, blank=True, db_column='ps_session_id', unique=True)
    user_ip = models.CharField(max_length=90, blank=True, db_column='ps_user_ip')
    useraccount_id = models.IntegerField(null=True, blank=True, db_column='ps_useraccount_id')
    ps_date_start = models.DateTimeField(null=True, blank=True)
    ps_store_id = models.IntegerField(null=True, blank=True)
    ps_localtime = models.CharField(max_length=15)
    ps_session_dotcom = models.CharField(max_length=255, db_column='ps_session_dotCom', blank=True) # Field name made lowercase.
    ps_date_end = models.DateTimeField(null=True, blank=True)
    ps_cadi_cookie = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=3, blank=True, default='', db_column='ps_country')
    class Meta:
        db_table = u'profil_sessions'


class Paniers(models.Model):
    paniers = models.AutoField(primary_key=True)
    session = models.ForeignKey(ProfilSessions,  db_column='pa_user_session', to_field='session_id')
    pa_date_start = models.DateTimeField(null=True, blank=True)
    pa_date_end = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'paniers'

class CountryIp(models.Model):
    country_ip = models.IntegerField(primary_key=True)
    ip_from = models.FloatField(db_column='ci_ip_from')
    ip_to = models.FloatField(db_column='ci_ip_to')
    country_code2 = models.CharField(max_length=6, db_column='ci_country_code2')
    country_code3 = models.CharField(max_length=9, db_column='ci_country_code3')
    ci_country_name = models.CharField(max_length=300)
    class Meta:
        db_table = u'country_ip'



class CountryIsoEn(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=6)
    class Meta:
        db_table = u'country_iso_en'



class Credits(models.Model):
    credits = models.IntegerField(primary_key=True)
    cre_libelle_fr = models.CharField(max_length=255, blank=True)
    cre_nb_credit = models.IntegerField(null=True, blank=True)
    cre_prix = models.IntegerField(null=True, blank=True)
    cre_validite = models.IntegerField(null=True, blank=True)
    cre_libelle_en = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'credits'

class Currency(models.Model):
    currency = models.IntegerField(primary_key=True)
    cur_name = models.CharField(max_length=9)
    class Meta:
        db_table = u'currency'


class Distributor(models.Model):
    distributor = models.IntegerField(primary_key=True)
    dis_name = models.CharField(unique=True, max_length=255)
    dis_website = models.CharField(max_length=255, blank=True)
    dis_notes = models.TextField(blank=True)
    excel = models.IntegerField(db_column='EXCEL') # Field name made lowercase.
    dis_created = models.DateField(null=True, blank=True)
    dis_modified = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'distributor'

class Eticket(models.Model):
    eticket = models.IntegerField(primary_key=True)
    eti_profile = models.IntegerField()
    eti_mail = models.CharField(max_length=255)
    eti_nom = models.CharField(max_length=255)
    eti_prenom = models.CharField(max_length=255)
    eti_subject = models.CharField(max_length=255)
    eti_message = models.TextField()
    eti_reply = models.TextField()
    eti_priority = models.IntegerField()
    eti_datetime = models.DateTimeField()
    eti_os = models.CharField(max_length=255)
    eti_browser = models.CharField(max_length=255)
    eti_language = models.CharField(max_length=255)
    eti_status = models.CharField(max_length=60)
    class Meta:
        db_table = u'eticket'

class GenresFocus(models.Model):
    genres_focus = models.IntegerField(primary_key=True)
    gf_label = models.CharField(max_length=255, blank=True)
    gf_album1 = models.IntegerField(null=True, blank=True)
    gf_album2 = models.IntegerField(null=True, blank=True)
    gf_album3 = models.IntegerField(null=True, blank=True)
    gf_localisation = models.IntegerField(null=True, blank=True)
    gf_album4 = models.IntegerField(null=True, blank=True)
    gf_album5 = models.IntegerField(null=True, blank=True)
    gf_album6 = models.IntegerField(null=True, blank=True)
    gf_date_creation = models.DateField(null=True, blank=True)
    gf_album_master = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'genres_focus'

class HighlightTypes(models.Model):
    highlight_types = models.IntegerField(primary_key=True)
    ht_label = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'highlight_types'


class ImageFileNoimportcalabash(models.Model):
    image_file = models.IntegerField(primary_key=True)
    ima_album_id = models.IntegerField(null=True, blank=True)
    ima_artist_id = models.IntegerField(null=True, blank=True)
    ima_filepath = models.CharField(max_length=255, blank=True)
    ima_disk_id = models.IntegerField(null=True, blank=True)
    ima_format = models.CharField(max_length=9, blank=True)
    ima_filesize = models.IntegerField(null=True, blank=True)
    ima_width = models.IntegerField(null=True, blank=True)
    ima_height = models.IntegerField(null=True, blank=True)
    ima_quality = models.IntegerField(null=True, blank=True)
    ima_usage = models.CharField(max_length=60, blank=True)
    class Meta:
        db_table = u'image_file_noimportcalabash'

class Instrument(models.Model):
    instrument = models.IntegerField(primary_key=True)
    ins_name = models.CharField(max_length=255, blank=True)
    ins_name_en = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'instrument'


class Languages(models.Model):
    languages = models.IntegerField(primary_key=True)
    lan_name = models.CharField(max_length=255, blank=True)
    lan_code = models.CharField(max_length=30, blank=True)
    lan_created = models.DateField(null=True, blank=True)
    lan_currency_symbol = models.CharField(max_length=30, blank=True)
    lan_currency_code = models.CharField(max_length=30, blank=True)
    lan_currency_convertaux = models.CharField(max_length=30, db_column='lan_currency_converTaux', blank=True) # Field name made lowercase.
    lan_format_date = models.CharField(max_length=60, blank=True)
    lan_currency_label_zone = models.CharField(max_length=450, blank=True)
    class Meta:
        db_table = u'languages'

class LogRecherche(models.Model):
    recherche_id = models.IntegerField(primary_key=True)
    session_id = models.CharField(max_length=300)
    visit_at = models.DateTimeField()
    keywords = models.TextField()
    class Meta:
        db_table = u'log_recherche'

class MdbCountry(models.Model):
    pays = models.TextField()
    code_pays = models.TextField()
    italien = models.TextField()
    espagnol = models.TextField()
    anglais = models.TextField()
    allemand = models.TextField()
    indicatif = models.TextField()
    class Meta:
        db_table = u'mdb_country'

class Multiartist(models.Model):
    album = models.IntegerField(primary_key=True)
    nb = models.IntegerField()
    class Meta:
        db_table = u'multiartist'

class Newsletter(models.Model):
    newsletter = models.IntegerField(primary_key=True)
    nl_email = models.CharField(max_length=255)
    nl_langue = models.CharField(max_length=30)
    nl_date_creation = models.DateField()
    nl_session_id = models.CharField(max_length=255)
    nl_imported = models.CharField(max_length=3)
    class Meta:
        db_table = u'newsletter'

class ValidatedOrdersManager(models.Manager):
    """
    Return all validated orders 
    """
    def get_query_set(self):
        return super(ValidatedOrdersManager, self).get_query_set()\
        .filter(models.Q(payment_status='Completed') | models.Q(payment_status='Canceled_Reversal'))\
        .filter(validation_date__isnull=False)

class Orders(models.Model):

    orders = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=True, blank=True, db_column='ord_user_id')
    panier_id = models.IntegerField(db_column='ord_cart_id', null=True)
    ord_price = models.FloatField(null=True, blank=True)
    ord_status = models.CharField(max_length=75, null=True, blank=True)
    pp_txn_id = models.CharField(max_length=75, null=True, blank=True)
    payment_status = models.CharField(max_length=75, null=True,  blank=True, db_column='pp_payment_status')
    pp_payer_id = models.CharField(max_length=75, blank=True, null=True)
    pp_payer_status = models.CharField(max_length=75, blank=True, null=True, )
    pp_mc_gross = models.FloatField(null=True, blank=True)
    pp_mc_fee = models.FloatField(null=True, blank=True)
    pp_mc_currency = models.CharField(max_length=9, null=True, blank=True)
    pp_residence_country = models.CharField(null=True, max_length=9)
    pp_settle_amount = models.FloatField(null=True)
    pp_exchange_rate = models.FloatField(null=True)
    pp_reason_code = models.CharField(null=True, max_length=255)
    pp_pending_reason = models.CharField(null=True, max_length=255)
    pp_raw_datas = models.TextField(null=True, blank=True)
    ord_created = models.DateTimeField(null=True, blank=True)
    ord_modified = models.DateTimeField(null=True, blank=True)
    validation_date = models.DateTimeField(null=True, blank=True, db_column='ord_validated')
    
    objects = models.Manager()
    validated_objects = ValidatedOrdersManager()
    
    class Meta:
        db_table = u'orders'

class PanierItems(models.Model):
    panier_items = models.AutoField(primary_key=True)
    object_id = models.IntegerField(null=True, blank=True, db_column='pi_object_id')
    object_type = models.IntegerField(null=True, blank=True, db_column='pi_object_type')
    panier_id = models.IntegerField(null=True, blank=True, db_column='pi_panier_id')
    pi_date_update = models.DateTimeField(null=True, blank=True)
    date_suppr = models.DateTimeField(null=True, blank=True, db_column='pi_date_suppr')
    pi_date_dl = models.DateTimeField(db_column='pi_date_DL') # Field name made lowercase.
    pi_object_official_current_price = models.FloatField()
    pi_objet_real_current_price = models.FloatField()
    class Meta:
        db_table = u'panier_items'

class PanierItemsFinance(models.Model):
    panier_items_finance = models.IntegerField(primary_key=True)
    pif_panier_item = models.IntegerField()
    pif_object_parent_id = models.IntegerField()
    pif_object_parent_type = models.IntegerField()
    pif_object_type = models.IntegerField()
    pif_object_id = models.IntegerField()
    pif_object_price_l10n = models.FloatField()
    pif_object_parent_price_l10n = models.FloatField()
    pif_currency = models.CharField(max_length=15)
    pif_exchange_rate = models.FloatField()
    pif_residence_country = models.CharField(max_length=15)
    pif_txn_type = models.CharField(max_length=255)
    pif_ord_validated = models.DateTimeField()
    pif_datetime = models.DateTimeField()
    class Meta:
        db_table = u'panier_items_finance'



class Pays(models.Model):
    pays = models.IntegerField(primary_key=True)
    pay_nom = models.CharField(max_length=192, blank=True)
    eng_pay_nom = models.CharField(max_length=255)
    pay_isocode2 = models.CharField(max_length=6, blank=True)
    pay_continent = models.CharField(max_length=150)
    class Meta:
        db_table = u'pays'

class Platform(models.Model):
    platform = models.IntegerField(primary_key=True)
    pla_name = models.CharField(max_length=255)
    pla_code = models.CharField(max_length=255)
    class Meta:
        db_table = u'platform'
        
        
"""
class Prefs(models.Model):
    prf_auteur = models.CharField(max_length=60, primary_key=True)
    prf_class = models.CharField(max_length=90, primary_key=True)
    prf_fieldname = models.CharField(max_length=120, primary_key=True)
    prf_affichage = models.CharField(max_length=9)
    prf_affichageapercu = models.CharField(max_length=9)
    prf_actiondata_subs = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'prefs'
"""



class PrixHistorique(models.Model):
    prix_historique = models.IntegerField(primary_key=True)
    ph_modification_date = models.DateTimeField(null=True, blank=True)
    ph_objet_id = models.IntegerField(null=True, blank=True)
    ph_objet_type = models.IntegerField(null=True, blank=True)
    ph_objet_prix_eur = models.IntegerField(null=True, blank=True)
    ph_objet_prix_usd = models.IntegerField(null=True, blank=True)
    ph_objet_prix_gbp = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'prix_historique'

class Profil(models.Model):
    profil = models.IntegerField(primary_key=True)
    pro_wallet_mdx_solde = models.IntegerField(null=True, blank=True)
    pro_wallet_clb_solde = models.IntegerField(null=True, blank=True)
    pro_mondomix_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'profil'

class ProfilBackupmigration(models.Model):
    profil = models.IntegerField(primary_key=True)
    pro_email = models.CharField(max_length=255, blank=True)
    pro_password = models.CharField(max_length=255, blank=True)
    pro_genre = models.IntegerField(null=True, blank=True)
    pro_datebirth = models.CharField(max_length=255, blank=True)
    pro_language = models.IntegerField(null=True, blank=True)
    pro_createdatetime = models.DateField(null=True, blank=True)
    pro_firstname = models.CharField(max_length=255, blank=True)
    pro_name = models.CharField(max_length=255, blank=True)
    pro_wallet_solde = models.IntegerField(null=True, blank=True)
    pro_isactived = models.IntegerField(null=True, db_column='pro_isActived', blank=True) # Field name made lowercase.
    pro_date_activation = models.DateField(null=True, blank=True)
    pro_typeuser = models.IntegerField(null=True, db_column='pro_typeUser', blank=True) # Field name made lowercase.
    pro_photo = models.TextField(blank=True)
    pro_mondomix_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'profil_backupmigration'

class ProfilOldbeforeimportcalabash(models.Model):
    profil = models.IntegerField(primary_key=True)
    pro_wallet_mdx_solde = models.IntegerField(null=True, blank=True)
    pro_wallet_clb_solde = models.IntegerField(null=True, blank=True)
    pro_mondomix_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'profil_oldbeforeimportcalabash'



class ProjectArtist(models.Model):
    project_artist = models.IntegerField(primary_key=True)
    prar_project_id = models.IntegerField(null=True, blank=True)
    prar_artist_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'project_artist'

class Promotions(models.Model):
    promotions = models.IntegerField(primary_key=True)
    pr_libelle = models.CharField(max_length=255, blank=True)
    pr_img_homepage = models.TextField(blank=True)
    pr_texte = models.TextField(blank=True)
    pr_image = models.TextField(blank=True)
    pr_prix_id = models.IntegerField(null=True, blank=True)
    pr_date_start = models.DateField(null=True, blank=True)
    pr_date_stop = models.DateField(null=True, blank=True)
    pr_promo_pageid = models.IntegerField(null=True, blank=True)
    pr_image_alt = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'promotions'

class Radioplaylist(models.Model):
    radioplaylist = models.IntegerField(primary_key=True)
    rad_statut = models.CharField(max_length=150)
    rad_name = models.CharField(max_length=255)
    class Meta:
        db_table = u'radioplaylist'

class Radiotracks(models.Model):
    radiotracks = models.IntegerField(primary_key=True)
    rad_radioplaylist = models.IntegerField()
    rad_trackid = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'radiotracks'

class Rating(models.Model):
    rating = models.IntegerField(primary_key=True)
    rat_user_id = models.CharField(max_length=255, blank=True)
    rat_album_id = models.IntegerField(null=True, blank=True)
    rat_score = models.IntegerField(null=True, blank=True)
    rat_date_creation = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'rating'

class SendToFriend(models.Model):
    send_to_friend = models.IntegerField(primary_key=True)
    s2f_user_id = models.CharField(max_length=255, blank=True)
    s2f_texte = models.CharField(max_length=255, blank=True)
    s2f_album_id = models.IntegerField(null=True, blank=True)
    s2f_email_to = models.CharField(max_length=255, blank=True)
    s2f_date_creation = models.DateTimeField(null=True, blank=True)
    s2f_nom_from = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'send_to_friend'

class Statement(models.Model):
    id = models.IntegerField(primary_key=True)
    sta_year = models.IntegerField()
    sta_quarter = models.IntegerField()
    sta_platform_name = models.CharField(max_length=255)
    sta_provider_name = models.CharField(max_length=255)
    sta_track_title = models.CharField(max_length=255)
    sta_artist_name = models.CharField(max_length=255)
    sta_album_title = models.CharField(max_length=255)
    sta_quantity = models.IntegerField()
    sta_net_price = models.FloatField(null=True, blank=True)
    sta_provider_rate = models.FloatField()
    sta_track_isrc = models.CharField(max_length=36, blank=True)
    sta_track_id = models.IntegerField(null=True, blank=True)
    sta_track_nb = models.IntegerField(null=True, blank=True)
    sta_track_cd_nb = models.IntegerField(null=True, blank=True)
    sta_artist_id = models.IntegerField(null=True, blank=True)
    sta_album_id = models.IntegerField(null=True, blank=True)
    sta_provider_id = models.IntegerField(null=True, blank=True)
    sta_platform_id = models.IntegerField()
    class Meta:
        db_table = u'statement'

class Statistiques(models.Model):
    statistiques = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u'statistiques'

class Style(models.Model):
    style = models.IntegerField(primary_key=True)
    sty_name = models.CharField(unique=True, max_length=255)
    sty_created = models.DateField(null=True, blank=True)
    sty_modified = models.DateField(null=True, blank=True)
    sty_name_en = models.CharField(max_length=255)
    class Meta:
        db_table = u'style'



class XportMp3Img(models.Model):
    termine = models.IntegerField(primary_key=True)
    objet_id = models.IntegerField()
    objet_type = models.CharField(max_length=255)
    date_validation = models.DateTimeField()
    is_uploaded = models.IntegerField()
    date_upload = models.DateTimeField()
    objet_disk = models.IntegerField()
    class Meta:
        db_table = u'xport_mp3_img'

