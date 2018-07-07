# This file contains model class for our database

from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declaritive import declaritive_base

import .model

Base = declaritive_base()

def insert_architecture( session, s_name, l_name, desc ):
    """ 
    A wrapper to insert an architecture into proper table 
    """
    arch = model.LU_Architecture(
        short_name = s_name,
        long_name = l_name,
        description = desc)
    arch.save(session)
    session.flush()
    return arch

def insert_os( session, s_name, l_name, desc ):
    """ 
    A wrapper to insert an architecture into proper table 
    """
    my_os = model.LU_OS(
        short_name = s_name,
        long_name = l_name,
        description = desc)
    my_os.save(session)
    session.flush()
    return my_os

def insert_release( session, s_name, l_name, desc, rel_date,eol ):
    """ 
    A wrapper to insert an architecture into proper table 
    """
    release = model.LU_OS(
        short_name = s_name,
        long_name = l_name,
        description = desc,
        release_date = date(rel_date),
        eol_date = date(eol_date)
    )
    release.save(session)
    session.flush()
    return release
    
def insert_variant( session, s_name, l_name, desc ):
    """ 
    A wrapper to insert an architecture into proper table 
    """
    variant = model.LU_OS(
        short_name = s_name,
        long_name = l_name,
        description = desc)
    variant.save(session)
    session.flush()
    return variant

