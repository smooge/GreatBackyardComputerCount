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

This is the basic census server which gathers data from yum/dnf
clients querying from the internet. It then replies back a string of
mirrors that can be used to get the current repodata for the server.

"""

import errno, sys
import time              # get your time, get your red hot time
import geoip2.database   # can't know your places 
import geoip2.errors     # without geoip2
import logging           # and to log our errors

from datetime import datetime
from flask import Flask,request,abort

from db import models

# local config
import config
import common

## These are global readers for the application
try:
    reader_country = geoip2.database.Reader(config.GEO_DB_COUNTRY_LOC)
except:
    sys.exit(errno.EACCES)

try:
    session = models.init_db(config.DB_URL,config.DB_DEBUG,create=False)
except:
    sys.exit(errno.EACCES)


app = Flask(__name__)

@app.route("/census",  methods=('get', 'post'))
def census():
    if not request.headers:
        abort(400)

    '''
    The cenus application is going to listen for requests that look like:
    census?os=centos&version=7&arch=x86_64&uuid=20cfef29-b0d9-426a-8f48-9c5272082ba9
    It takes the ip address as that handed to it from the request environ. 
    
    '''

    ## Determine our date
    my_time = datetime.now()

    # Get the IP address from the request
    # If for some reason it is None, define an emergency ip
    my_ip = request.environ['REMOTE_ADDR']
    if my_ip is None:
        my_ip = config.DEF_IP

    # NOTE: This is detailed as we will be following this for other
    # queries from the command line.
    
    # Check to see if the Arch is defined.
    temp = request.args.get('arch')
    my_arch = common.determine_arch(temp)

    ## Repeat the above for the OS
    temp = request.args.get('os')
    my_os = common.determine_os(temp)

    ## Repeat for the release
    temp = request.args.get('release')
    my_release = common.determine_release(temp)

    # Try to determine what variant we got
    temp = request.args.get('variant')
    my_variant = common.determine_variant(temp)

    # try to determine what uuid we got
    temp = request.args.get('uuid')
    my_uuid = common.determine_uuid(temp)

    # try to determine what user agent talked to us
    temp = request.headers.get('User-Agent')
    my_client = common.determine_client(temp)

    ## Figure out where in the world we think we are.
    try:
        response = reader_country.country(request.remote_addr)
        my_country = response.country.iso_code
    except:
        my_country = config.DEF_COUNTRY

    my_obj = models.add_event( session,
                               date = my_date,
                               arch = my_arch,
                               os   = my_os,
                               release = my_release,
                               variant = my_variant,
                               country = my_country,
                               address = my_ip,
                               uuid = my_uuid,
                               client = my_client
                               )
    # if my_obj is None:
    #     app.logger

    # and end this by returning our mirror
    # TODO: make this a metalink using a template
    return config.MIRROR_LIST

