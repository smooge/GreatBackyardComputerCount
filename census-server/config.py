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
LOGFILE= basedir+ '/GBCC_server.log'
DEBUGFILE= basedir+ '/GBCC_debug.log'

KNOWN_VARIANTS={
    'workstation':'workstation',
    'server': 'server', 
    'desktop': 'desktop',
    'silverblue': 'silverblue',
}
KNOWN_OSES={
    'fedora':'fedora',
    'centos':'centos',
    'rhel':'rhel',
    'el':'rhel',
    'coreos':'coreos',
    'scilin':'scilin'
}
# Arches taken from what systems have replied in logs
KNOWN_ARCHES = {
    'aarch64' : 'aarch64',
    'alpha' : 'alpha',
    'arm' : 'arm',
    'armhfp' : 'armhfp',
    'i386' : 'i386',
    'i486' : 'i386',
    'i586' : 'i386',
    'i686' : 'i386',
    'athlon' : 'i386',
    'x86_64' : 'x86_64',
    'amd64' : 'x86_64',
    'arm64' : 'aarch64',
    'ia64' : 'ia64',
    'mips' : 'mips',
    'mips64' : 'mips64',
    'mips64el' : 'mips64',
    'powerpc' : 'ppc',
    'ppc' : 'ppc',
    'ppc32' : 'ppc',
    'ppc64' : 'ppc64',
    'ppc64le' : 'ppc64le',
    'risc-v' : 'risc-v',
    's390' : 's390',
    's390x' : 's390x',
    'sparc' : 'sparc',
    'sparc64' : 'sparc64',
    'tilegx' : 'tilegx',
}

# These are taken from the regular logs
KNOWN_CLIENTS = {
    'anaconda' : 'anaconda',
    'apt-cacher' : 'apt',
    'curl' : 'curl',
    'dnf' : 'dnf',
    'packagekit' : 'packagekit',
    'python-requests' : 'anaconda',
    'ostree' : 'ostree',
    'atomic' : 'ostree',
    'urlgrabber' : 'yum', 
    'wget' : 'wget',
    'yum' : 'yum',
}



DEF_COUNTRY = 'unknown'
DEF_IP = '255.255.255.255'
DEF_OS = 'unknown'
DEF_ARCH = 'unknown'
DEF_VARIANT = 'unknown'
DEF_RELEASE = 0
DEF_CLIENT = 'unknown'
DEF_UUID = 'unknown'
