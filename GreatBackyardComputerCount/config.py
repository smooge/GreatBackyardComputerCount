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

from datetime import datetime

# This needs to be edited for the site.
# TODO have setup do this.
basedir = '/home/smooge'

DB_URL = 'sqlite:///' + basedir + '/GBCC.db'
DB_DEBUG = False


#
# These are global variables for hte GEOIP and need to be changed per site.

GEO_DB_COUNTRY_LOC = basedir + '/GeoIP2/GeoIP2-Country.mmdb'

# Number of queries we default to
NUMQ = 100

#
# Our one mirror.
MIRROR_LIST = """
http://www.smoogespace.com/downloads/census/
"""

# Default file for CSV writing
CSV_FILE = basedir + '/GBCC.csv'

#
# The logfile
LOGFILE = basedir + '/GBCC_server.log'

#
# This needs to be set to which logs we are looking at
MIRRORS = 'fedora'
# MIRRORS = 'centos'


#
# FIXME: The following are all more constants for programs to use. They
# should probably be moved to a different file
#

# Log files get a lot of weird things stuck in them.. if we see these
# ignore them..
CRAP_CHARS = ['/', '$', '!', '#', '%', '&', "'", '"',
              "(", ")", "*", "+", ",", ":", ";", "<",
              ">", "=", "?", "@", "[", "^", "|"]


#
# FIXME: This is all in the sql database. Should we just pull the data out
# of a SQL DB at startup even if we are running in CVS mode?
#

KNOWN_VARIANTS = {
    'unknown': 'unknown',
    'atomichost': 'atomichost',
    'atomicworkstation': 'atomicworkstation',
    'cinnamon': 'cinnamon',
    'cloud': 'cloud',
    'container': 'container',
    'desktop': 'desktop',
    'gnome': 'gnome',
    'kde': 'kde',
    'lxde': 'lxde',
    'lxqt': 'lxqt',
    'mate': 'mate',
    'minimal': 'minimal',
    'modular': 'modular',
    'netinstall': 'netinstall',
    'server': 'server',
    'silverblue': 'silverblue',
    'soas': 'soas',
    'workstation': 'workstation',
    'xfce': 'xfce',
}

KNOWN_OS = {
    'unknown': 'unknown',
    'fedora': 'fedora',
    'centos': 'centos',
    'rhel': 'rhel',
    'scilin': 'scilin',
    'el': 'el',
    'redsleeve': 'redsleeve',
    'fedatomic': 'fedatomic',
    'fedcore': 'fedcore',
}

KNOWN_RELEASES = {
    "unknown": "unknown",
    "f1": "f01",
    "f2": "f02",
    "f3": "f03",
    "f4": "f04",
    "f5": "f05",
    "f6": "f06",
    "f7": "f07",
    "f8": "f08",
    "f9": "f09",
    "f10": "f10",
    "f11": "f11",
    "f12": "f12",
    "f13": "f13",
    "f14": "f14",
    "f15": "f15",
    "f16": "f16",
    "f17": "f17",
    "f18": "f18",
    "f19": "f19",
    "f20": "f20",
    "f21": "f21",
    "f22": "f22",
    "f23": "f23",
    "f24": "f24",
    "f25": "f25",
    "f26": "f26",
    "f27": "f27",
    "f28": "f28",
    "f29": "f29",
    "f30": "f30",
    "f31": "f31",
    "rawhide": "frawhide",
    "el2": "el02",
    "el3": "el03",
    "el4": "el04",
    "el5": "el05",
    "el6": "el06",
    "el7": "el07",
    "el8": "el08",
}


