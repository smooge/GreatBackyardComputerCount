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


import csv               # this is a temp to write out logs. 
                         # replace with alchemy
import errno
import geoip2.database   # can't know your places 
import geoip2.errors     # without geoip2
import maxminddb.const
import logging           # and to log our errors
import argparse
import os
import re
import string
import sys

from uuid import UUID

from GreatBackyardComputerCount import config
from GreatBackyardComputerCount import common
from GreatBackyardComputerCount.db import models

repo_keys = config.REPO_KEYS

pattern = re.compile("".join(config.REPO_LOGFMT))

## These are global readers for the application
## FIXME (make it non global)
## FIXME (doing country look ups slows down the processing of log files by
##        10.)

try:
    reader_country = geoip2.database.Reader(config.GEO_DB_COUNTRY_LOC,
                                            mode=maxminddb.const.MODE_MEMORY
    )
except:
    sys.exit(errno.EACCES)


##
## Start our subroutines here


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
def parse_line(our_line, use_geoip):

    ##
    ## Figure out if line is something we want to work on more
    global pattern

    my_ip      = config.DEF_IP
    my_country = config.DEF_COUNTRY
    my_uuid    = config.DEF_UUID
    my_os      = config.DEF_OS
    my_variant = config.DEF_VARIANT
    my_release = config.DEF_RELEASE
    my_arch    = config.DEF_ARCH
    my_client  = config.DEF_CLIENT
    if (('/metalink' in our_line) or ('/mirrorlist' in our_line)):
        our_blob = pattern.match(our_line)
        if our_blob:
            our_dict = our_blob.groupdict()
            if our_dict['status'] != "200":
                return None
            if ('repo=' not in our_dict['request']):
                return None
            my_ip             = our_dict['host']
            my_time           = common.determine_apache_date(our_dict['time']) 
            r,a,u,v           = parse_request(our_dict['request'])
            my_os,my_release  = common.determine_repo(r,re)
            my_arch     = common.determine_arch(a)
            my_uuid     = common.determine_uuid(u)
            my_variant  = common.determine_variant(v)
            my_client   = common.determine_client(our_dict['user_agent'])

            ## Figure out where in the world we think we are.
            if (use_geoip):
                try:
                    response   = reader_country.country(my_ip)
                    my_country = response.country.iso_code
                except:
                    my_country = config.DEF_COUNTRY
            else:
                my_country = config.DEF_COUNTRY

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
def parselog(in_file, use_CSV, out_file, use_SQL, use_geoip):

    if (use_CSV):
        try:
            writer = csv.DictWriter(out_file, delimiter=',', quoting=csv.QUOTE_ALL, quotechar='"', fieldnames=config.CSV_FIELD)
            writer.writeheader()
        except Exception, e:
            sys.stderr.write("Error writing output: %s\n" % e )
            sys.exit(-1)

    for line in in_file:
        parsed = parse_line(line,use_geoip)
        if parsed is None:
            pass
        else:
            if (use_CSV):
                writer.writerow(parsed)
            elif (use_SQL):
                my_obj = models.add_event( 
                                           date    = parsed['Date'],
                                           arch    = parsed['Arch'],
                                           os      = parsed['OS'],
                                           release = parsed['Release'],
                                           variant = parsed['Variant'],
                                           country = parsed['Country'],
                                           address = parsed['IP'],
                                           uuid    = parsed['UUID'],
                                           client  = parsed['ClientApp']
                                       )

    # Don't Leak data and close our streams.
    if (use_SQL):
        models.session.close()

    in_file.close()
    return


##
## The main procedure parses our command lines and sees what may have been given
## It will take multiple files and output them to a defined output file
def main():
    # Define our parser tuple
    parser = argparse.ArgumentParser(
        description = "A program to parse Fedora mirrorlist apache common log format files.",
        prog = "mirror-analysis.py",
        version = "1.1.0",
        epilog = "CSV and SQL are mutually exclusive."
    )
    #
    # By default Output to CSV
    #
    parser.set_defaults(
        CSV=False, 
        SQL=False, 
        geoip=False
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-C", "--CSV",
                      action="store_true",
                      help = "Use csv output file.",
                      dest = "CSV")

    group.add_argument("-S", "--SQL",
                       action="store_true",
                       help = "Sets the name of the database file for the run.",
                       dest = "SQL")

    parser.add_argument("-o", "--output",
                        help = "Sets the name of the output file for the run.",
                        dest = "output",
                        default = config.CSV_FILE,
                        type =argparse.FileType('a')

)
    parser.add_argument("-G", "--geoip",
                        action="store_true",
                        help = "Says whether to turn on geoip lookups",
                        dest = "geoip")

    parser.add_argument('files', 
                        nargs='+', 
                        type=argparse.FileType('r'))


    # determine the options
    args = parser.parse_args()

    # loop through the remaining arguments to see if we have files to add.
    for our_file in args.files:
        parselog(our_file,args.CSV,args.output,args.SQL,args.geoip)

if __name__ == '__main__':
    main()
