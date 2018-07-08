#!/usr/bin/python

DB_URL='sqlite:////tmp/test.db'
DB_TEST=True

import models

from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.orm import relationship, backref, sessionmaker, scoped_session

ss = models.create_db(DB_URL,DB_TEST)


## Test adding an architecture
foo = models.get_or_create( 
    ss, 
    LU_Architecture, 
    short_name='x86_64', 
    long_name='AMD 64 reference', 
    description='64 bit architecture'
)

print foo

## Test adding an OS
foo = models.get_or_create(
    ss,
    LU_OS,
    short_name='EL',
    long_name='Generic Enterprise Linux',
    description='Default OS for which EL cant be determined'
)

print foo

## Test our OS table
foo = models.get_or_create(
    ss,
    LU_OS,
    short_name='EL',
    long_name='Generic Enterprise Linux',
    description='Default OS for which EL cant be determined'
)

print foo
