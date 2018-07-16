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


import errno
import geoip2.database   # can't know your places 
import geoip2.errors     # without geoip2
import logging           # and to log our errors
import optparse
import os
import re
import string
import sys
import csv 

from uuid import UUID

from GreatBackyardComputerCount import config
from GreatBackyardComputerCount import common
from GreatBackyardComputerCount.db import models

pattern = re.compile("".join(config.REPO_LOGFMT))
repo_keys = config.REPO_KEYS

## These are global readers for the application
try:
    reader_country = geoip2.database.Reader(config.GEO_DB_COUNTRY_LOC)
except:
    sys.exit(errno.EACCES)


##
## Start our subroutines here
#
# CSV files 



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
        my_ip      = config.DEF_IP
        my_country = config.DEF_COUNTRY
        my_uuid    = config.DEF_UUID
        my_os      = config.DEF_OS
        my_variant = config.DEF_VARIANT
        my_release = config.DEF_RELEASE
        my_arch    = config.DEF_ARCH
        my_client  = config.DEF_CLIENT
        if ('repo=' not in our_line) :
            return None
        our_blob = pattern.match(our_line)
        if our_blob:
            our_dict = our_blob.groupdict()
            if our_dict['status'] != "200":
                return None
            my_ip       = our_dict['host']
            ## Figure out where in the world we think we are.
            try:
                response   = reader_country.country(my_ip)
                my_country = response.country.iso_code
            except:
                my_country = config.DEF_COUNTRY
                        
            my_time     = common.determine_rfc3339_date(our_dict['time']) 
            r,a,u,v  = parse_request(our_dict['request'])
            my_os,my_release  = common.determine_repo(r)
            my_arch     = common.determine_arch(a)
            my_uuid     = common.determine_uuid(u)
            my_variant  = common.determine_variant(v)
            my_client   = common.determine_client(our_dict['user_agent'])
            
            my_data = {
                config.CSV_FIELD[0] : my_time,
                config.CSV_FIELD[1] : my_ip,
                config.CSV_FIELD[2] : my_country,
                config.CSV_FIELD[3] : my_uuid,
                config.CSV_FIELD[4] : my_os,
                config.CSV_FIELD[5] : my_variant,
                config.CSV_FIELD[6] : my_release,
                config.CSV_FIELD[7] : my_arch,
                config.CSV_FIELD[8] : my_client
            }

            return my_data
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
