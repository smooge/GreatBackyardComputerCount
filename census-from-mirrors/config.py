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


#
# This needs to point to where the geoip2 data is
GEO_DB_COUNTRY_LOC = basedir + '/GeoIP2/GeoIP2-Country.mmdb'

#
# This needs to be set to which logs we are looking at
MIRRORS='fedora'
#MIRRORS='centos'

# We do not define the CSV_FILE here as it should be an argument of
# the calling analysis program.
#
CSV_FILE = basedir + '/mirrors-analized.csv'

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

KNOWN_VARIANTS={
    'workstation':'workstation',
    'server': 'server', 
    'desktop': 'desktop',
    'silverblue': 'silverblue',
}

KNOWN_OSES={
    'fedora': 'fedora',
    'fed_mod': 'fed_mod',
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

DEF_IP = '255.255.255.255'
DEF_COUNTRY = 'unknown'
DEF_UUID = 'unknown'
DEF_OS = 'unknown'
DEF_VARIANT = 'unknown'
DEF_REPO = 'unknown'
DEF_RELEASE = 0
DEF_ARCH = 'unknown'
DEF_CLIENT = 'unknown'
DEF_DATE = ['02', 'Jan', '1970'] # day after epoch

## Standard Fedora Apache Log Format
FEDORA_LOGFORMAT =  [
    r"(?P<host>([\d\.]+|[0-9a-fA-F\:]+))\s",
    r"(?P<identity>\S*)\s",
    r"(?P<user>\S*)\s",
    r"\[(?P<time>.*?)\]\s",
    r'"(?P<request>.*?)"\s',
    r"(?P<status>\d+)\s",
    r"(?P<bytes>\S*)\s",
    r'"(?P<referrer>.*?)"\s',
    r'"(?P<user_agent>.*?)"\s*',
]

# The repository that is returned by clients can be weird so we have to
# have multiple variants.
FEDORA_REPOS = {
    "epel4" : ("el",4),
    "epel5" : ("el",5),
    "epel6" : ("el",6), 
    "epel7" : ("el",7),
    "epel8" : ("el",8),
    "rawhide" : ("fedora",-1),
    "frawhide" : ("fedora",-1),
    "rawhidemodular" :  ("fed_mod",-1),
    "f03" : ("fedora",3),
    "f04" : ("fedora",4),
    "f05" : ("fedora",5),
    "f06" : ("fedora",6),
    "f07" : ("fedora",7),
    "f08" : ("fedora",8),
    "f09" : ("fedora",9),
    "f3" : ("fedora",3),
    "f4" : ("fedora",4),
    "f5" : ("fedora",5),
    "f6" : ("fedora",6),
    "f7" : ("fedora",7),
    "f8" : ("fedora",8),
    "f9" : ("fedora",9),
    "f10" : ("fedora",10),
    "f11" : ("fedora",11),
    "f12" : ("fedora",12),
    "f13" : ("fedora",13),
    "f14" : ("fedora",14),
    "f15" : ("fedora",15),
    "f16" : ("fedora",16),
    "f17" : ("fedora",17),
    "f18" : ("fedora",18),
    "f19" : ("fedora",19),
    "f20" : ("fedora",20),
    "f21" : ("fedora",21),
    "f22" : ("fedora",22),
    "f23" : ("fedora",23),
    "f24" : ("fedora",24),
    "f25" : ("fedora",25),
    "f26" : ("fedora",26),
    "f27" : ("fedora",27),
    "f28" : ("fedora",28),
    "f29" : ("fedora",29),
    "f30" : ("fedora",30),
    "f31" : ("fedora",31),
    "f32" : ("fedora",32),
    "f33" : ("fedora",33),
    'modular27' : ("fed_mod",27),
    'modular28' : ("fed_mod",28),
    'modular29' : ("fed_mod",29),
    'modular30' : ("fed_mod",30),
    'modular31' : ("fed_mod",31),
    'modular32' : ("fed_mod",32),
    'modular33' : ("fed_mod",33),
    'modularf27' : ("fed_mod",27),
    'modularf28' : ("fed_mod",28),
    'modularf29' : ("fed_mod",29),
    'modularf30' : ("fed_mod",30),
    'modularf31' : ("fed_mod",31),
    'modularf32' : ("fed_mod",32),
    'modularf33' : ("fed_mod",33),
    'modularrawhide' : ("fed_mod",-1),
    'modularfrawhide' : ("fed_mod",-1),
    'rhel4'     : ("rhel",4),
    'rhel5'     : ("rhel",5),
    'rhel6'     : ("rhel",6),
    'rhel7'     : ("rhel",7),
    'rhel8'     : ("rhel",8),
    'rhel9'     : ("rhel",9),
    'centos4'     : ("centos",4),
    'centos5'     : ("centos",5),
    'centos6'     : ("centos",6),
    'centos7'     : ("centos",7),
    'centos8'     : ("centos",8),
    'centos9'     : ("centos",9),
}

APACHE_MONTHS ={
    'Jan' : '01',
    'Feb' : '02',
    'Mar' : '03',
    'Apr' : '04',
    'May' : '05',
    'Jun' : '06',
    'Jul' : '07',
    'Aug' : '08',
    'Sep' : '09',
    'Oct' : '10',
    'Nov' : '11',
    'Dec' : '12', 
}

# Log files get a lot of weird things stuck in them.. if we see these
# ignore them..
CRAP_CHARS = ['/', '$', '!', '#', '%', '&', "'", '"', "(", ")", "*", "+", ",", ":", ";", "<", ">", "=", "?", "@", "[", "^", "|"]

FED_REPO_PREWORDS = ["core", 
                     "fedora", 
                     "extras", 
                     "legacy", 
                     "fc"]
FED_REPO_SUBWORDS = [ ".newkey", 
                      "install", 
                      "alpha", 
                      "beta", 
                      "debug", 
                      "devel", 
                      "info", 
                      "optional", 
                      "preview", 
                      "released", 
                      "source", 
                      "testing", 
                      "updates",
                      "client",
                      "cloud",
                      "server",
                      "workstation",
                      ]

FED_REPO_CODE = "f"

## We may have different rules here for centos
if MIRRORS == 'fedora':
    REPO_PREWORDS = FED_REPO_PREWORDS
    REPO_SUBWORDS = FED_REPO_SUBWORDS
    REPO_CODE = FED_REPO_CODE
    REPO_NAMES = FEDORA_REPOS 
    REPO_LOGFMT = FEDORA_LOGFORMAT
    REPO_KEYS = FEDORA_REPOS.keys()
