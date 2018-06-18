# -*- mode: python; coding: utf-8; fill-column: 75;  -*-

"""

This module is responsible for loading the application configuration.

"""

import os
#basedir = os.path.abspath(os.path.dirname(__file__))

basedir = '/home/smooge'
##
## These are global variables for hte GEOIP and need to be changed per site. 
GEO_DB_COUNTRY_LOC = basedir + '/GeoIP2/GeoIP2-Country.mmdb'
GEO_DB_DOMAIN_LOC  = basedir + '/GeoIP2/GeoIP2-Domain.mmdb'
GEO_DB_ISP_LOC     = basedir + '/GeoIP2/GeoIP2-ISP.mmdb'

##
## Our one mirror.
MIRROR_LIST="""
http://www.smoogespace.com/downloads/census/
"""

##
## The logfile 
LOGFILE='/home/smooge/census-server/GBCC_server.log'
