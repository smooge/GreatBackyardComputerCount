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

import flask

# local config
from . import blueprints


def engine():
    app = flask.Flask(__name__)

    app.logger.addHandler

    app.register_blueprint(blueprints.census_page)
    app.register_blueprint(blueprints.data_page)
    app.register_blueprint(blueprints.arches_page)
    app.register_blueprint(blueprints.apps_page)
    app.register_blueprint(blueprints.countries_page)
    app.register_blueprint(blueprints.os_page)
    app.register_blueprint(blueprints.releases_page)
    app.register_blueprint(blueprints.variants_page)
    app.register_blueprint(blueprints.ips_page)
    app.register_blueprint(blueprints.uuids_page)
    app.register_blueprint(blueprints.events_page)

    return app
