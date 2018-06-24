#!/usr/bin/python
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


import csv               # this is a temp to write out logs. replace with alchemy
import errno
import geoip2.database   # can't know your places 
import geoip2.errors     # without geoip2
import logging           # and to log our errors
import optparse
import os
import re
import string
import sys
import time              # get your time, get your red hot time

from uuid import UUID


import config

pattern = re.compile("".join(config.REPO_LOGFMT))
repo_keys = config.REPO_KEYS


## These are global readers for the application
try:
    reader_country = geoip2.database.Reader(config.GEO_DB_COUNTRY_LOC)
except:
    sys.exit(errno.EACCES)


##
## Start our subroutines here

def clean_request(temp_answer):
    # We sometimes get additional data added onto the yum/dnf requests.
    spew = temp_answer.split("/")[0]
    for char in config.CRAP_CHARS:
        if char in spew:
            spew = spew.split(char)[0]
    sanitize = spew.lower()
    return sanitize

#
# A routine which takes the date from apache format to standard RFC3339
# Please see https://tools.ietf.org/html/rfc3339
def determine_rfc3339_date(a_date):
    date_subpart = a_date.split()
    
    # We may have been given garbage.. logs are the devil's playground
    try:
        [day, month, year] = date_subpart.split(":")[0].split('/')
    except:
        # string out of index because date corrupted?
        [day, month, year ] = ['01', '01', '1970'] # epoch
    ret_str = "%s-%s-%s" % (year, config.APACHE_MONTHS[month], day)
    return ret_str

def determine_repo(asked_repo):
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

    # And even other stuff we see
    for word in config.REPO_SPEW:
        if word in spew:
            tempstr = spew + ".*"
            spew = re.sub(tempstr, "", spew)

    # OK clean out any other garbage and remove end of line
    sanitize = spew.strip()

    if sanitize in config.REPO_KEYS:
        return config.REPO_NAMES[sanitize]
    else:
        return (config.DEF_OS,config.DEF_RELEASE)

# This is similar to the repos but has a lot less garbage normally
def determine_arch(asked_arch):

    sanitize = clean_request(asked_arch)

    if sanitize in config.KNOWN_ARCHES:
        return config.KNOWN_ARCHES[sanitize]
    else:
        return config.DEF_ARCH

## Determine variants
def determine_variant(asked_variant):
    if asked_variant is None:
        return config.DEF_VARIANT

    sanitized = clean_request(asked_variant)
    if sanitized in config.KNOWN_VARIANTS.keys():
        return config.KNOWN_VARIANTS[sanitized]
    else:
        return config.DEF_VARIANT

# based off of https://gist.github.com/ShawnMilo/7777304
def determine_uuid(asked_uuid):
    if asked_uuid is None:
        return config.DEF_UUID
    try:
        asked_uuid = asked_uuid.lower()
    except:
        return config.DEF_UUID
    try:
        sanitize = str(UUID(asked_uuid, version=4))
    except:
        return config.DEF_UUID
    if sanitize == asked_uuid:
        return sanitize
    else:
        return config.DEF_UUID

# Determine if client user agent is known
def determine_client(asked_client):
    if asked_client is None:
        return config.DEF_CLIENT
    try:
        asked_client = asked_client.lower()
    except:
        return config.DEF_CLIENT

    for key,value in config.KNOWN_CLIENTS.iteritems():
        if key in asked_client:
            return value
    return config.DEF_CLIENT


#
# A subroutine to try to determine our get data (field 7 of normal apache log)
#
def parse_request(request):
    repo=config.DEF_REPO
    arch=config.DEF_ARCH
    uuid=config.DEF_UUID
    variant=config.DEF_VARIANT
    parts = request.split()[1].split("?")[1].split("&")
    for i in parts:
        if 'repo=' in i:
            repo = i.split('=')[1]
        if 'arch=' in i:
            arch = i.split('=')[1]
        if 'uuid=' in i:
            uuid = i.split('=')[1]
        if 'variant=' in i:
            variant = i.split('=')[1]
    return (repo,arch,uuid,variant)

#
# Parse the log line
#
def parse_line(our_line):

    ##
    ## Figure out if line is something we want to work on more
    global pattern

    if (('/metalink' in our_line) or ('/mirrorlist' in our_line)):
        our_blob = pattern.match(our_line)
        if our_blob:
            our_dict = our_blob.groupdict()
            if our_dict['status'] != 200:
                return None
            ip       = our_dict['host']
            ## Figure out where in the world we think we are.
            try:
                country = reader_country.country(ip)
            except:
                country = config.DEF_COUNTRY
            my_time     = determine_rfc3339_date(our_dict['time']) 
            r,a,u,v  = parse_request(our_dict['request'])
                
            my_os,my_release  = determine_repo(r)
            my_arch     = determine_arch(a)
            my_uuid     = determine_uuid(u)
            my_variant  = determine_variant(v)
            my_client   = determine_client(our_dict['user_agent'])

            my_data = {
                config.CSV_FIELD[0] : my_time,
                config.CSV_FIELD[1] : my_ip,
                config.CSV_FIELD[1] : my_country,
                config.CSV_FIELD[2] : my_uuid,
                config.CSV_FIELD[3] : my_os,
                config.CSV_FIELD[4] : my_variant,
                config.CSV_FIELD[5] : my_release,
                config.CSV_FIELD[6] : my_arch,
                config.CSV_FIELD[7] : my_client
            }
        else:
            return None
    else:
        return None


##
## The main worker subroutine
## Input: a file which should contain formated data from 
def parselog(our_file, out_file):
    our_file = our_file
    output_file = out_file
    try:
        in_data = open(our_file, "r")
    except:
        sys.stderr.write("Unable to open %s\n" % our_file )
        sys.exit(-1)

    try:
        out_data = open(out_file, 'a')
        writer = csv.DictWriter(out_data, fieldnames=config.CSV_FIELD)
        writer.writeheader()
    except:
        sys.stderr.write("Unable to open %s\n" % out_file )
        sys.exit(-1)

    for line in in_data:
        parsed = parse_line(line)
        if parsed is None:
            pass
        else:
            writer.writerow(parsed)

    in_data.close()
    out_data.close()

    return


##
## The main procedure parses our command lines and sees what may have been given
## It will take multiple files and output them to a defined output file
def main():
    # Define our parser tuple
    parser = optparse.OptionParser(
        description = "A program to parse Fedora mirrorlist apache common log format files.",
        prog = "mirror-analysis.py",
        version = "1.0.0",
        usage = "%prog [-o output-filename] logfile1 [logfile2...]"
    )
    #
    parser.add_option("-o", "--output",
                      default = config.CSV_FILE,
                      help = "Sets the name of the output file for the run.",
                      dest = "output")

    # determine the options
    (options, args) = parser.parse_args()
    if options.output:
        out_file = options.output
    else:
        out_file = config.CSV_FILE

    # loop through the remaining arguments to see if we have files to add.
    for our_file in args:
        parselog(our_file,out_file)

if __name__ == '__main__':
    main()