# Arches taken from what systems have replied in logs
KNOWN_ARCHES = {
    'aarch64': 'aarch64',
    'alpha': 'alpha',
    'arm': 'arm',
    'armhfp': 'armhfp',
    'i386': 'i386',
    'i486': 'i386',
    'i586': 'i386',
    'i686': 'i386',
    'athlon': 'i386',
    'x86_64': 'x86_64',
    'amd64': 'x86_64',
    'arm64': 'aarch64',
    'ia64': 'ia64',
    'mips': 'mips',
    'mips64': 'mips64',
    'mips64el': 'mips64',
    'powerpc': 'ppc',
    'ppc': 'ppc',
    'ppc32': 'ppc',
    'ppc64': 'ppc64',
    'ppc64le': 'ppc64le',
    'risc-v': 'risc-v',
    's390': 's390',
    's390x': 's390x',
    'sparc': 'sparc',
    'sparc64': 'sparc64',
    'tilegx': 'tilegx',
}

# These are taken from the regular logs
KNOWN_CLIENTS = {
    'anaconda': 'anaconda',
    'apt-cacher': 'apt',
    'curl': 'curl',
    'dnf': 'dnf',
    'packagekit': 'packagekit',
    'preupgrade': 'anaconda',
    'ostree': 'ostree',
    'atomic': 'ostree',
    'urlgrabber': 'yum',
    'wget': 'wget',
    'yum': 'yum',
}

DEF_SQL = 'unknown'
DEF_DATE = datetime(1970, 1, 2, 1, 0, 0)
DEF_ARCH = DEF_SQL
DEF_OS = DEF_SQL
DEF_RELEASE = DEF_SQL
DEF_VARIANT = DEF_SQL
DEF_COUNTRY = DEF_SQL
DEF_IP = '255.255.255.255'
DEF_UUID = 'ffffffff-ffff-4fff-bfff-ffffffffffff'
DEF_CLIENT = DEF_SQL
DEF_REPO = DEF_SQL

# We do not define the CSV_FILE here as it should be an argument of
# the calling analysis program.
#

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

KNOWN_VARIANTS = {
    'workstation': 'workstation',
    'server': 'server',
    'desktop': 'desktop',
    'silverblue': 'silverblue',
}

KNOWN_OSES = {
    'fedora': 'fedora',
    'fed_mod': 'fed_mod',
    'centos': 'centos',
    'rhel': 'rhel',
    'scilin': 'scilin',
    'el': 'el',
    'coreos': 'coreos',
}

# Arches taken from what systems have replied in logs
KNOWN_ARCHES = {
    'aarch64': 'aarch64',
    'alpha': 'alpha',
    'arm': 'arm',
    'armhfp': 'armhfp',
    'i386': 'i386',
    'i486': 'i386',
    'i586': 'i386',
    'i686': 'i386',
    'athlon': 'i386',
    'x86_64': 'x86_64',
    'amd64': 'x86_64',
    'arm64': 'aarch64',
    'ia64': 'ia64',
    'mips': 'mips',
    'mips64': 'mips64',
    'mips64el': 'mips64',
    'powerpc': 'ppc',
    'ppc': 'ppc',
    'ppc32': 'ppc',
    'ppc64': 'ppc64',
    'ppc64le': 'ppc64le',
    'risc-v': 'risc-v',
    's390': 's390',
    's390x': 's390x',
    'sparc': 'sparc',
    'sparc64': 'sparc64',
    'tilegx': 'tilegx',
}

# These are taken from the regular logs
KNOWN_CLIENTS = {
    'anaconda': 'anaconda',
    'apt-cacher': 'apt',
    'curl': 'curl',
    'dnf': 'dnf',
    'packagekit': 'packagekit',
    'preupgrade': 'anaconda',
    'python-requests': 'anaconda',
    'ostree': 'ostree',
    'atomic': 'ostree',
    'urlgrabber': 'yum',
    'wget': 'wget',
    'yum': 'yum',
}


