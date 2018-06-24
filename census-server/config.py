# -*- mode: python; coding: utf-8; fill-column: 75;  -*-

# This file is part of Great Backyard Computer Count Repository (GBCC).
#
# The Great Backyard Computer Count Repository is free software: you
# can redistribute it and/or modify it under the terms of the GNU
# General Public License as published by the Free Software Foundation,
# either version 2 of the License and with an addition from the Common
# Cure Rights Commitment.
#
# The Great Backyard Computer Count software is distributed in
# the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License
# along with the Great Backyard Computer Count.  If not, see
# <http://www.gnu.org/licenses/>. You should have also received a copy
# of the Common Cure Rights Commitment.

"""

This module is responsible for loading the application configuration.

"""

# This needs to be edited for the site. 
# TODO have setup do this.
basedir = '/home/smooge'

##
## These are global variables for hte GEOIP and need to be changed per site. 

GEO_DB_COUNTRY_LOC = basedir + '/GeoIP2/GeoIP2-Country.mmdb'

CSV_FILE = basedir + '/GBCC.csv'
CSV_FIELD = [
    "Date", 
    "IP",
    "Country",
    "UUID",
    "OS",
    "Variant",
    "Release",
    "Arch",
    "ClientApp"
]

# Log files get a lot of weird things stuck in them.. if we see these
# ignore them..
CRAP_CHARS = ['/', '$', '!', '#', '%', '&', "'", '"', "(", ")", "*", "+", ",", ":", ";", "<", ">", "=", "?", "@", "[", "^", "|"]


##
## Our one mirror.
MIRROR_LIST="""
http://www.smoogespace.com/downloads/census/
"""

##
## The logfile 
LOGFILE= basedir+ '/GBCC_server.log'

KNOWN_VARIANTS={
    'workstation':'workstation',
    'server': 'server', 
    'desktop': 'desktop',
    'silverblue': 'silverblue',
}
KNOWN_OSES={
    'fedora': 'fedora',
    'centos': 'centos',
    'rhel':'rhel',
    'scilin': 'scilin',
    'el':'el',
    'coreos':'coreos',
}

FEDORA_RELEASES= [3,40]
EL_RELEAES= [5,8]
CORE_RELEASES= [0,40]


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
    'preupgrade' : 'anaconda',
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

