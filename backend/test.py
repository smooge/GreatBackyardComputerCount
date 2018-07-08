#!/usr/bin/python

DB_URL='sqlite:////tmp/test.db'
DB_TEST=True

import models
import utilities


from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.orm import relationship, backref, sessionmaker, scoped_session

ss = models.create_db(DB_URL,DB_TEST)


## Test the add_architecture
utilities.add_architecture(
    ss, 
    'x86_64', 
    'AMD 64 reference', 
    '64 bit architecture'
)

## Test the add_os
utilities.add_os(
    ss,
    'EL',
    'Generic Enterprise Linux',
    'Default OS for which EL cant be determined'
)


utilities.add_release(
    ss,
    'EL4',
    'Enterprise Linux 4',
    'kernel 2.6.9',
    '2005-02-15',
    '2012-02-29'
)
    

utilities.add_variant(
    ss,
    'None',
    'Not a thing',
    'Nothing to see here'
)


## Test the 
