# -*- coding: utf-8 -*-

from mp3.main.helpers import Helper


class HighlightVignette(Helper):
    
    
    def __init__(self, request, highlight):
        super(HighlightVignette, self).__init__(request)
        self.id = highlight.pk
        self.title = highlight.title
        self.subtitle = highlight.subtitle
        self.text = highlight.text
        self.link = highlight.link
        self.img = highlight.img_fullpath()
        
    
