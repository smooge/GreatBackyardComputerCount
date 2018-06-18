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

import config

## These are global readers for the application
reader_country = geoip2.database.Reader(GEO_DB_COUNTRY_LOC)
reader_domain  = geoip2.database.Reader(GEO_DB_DOMAIN_LOC)
reader_isp     = geoip2.database.Reader(GEO_DB_ISP_LOC)

app = Flask(__name__)

@app.route("/census",  methods=('get', 'post'))
def census():
    if not request.headers:
        abort(400)

    my_ip = request.environ['REMOTE_ADDR']
    my_os = request.args.get('os')
    my_os_variant = request.args.get('variant')
    my_os_version = request.args.get('version')
    my_os_arch = request.args.get('arch')
    my_uuid = request.args.get('uuid')
    try:
        my_country = reader_country.country(request.remote_addr)
    except:
        my_country = "UNKNOWN"
    app.logger.info("IP: %s, Country: %s, OS: %s, Variant: %s, Version: %s, Arch: %s, UUID: %s" % (my_ip,my_country,my_os,my_os_variant,my_os_version,my_os_arch,my_uuid))

    return MIRROR_LIST

if __name__ == "__main__":
    logHandler = logging.FileHandler(filename='GBCC.log')
    formatter = logging.Formatter('%(asctime)s %(message)s')
    logHandler.setFormatter(formatter)
    logHandler.setLevel(logging.INFO)

    # set the app logger level
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(logHandler)
    app.run(host='0.0.0.0', port=5000, debug=True)
