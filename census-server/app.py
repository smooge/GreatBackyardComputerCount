# -*- mode: python; coding: utf-8; fill-column: 75; -*-

"""

This is the basic census server which gathers data from yum/dnf
clients querying from the internet. It then replies back a string of
mirrors that can be used to get the current repodata for the server.

"""

import logging
import geoip2.database
import geoip2.errors

from flask import Flask,request,abort
from uuid import UUID

import config

## These are global readers for the application
reader_country = geoip2.database.Reader(config.GEO_DB_COUNTRY_LOC)
reader_domain  = geoip2.database.Reader(config.GEO_DB_DOMAIN_LOC)
reader_isp     = geoip2.database.Reader(config.GEO_DB_ISP_LOC)


def clean_request(temp_answer):
    # We sometimes get additional data added onto the yum/dnf requests.
    spew = temp_answer.split("/")[0]
    spew = spew.split("!")[0]
    spew = spew.split("#")[0]
    spew = spew.split("%")[0]
    spew = spew.split("&")[0]
    spew = spew.split("'")[0]
    spew = spew.split("(")[0]
    spew = spew.split("*")[0]
    spew = spew.split("+")[0]
    spew = spew.split(",")[0]
    spew = spew.split("-")[0]
    spew = spew.split(".")[0]
    spew = spew.split(":")[0]
    spew = spew.split(";")[0]
    spew = spew.split("<")[0]
    spew = spew.split("=")[0]
    spew = spew.split(">")[0]
    spew = spew.split("?")[0]
    spew = spew.split("@")[0]
    spew = spew.split("[")[0]
    spew = spew.split("]")[0]
    spew = spew.split("^")[0]
    spew = spew.split('"')[0]
    spew = spew.split('\\')[0]
    spew = spew.split('|')[0]
    spew = spew.split('$')[0]
    return spew


# This routine will sanitize the asked for arch to try and clean out
# garbage from bad client.
def sanitize_arch(asked_arch):
    # if we didn't get an arch define it to unknown
    if asked_arch is None:
        return config.DEF_ARCH

    # now attempt to make the string lowercase. If we still have problems
    # just set it to unknown
    try:
        asked_arch = asked_arch.lower()
    except:
        return config.DEF_ARCH

    # ok clean the output of noise
    sanitized = clean_request(asked_arch)
    if sanitized in config.KNOWN_ARCHES.keys():
        return config.KNOWN_ARCHES[sanitized]
    else:
        return config.DEF_ARCH

## A routine which will clean up the os
def sanitize_os(asked_os):
    if asked_os is None:
        return config.DEF_OS
    try:
        asked_os = asked_os.lower()
    except:
        return config.DEF_OS

    sanitized = clean_request(asked_os)
    if sanitized in config.KNOWN_OSES.keys():
        return config.KNOWN_OSES[sanitized]
    else:
        return config.DEF_OS

## Determine release.
## TODO: work out how to tell if os and release work as CentOS-48 is bad
def sanitize_release(asked_release):
    if asked_release is None:
        return config.DEF_RELEASE
    try:
        asked_release = asked_release.lower()
    except:
        return config.DEF_RELEASE
    try:
        sanitize = int(asked_release)
    except:
        sanitize = config.DEF_RELEASE
    return sanitize

## Determine variants
def sanitize_variant(asked_variant):
    if asked_variant is None:
        return config.DEF_VARIANT
    try:
        asked_variant = asked_variant.lower()
    except:
        return config.DEF_VARIANT
    sanitized = clean_request(asked_variant)
    if sanitized in config.KNOWN_VARIANTS.keys():
        return config.KNOWN_VARIANTS[sanitized]
    else:
        return config.DEF_VARIANT

# based off of https://gist.github.com/ShawnMilo/7777304
def sanitize_uuid(asked_uuid):
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
      
# Make the client user-agent string one of the known ones
def sanitize_client(asked_client):
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

    # Get the IP address from the request
    # If for some reason it is None, define an emergency ip
    my_ip = request.environ['REMOTE_ADDR']
    if my_ip is None:
        my_ip = config.DEF_IP

    # NOTE: This is detailed as we will be following this for other
    # queries from the command line.
    
    # Check to see if the Arch is defined.
    temp = request.args.get('arch')

    # sanitize it.
    my_arch = sanitize_arch(temp)

    ## Repeat the above for the OS
    temp = request.args.get('os')
    # sanitize it.
    my_os = sanitize_os(temp)

    ## Repeat for the release
    temp = request.args.get('release')
    my_release = sanitize_release(temp)

    # Try to determine what variant we got
    temp = request.args.get('variant')
    my_variant = sanitize_variant(temp)

    # try to determine what uuid we got
    temp = request.args.get('uuid')
    my_uuid = sanitize_uuid(temp)

    # try to determine what user agent talked to us
    temp = request.headers.get('User-Agent')
    my_client = sanitize_client(temp)

    ## Figure out where in the world we think we are.
    try:
        my_country = reader_country.country(request.remote_addr)
    except:
        my_country = config.DEF_COUNTRY
    app.logger.info("IP: %s, Country: %s, OS: %s, Variant: %s, Release: %s, Arch: %s, UUID: %s, Client: %s" % (my_ip,my_country,my_os,my_variant,my_release,my_arch,my_uuid,my_client))

    return config.MIRROR_LIST

if __name__ == "__main__":
    logHandler = logging.FileHandler(filename=config.LOGFILE)
    formatter = logging.Formatter('%(asctime)s %(message)s')
    logHandler.setFormatter(formatter)
    logHandler.setLevel(logging.INFO)

    # set the app logger level
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(logHandler)
    app.run(host='0.0.0.0', port=5000, debug=False)
