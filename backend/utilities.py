# This file contains model class for our database
from datetime import datetime

import sqlalchemy as sa

from sqlalchemy.orm import relationship, backref, sessionmaker, scoped_session

import models

def add_architecture( db_session, s_name, l_name, desc ):
    """ 
    A wrapper to insert an architecture into proper table
    """
    arch = models.LU_Architecture(s_name,l_name,desc)
    db_session.add(arch)
    db_session.flush()
    return arch

def add_os( db_session, s_name, l_name, desc ):
    """ 
    A wrapper to insert an architecture into proper table 
    """
    my_os = models.LU_OS(s_name,l_name,desc)
    db_session.add(my_os)
    db_session.flush()
    return my_os

def add_release( db_session, s_name, l_name, desc, rel_date, eol_date ):
    """ 
    A wrapper to insert an architecture into proper table 
    """
    try:
        rel=datetime.strptime(rel_date,"%Y-%m-%d")
    except:
        rel=datetime(1970,1,2)

    try:
        eol=datetime.strptime(eol_date,"%Y-%m-%d")
    except:
        eol=datetime(1970,1,2)

    release = models.LU_Release( s_name, l_name, desc, rel, eol )

    db_session.add(release)
    db_session.flush()
    return release
    
def add_variant(db_session, s_name, l_name, desc ):
    """ 
    A wrapper to insert an architecture into proper table 
    """
    variant = models.LU_Variant(
        short_name = s_name,
        long_name = l_name,
        description = desc)
    db_session.add(variant)
    db_session.flush()
    return variant

def add_country(db_session, s_name, l_name):
    """ 
    A wrapper to insert an architecture into proper table 
    """
    country = models.LU_Variant(
        short_name = s_name,
        long_name = l_name)
    db_session.add(country)
    db_session.flush()
    return country



##
## EOF
