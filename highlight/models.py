# -*- coding: utf-8 -*-

from django.db import models


class Highlight(models.Model):
    highlights = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, db_column='hig_title')
    subtitle = models.CharField(max_length=255, blank=True, db_column='hig_subtitle')
    text = models.CharField(max_length=255, blank=True, db_column='hig_texte')
    img = models.TextField(blank=True, db_column='hig_image')
    link = models.CharField(max_length=255, blank=True, db_column='hig_link')
    
    creadate = models.DateField(null=True, blank=True, db_column='hig_creadate')
    hig_link2 = models.CharField(max_length=255, blank=True)
    hig_title_color = models.CharField(max_length=255, blank=True)
    hig_postext = models.IntegerField(null=True, blank=True)
    hig_subtitle_color = models.CharField(max_length=255, blank=True)
    hig_majdate = models.DateField(null=True, blank=True)
    slide_type = models.IntegerField(null=True, blank=True, db_column='hig_slide_type')
    langue = models.IntegerField(null=True, blank=True, db_column='hig_version')
    class Meta:
        db_table = u'highlights'

    def img_fullpath(self):
        return "media/publish/highlights/%s" % (self.img,)


class Alaune(models.Model):
    alaune = models.IntegerField(primary_key=True)
    titre = models.CharField(max_length=255, blank=True, db_column='ala_titre')
    langue = models.IntegerField(null=True, blank=True, db_column='ala_langue')
    location = models.IntegerField(null=True, blank=True, db_column='ala_page_type')
    highlights = models.ManyToManyField(Highlight, through='AlauneHighlight', null=True)
    class Meta:
        db_table = u'alaune'


class AlauneHighlight(models.Model):
    alaune_highlight = models.IntegerField(primary_key=True)
    position = models.IntegerField(null=True, blank=True, db_column='ahl_position')
    alaune = models.ForeignKey(Alaune, db_column='ahl_alaune')
    highlight = models.ForeignKey(Highlight, db_column='ahl_highlight')
    class Meta:
        db_table = u'alaune_highlight'
