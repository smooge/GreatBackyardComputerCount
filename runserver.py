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
Program to run the FLASK app for human debugging.
"""

import logging

from GreatBackyardComputerCount import config
from GreatBackyardComputerCount.app import engine


logHandler = logging.FileHandler(filename=config.LOGFILE)
formatter = logging.Formatter('%(asctime)s %(message)s')
logHandler.setFormatter(formatter)
logHandler.setLevel(logging.INFO)

app = engine()
# set the app logger level
app.logger.setLevel(logging.INFO)
app.logger.addHandler(logHandler)
app.run(host='0.0.0.0', port=5000, debug=False)

