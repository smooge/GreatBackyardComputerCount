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

This is code that is common to many different parts of the census
server and census-import scripts

"""

from uuid import UUID
from datetime import datetime

import config
from db import models

def clean_request(temp_answer):
    # We sometimes get additional data added onto the yum/dnf requests.
    spew = temp_answer.split("/")[0]
    for char in config.CRAP_CHARS:
        if char in spew:
            spew = spew.split(char)[0]
    sanitize = spew.lower()
    return sanitize

#
# A routine which takes the date from apache format to a datetime
# format 

def determine_apache_date(givendate):
    try:
        date = datetime.strptime(givendate, "%d/%b/%Y:%H:%M:%S %z")
    except:
        date = config.DEF_DATE

# This is similar to the repos but has a lot less garbage normally
def determine_arch(asked_arch):
    # Set up a default answer
    arch = config.DEF_ARCH
    if asked_arch is None:
        return arch
    sanitized = clean_request(asked_arch)
    if sanitized in config.KNOWN_ARCHES.keys():
        arch = config.KNOWN_ARCHES[sanitized]
    return arch

def determine_os(asked_os):
    os = config.DEF_OS
    if asked_os is None:
        return os
    sanitized = clean_request(asked_os)
    if sanitized in config.KNOWN_OS.keys():
        os = config.KNOWN_OS[sanitized]
    return os

## Determine release
def determine_release(asked_rel):
    release = config.DEF_RELEASE
    if asked_rel is None:
        return release
    sanitized = clean_request(asked_rel)
    if sanitized in config.KNOWN_RELEASES.keys():
        release = config.KNOWN_RELEASES[sanitized]
    return release

def determine_repo(asked_repo):
    if asked_repo is None:
        return (config.DEF_OS,config.DEF_RELEASE)

    # start the process of cleaning out various weirdness clients have
    spew = clean_request(asked_repo)

    # Clean off prewords with repodata
    for word in config.REPO_PREWORDS:
        if word in spew:
            spew = spew.replace(word, config.REPO_CODE)

    # Clean out subwords inside of the repo
    for word in config.REPO_SUBWORDS:
        if word in spew:
            spew = spew.replace(word, "")

    if "-" in spew:
        spew = re.sub("-+", "", spew)

    # OK clean out any other garbage and remove end of line
    sanitize = spew.strip()

    if sanitize in config.REPO_KEYS:
        return config.REPO_NAMES[sanitize]
    else:
        return (config.DEF_OS,config.DEF_RELEASE)


## Determine variants
def determine_variant(asked_variant):
    variant = config.DEF_VARIANT
    if asked_variant is None:
        return variant

    sanitized = clean_request(asked_variant)
    if sanitized in config.KNOWN_VARIANTS.keys():
        variant = config.KNOWN_VARIANTS[sanitized]
    return variant
    
# based off of https://gist.github.com/ShawnMilo/7777304
def determine_uuid(asked_uuid):
    uuid = config.DEF_UUID

    if asked_uuid is None:
        return uuid
    try:
        asked_uuid = asked_uuid.lower()
    except:
        return uuid
    try:
        sanitize = str(UUID(asked_uuid, version=4))
    except:
        return uuid
    if sanitize == asked_uuid:
        return sanitize
    else:
        return uuid

# Determine if client user agent is known
def determine_client(asked_client):
    client = config.DEF_CLIENT
    if asked_client is None:
        return client
    try:
        asked_client = asked_client.lower()
    except:
        return config.DEF_CLIENT

    for key,value in config.KNOWN_CLIENTS.iteritems():
        if key in asked_client:
            return value
    return config.DEF_CLIENT

