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

#
# This code is heavily influenced (aka stolen) by
# https://github.com/release-monitoring/anitya
#

import csv
from datetime import datetime
import uuid

# Run with python initialize_db.py
#

from GreatBackyardComputerCount import config
from GreatBackyardComputerCount.db import models


def initialize_arch():
    with open('./initial_data/architectures.csv', 'r') as csvfile:
        my_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in my_reader:
            models.get_one_or_create(models.LU_Architecture,
                                     name=row[0],
                                     long_name=row[1],
                                     description=row[2])


def initialize_os():
    with open('./initial_data/operating_systems.csv', 'r') as csvfile:
        my_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in my_reader:
            models.get_one_or_create(
                models.LU_OS,
                name=row[0],
                long_name=row[1],
                description=row[2])


def initialize_os_release():
    with open('./initial_data/os_releases.csv', 'r') as csvfile:
        my_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in my_reader:
            models.get_one_or_create(
                models.LU_Release,
                name=row[0],
                long_name=row[1],
                description=row[2],
                release_date=row[3],
                eol_date=row[4],
            )


def initialize_os_variant():
    with open('./initial_data/os_variants.csv', 'r') as csvfile:
        my_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in my_reader:
            models.get_one_or_create(
                models.LU_Variant,
                name=row[0],
                description=row[1],
            )


def initialize_country():
    with open('./initial_data/countries.csv', 'r') as csvfile:
        my_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in my_reader:
            models.get_one_or_create(
                models.LU_Country,
                name=row[0],
                long_name=row[1],
            )


def initialize_clientapps():
    with open('./initial_data/clientapps.csv', 'r') as csvfile:
        my_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in my_reader:
            models.get_one_or_create(
                models.LU_ClientApp,
                name=row[0],
            )


def initialize_ipaddress():
    models.get_one_or_create(
        models.LU_IPAddress,
        ip_address=config.DEF_IP,
    )


def initialize_uuid():
    models.get_one_or_create(
        models.LU_UUID,
        uuid=config.DEF_UUID,
    )


def initialize_events(ss, engine):
    date1 = datetime.strptime("1970-01-02 01:00:00", "%Y-%m-%d %H:%M:%S")
    date2 = "1970-01-02 01:00:01"
    date3 = "1970-01-02 01:00:02"

    arch1 = models.LU_Architecture.query.filter_by(
        name=config.DEF_ARCH).first().name
    arch2 = config.DEF_ARCH
    arch3 = 'x86_64'

    os1 = models.LU_OS.query.filter_by(
        name=config.DEF_OS).first().name
    os2 = config.DEF_OS
    os3 = 'EL'

    release1 = ss.query(models.LU_Release).filter_by(
        name=config.DEF_RELEASE).first().name
    release2 = config.DEF_RELEASE
    release3 = 'EL07'

    variant1 = ss.query(models.LU_Variant).filter_by(
        name=config.DEF_VARIANT).first().name
    variant2 = config.DEF_RELEASE
    variant3 = 'workstation'

    country1 = ss.query(models.LU_Country).filter_by(
        name=config.DEF_COUNTRY).first().name
    country2 = config.DEF_RELEASE
    country3 = 'US'

    client1 = ss.query(models.LU_ClientApp).filter_by(
        name=config.DEF_CLIENT).first().name
    client2 = config.DEF_CLIENT
    client3 = 'yum'

    ip1 = ss.query(models.LU_IPAddress).filter_by(
        ip_address=config.DEF_IP).first().ip_address
    ip2 = config.DEF_IP
    ip3 = '127.0.0.1'

    uuid1 = ss.query(models.LU_UUID).filter_by(
        uuid=config.DEF_UUID).first().uuid
    uuid2 = config.DEF_UUID
    uuid3 = str(uuid.uuid4())

    models.add_event(
        date=date1,
        arch=arch1,
        os=os1,
        release=release1,
        variant=variant1,
        country=country1,
        address=ip1,
        uuid=uuid1,
        client=client1,
    )

    models.add_event(
        date=date2,
        arch=arch2,
        os=os2,
        release=release2,
        variant=variant2,
        country=country2,
        address=ip2,
        uuid=uuid2,
        client=client2,
    )

    models.add_event(
        date=date3,
        arch=arch3,
        os=os3,
        release=release3,
        variant=variant3,
        country=country3,
        address=ip3,
        uuid=uuid3,
        client=client3,
    )


if __name__ == '__main__':
    ss = models.session
    engine = models.engine

    models.init_db()
    initialize_arch()
    initialize_os()
    initialize_os_release()
    initialize_os_variant()
    initialize_country()
    initialize_clientapps()
    initialize_ipaddress()
    initialize_uuid()
    initialize_events(ss, engine)
    ss.close()
