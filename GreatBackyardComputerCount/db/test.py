#!/usr/bin/python


import models

from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.orm import relationship, backref, sessionmaker, scoped_session

import uuid

import sys
sys.path.append('../')
import config

test_uuid='f3159e3b-7ca6-4243-83dd-376755ab4721'

ss = models.create_db(config.DB_URL,config.DB_DEBUG)


## Test adding an architecture
foo = models.get_one_or_create( ss, models.LU_Architecture, short_name='unknown', long_name='unknown', description='unknown')
print foo
bar = ss.query(models.LU_Architecture).all()
print bar
foo = models.get_one_or_create( ss, models.LU_Architecture, short_name='x86_64', long_name='AMD 64 reference', description='64 bit architecture')
print foo
bar = models.get_only_one( ss, models.LU_Architecture, short_name='x86_64', long_name='AMD 64 reference', description='64 bit architecture')
print bar




# ## Test adding an OS
# foo = models.get_or_create( ss, models.LU_OS, short_name='EL', long_name='Generic Enterprise Linux',  description='Default OS for which EL cant be determined')

# print foo

# ## Test our OS table
# foo = models.get_or_create(
#     ss,
#     models.LU_Release,
#     short_name='EL4',
#     long_name='Enterprise Linux 4',
#     description='',
#     release_date=datetime(2005,2,14),
#     eol_date=datetime(2012,2,29)
# )

# print foo

# ## Test variant
# foo = models.get_or_create(
#     ss,
#     models.LU_Variant,
#     name='None',
#     description='Default variant'
# )

# print foo

# ## Test Country

# foo = models.get_or_create(
#     ss,
#     models.LU_Country,
#     short_name='UZ',
#     long_name="Uzbekistan"
# )

# print foo


# foo = models.get_or_create(
#     ss,
#     models.LU_Address,
#     ip_address='127.0.0.1'
# )

# print foo


# foo = models.get_or_create(
#     ss,
#     models.LU_UUID,
#     uuid=test_uuid
# )

# ############################
# ## Query tests

# for instance in ss.query(models.LU_Architecture).order_by(models.LU_Architecture.my_id):
#     print instance



ss.close()
##
##

