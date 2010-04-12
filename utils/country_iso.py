from __future__ import with_statement
import os
import utils_localsettings

from mp3.main import main_localsettings
from mp3.main.models import CountryIsoEn



country_iso_dict =  {}
with open(os.path.join(utils_localsettings.DATA_PATH, 'iso')) as f:
    for line in f:
        country_name, country_code = line.rstrip().split(';')
        country_iso_dict[country_code] = country_name


# Check which iso countries are not in the country_iso table 

"""
for country_code, country_name in country_iso_dict.items():
    try:
        CountryIsoEn.objects.get(code=country_code)
    except CountryIsoEn.DoesNotExist:
        print "%s, %s \n" % (country_code, country_name)

"""

# Check wich countries are in country_iso table but not in the iso norm

country_iso_list  =  CountryIsoEn.objects.all().values_list('code', 'name')
for country_code, country_name in country_iso_list:
    if country_code not in country_iso_dict:
        print "%s, %s \n" % (country_code, country_name)
