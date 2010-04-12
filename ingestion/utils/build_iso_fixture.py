from __future__ import with_statement
import utils_localsettings
from mp3.ingestion.ingestion_localsettings import FIXTURES_PATH

"""
from optparse import OptionParser

# Command line options                                                                                                                                       
parser = OptionParser()
parser.add_option("-f", "--file", action="store", type="string", dest="filename")
parser.add_option("-l", "--lc", action="store", dest="int", dest="lc_pk")
opts, args = parser.parse_args()
"""




from django.core.serializers import json
#from django.core.exceptions import ObjectDoesNotExist
from mp3.main.models import CountryIsoEn


serializer = json.Serializer()
iso_queryset =  CountryIsoEn.objects.all()

"""
for item in iso_queryset:
    try:
        final_list.append(eval("lc.%s" % (item,)))
    except ObjectDoesNotExist:
        pass
        
to_serialize = []
for item in final_list:
    if isinstance(item, list):
        to_serialize.extend(item)
    else:
        to_serialize.append(item)
"""     
fixture_filepath = FIXTURES_PATH + '/iso.json'
with open(fixture_filepath,'w') as f:
        f.write(serializer.serialize(iso_queryset, indent=4, ensure_ascii=False).encode('utf-8'))



