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

import flask
from datetime import datetime

import geoip2.database   # can't know your places
import maxminddb.const
import logging           # and to log our errors

from db import models

# local config
from . import config
from . import common

census_page = flask.Blueprint('census', __name__)
data_page = flask.Blueprint('data', __name__)
arches_page = flask.Blueprint('arches', __name__)
apps_page = flask.Blueprint('apps', __name__)
countries_page = flask.Blueprint('countries', __name__)
os_page = flask.Blueprint('oses', __name__)
releases_page = flask.Blueprint('releases', __name__)
variants_page = flask.Blueprint('variants', __name__)
ips_page = flask.Blueprint('ips', __name__)
uuids_page = flask.Blueprint('uuids', __name__)
events_page = flask.Blueprint('events', __name__)


@census_page.route("/census", methods=('get', 'post'))
def census():
    reader_country = geoip2.database.Reader(config.GEO_DB_COUNTRY_LOC,
                                            mode=maxminddb.const.MODE_MEMORY)

    if not flask.request.headers:
        flask.abort(400)

    '''
    The cenus application is going to listen for requests that look like:
    census?os=centos&version=7&arch=x86_64&uuid=20cfef29-b0d9-426a-8f48-9c5272082ba9
    It takes the ip address as that handed to it from the request environ.

    '''

    # Determine our date
    my_date = datetime.now()

    # Get the IP address from the request
    # If for some reason it is None, define an emergency ip
    my_ip = flask.request.environ['REMOTE_ADDR']
    if my_ip is None:
        my_ip = config.DEF_IP

    # NOTE: This is detailed as we will be following this for other
    # queries from the command line.

    # Check to see if the Arch is defined.
    temp = flask.request.args.get('arch')
    my_arch = common.determine_arch(temp)

    # Repeat the above for the OS
    temp = flask.request.args.get('os')
    my_os = common.determine_os(temp)

    # Repeat for the release
    temp = flask.request.args.get('release')
    my_release = common.determine_release(temp)

    # Try to determine what variant we got
    temp = flask.request.args.get('variant')
    my_variant = common.determine_variant(temp)

    # try to determine what uuid we got
    temp = flask.request.args.get('uuid')
    my_uuid = common.determine_uuid(temp)

    # try to determine what user agent talked to us
    temp = flask.request.headers.get('User-Agent')
    my_client = common.determine_client(temp)

    # Figure out where in the world we think we are.
    try:
        response = reader_country.country(flask.request.remote_addr)
        my_country = response.country.iso_code
    except:
        my_country = config.DEF_COUNTRY

    flask.current_app.logger.info(
        "D:%s A:%s O:%s R:%s V:%s C:%s I:%s U:%s X:%s",
        my_date,
        my_arch,
        my_os,
        my_release,
        my_variant,
        my_country,
        my_ip,
        my_uuid,
        my_client
    )

    models.add_event(
        date=my_date,
        arch=my_arch,
        os=my_os,
        release=my_release,
        variant=my_variant,
        country=my_country,
        address=my_ip,
        uuid=my_uuid,
        client=my_client
    )

    return config.MIRROR_LIST


@data_page.route("/data/", methods=('get', 'post'))
def data():
    return flask.render_template('default.html',
                                 count=config.NUMQ)


@arches_page.route("/data/arches", methods=('get', 'post'))
def arches():
    lookups = models.LU_Architecture.query.all()
    # FIXME: The following is a travesty against python
    temp_table = [{}]
    for i in lookups:
        temp_table.append({
            'name': i.name,
            'long_name': i.long_name,
            'description': i.description,
            'count': models.Events.query.filter(
                models.Events.fk_arch == models.LU_Architecture.query.filter(
                    models.LU_Architecture.name == i.name).first().pk_id).count()})

    return flask.render_template('arches.html',
                                 arches=temp_table)