# Standard Fedora Apache Log Format
FEDORA_LOGFORMAT = [
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
    "epel4": ("el", "el04"),
    "epel5": ("el", "el05"),
    "epel6": ("el", "el06"),
    "epel7": ("el", "el07"),
    "epel8": ("el", "el08"),
    "rawhide": ("fedora", "frawhide"),
    "frawhide": ("fedora", "frawhide"),
    "rawhidemodular": ("fed_mod", "frawhide"),
    "f03": ("fedora", "f03"),
    "f04": ("fedora", "f04"),
    "f05": ("fedora", "f05"),
    "f06": ("fedora", "f06"),
    "f07": ("fedora", "f07"),
    "f08": ("fedora", "f08"),
    "f09": ("fedora", "f09"),
    "f3": ("fedora", "f03"),
    "f4": ("fedora", "f04"),
    "f5": ("fedora", "f05"),
    "f6": ("fedora", "f06"),
    "f7": ("fedora", "f07"),
    "f8": ("fedora", "f08"),
    "f9": ("fedora", "f09"),
    "f10": ("fedora", "f10"),
    "f11": ("fedora", "f11"),
    "f12": ("fedora", "f12"),
    "f13": ("fedora", "f13"),
    "f14": ("fedora", "f14"),
    "f15": ("fedora", "f15"),
    "f16": ("fedora", "f16"),
    "f17": ("fedora", "f17"),
    "f18": ("fedora", "f18"),
    "f19": ("fedora", "f19"),
    "f20": ("fedora", "f20"),
    "f21": ("fedora", "f21"),
    "f22": ("fedora", "f22"),
    "f23": ("fedora", "f23"),
    "f24": ("fedora", "f24"),
    "f25": ("fedora", "f25"),
    "f26": ("fedora", "f26"),
    "f27": ("fedora", "f27"),
    "f28": ("fedora", "f28"),
    "f29": ("fedora", "f29"),
    "f30": ("fedora", "f30"),
    'modular27': ("fed_mod", "f27"),
    'modular28': ("fed_mod", "f28"),
    'modular29': ("fed_mod", "f29"),
    'modular30': ("fed_mod", "f30"),
    'modular31': ("fed_mod", "f31"),
    'modular32': ("fed_mod", "f32"),
    'modular33': ("fed_mod", "f33"),
    'modularf27': ("fed_mod", "f27"),
    'modularf28': ("fed_mod", "f28"),
    'modularf29': ("fed_mod", "f29"),
    'modularf30': ("fed_mod", "f30"),
    'modularrawhide': ("fed_mod", "frawhide"),
    'modularfrawhide': ("fed_mod", "frawhide"),
    'rhel4': ("rhel", "el04"),
    'rhel5': ("rhel", "el05"),
    'rhel6': ("rhel", "el06"),
    'rhel7': ("rhel", "el07"),
    'rhel8': ("rhel", "el08"),
    'centos4': ("centos", "el04"),
    'centos5': ("centos", "el05"),
    'centos6': ("centos", "el06"),
    'centos7': ("centos", "el07"),
    'centos8': ("centos", "el08"),
}

APACHE_MONTHS = {
    'Jan': '01',
    'Feb': '02',
    'Mar': '03',
    'Apr': '04',
    'May': '05',
    'Jun': '06',
    'Jul': '07',
    'Aug': '08',
    'Sep': '09',
    'Oct': '10',
    'Nov': '11',
    'Dec': '12',
}

FED_REPO_PREWORDS = ["core",
                     "fedora",
                     "extras",
                     "legacy",
                     "fc"]

FED_REPO_SUBWORDS = [".newkey",
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
                     "workstation", ]

FED_REPO_CODE = "f"

# We may have different rules here for centos
if MIRRORS == 'fedora':
    REPO_PREWORDS = FED_REPO_PREWORDS
    REPO_SUBWORDS = FED_REPO_SUBWORDS
    REPO_CODE = FED_REPO_CODE
    REPO_NAMES = FEDORA_REPOS
    REPO_LOGFMT = FEDORA_LOGFORMAT
    REPO_KEYS = FEDORA_REPOS.keys()