@apps_page.route("/data/clientapps", methods=('get', 'post'))
def apps():
    lookups = models.LU_ClientApp.query.all()
    temp_table = [{}]
    for i in lookups:
        temp_table.append({
            'name': i.name,
            'count': models.Events.query.filter(
                models.Events.fk_client == models.LU_ClientApp.query.filter(models.LU_ClientApp.name == i.name).first().pk_id).count()})
    return flask.render_template('clientapps.html',
                                 clientapps=temp_table)


@countries_page.route("/data/countries", methods=('get', 'post'))
def countries():
    lookups = models.LU_Country.query.all()
    temp_table = [{}]
    for i in lookups:
        temp_table.append({
            'name': i.name,
            'long_name': i.long_name,
            'count': models.Events.query.filter(
                models.Events.fk_country == models.LU_Country.query.filter(models.LU_Country.name == i.name).first().pk_id).count()})
    return flask.render_template('countries.html',
                                 countries=temp_table)


@os_page.route("/data/os", methods=('get', 'post'))
def os():
    lookups = models.LU_OS.query.all()
    temp_table = [{}]
    for i in lookups:
        temp_table.append({
            'name': i.name,
            'long_name': i.long_name,
            'description': i.description,
            'count': models.Events.query.filter(
                models.Events.fk_os == models.LU_OS.query.filter(models.LU_OS.name == i.name).first().pk_id).count()})
    return flask.render_template('os.html',
                                 oses=temp_table)


@releases_page.route("/data/os_releases", methods=('get', 'post'))
def releases():
    lookups = models.LU_Release.query.all()
    temp_table = [{}]
    for i in lookups:
        temp_table.append({
            'name': i.name,
            'long_name': i.long_name,
            'description': i.description,
            'release_date': i.release_date,
            'eol_date': i.eol_date,
            'count': models.Events.query.filter(
                models.Events.fk_release == models.LU_Release.query.filter(models.LU_Release.name == i.name).first().pk_id).count()})
    return flask.render_template('os_releases.html',
                                 releases=temp_table)


@variants_page.route("/data/os_variants", methods=('get', 'post'))
def variants():
    lookups = models.LU_Variant.query.all()
    temp_table = [{}]
    for i in lookups:
        temp_table.append({
            'name': i.name,
            'description': i.description,
            'count': models.Events.query.filter(
                models.Events.fk_variant == models.LU_Variant.query.filter(models.LU_Variant.name == i.name).first().pk_id).count()})
    return flask.render_template('os_variants.html',
                                 variants=temp_table)


@ips_page.route("/data/addresses", methods=('get', 'post'))
def ips():
    lookups = models.LU_IPAddress.query.order_by(models.LU_IPAddress.pk_id.desc()).limit(config.NUMQ)
    temp_table = [{}]
    for i in lookups:
        temp_table.append({
            'ip_address': i.ip_address,
            'count': models.Events.query.filter(models.Events.fk_address == models.LU_IPAddress.query.filter(models.LU_IPAddress.ip_address == i.ip_address).first().pk_id).count()})
    return flask.render_template('addresses.html',
                                 count=config.NUMQ,
                                 addresses=temp_table)


@uuids_page.route("/data/uuids", methods=('get', ' post'))
def uuids():
    lookups = models.LU_UUID.query.order_by(models.LU_UUID.pk_id.desc()).limit(config.NUMQ)
    temp_table = [{}]
    for i in lookups:
        temp_table.append({
            'uuid': i.uuid,
            'count': models.Events.query.filter(models.Events.fk_uuid == models.LU_UUID.query.filter(models.LU_UUID.uuid == i.uuid).first().pk_id).count()})
    return flask.render_template('uuids.html',
                                 count=config.NUMQ,
                                 uuids=temp_table)


@events_page.route("/data/events", methods=('get', 'post'))
def events():
    lookups = models.Events.query.order_by(models.Events.date.desc()).limit(config.NUMQ)
    return flask.render_template('events.html',
                                 count=config.NUMQ,
                                 events=lookups)
