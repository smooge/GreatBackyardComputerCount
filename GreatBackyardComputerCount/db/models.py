# -*- mode: python; coding: utf-8; fill-column: 75;  -*-

# This file is a part of the Great Backyard Computer Count project.
#
# Copyright © 2018 Stephen Smoogen
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

# This file contains model class for our database

from datetime import datetime

import sqlalchemy as sa
import uuid

from sqlalchemy.orm import relationship, backref, sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.exc import SQLAlchemyError, IntegrityError 

from GreatBackyardComputerCount import config

engine = sa.create_engine(config.DB_URL, echo=config.DB_DEBUG)
# Source: https://docs.sqlalchemy.org/en/latest/dialects/sqlite.html
# see section 'sqlite-foreign-keys'
if config.DB_URL.startswith('sqlite:'):
   def _fk_pragma_on_connect(dbapi_con, con_record):
      dbapi_con.execute("PRAGMA foreign_keys=ON")
      sa.event.listen(engine, 'connect', _fk_pragma_on_connect)

session = scoped_session(sessionmaker(bind=engine))
session.configure(bind=engine, 
                        autoflush=False,
                        expire_on_commit=False)
Base = declarative_base()
Base.query = session.query_property()

def init_db():
   """
   A tool to set up the database
   """
   Base.metadata.create_all(bind=engine)


##
## Source https://stackoverflow.com/questions/2546207/does-sqlalchemy-have-an-equivalent-of-djangos-get-or-create
## http://skien.cc/blog/2014/01/15/sqlalchemy-and-race-conditions-implementing/
## Credit: Patrick Uiterwijk for mentioning it.
def get_one_or_create(model, **kwargs):
   """
   A utility to check to see if an entry exists. If it does not add
   it to the database.
   Derived from: http://skien.cc/blog/2014/01/15/sqlalchemy-and-race-conditions-implementing/

   """
   created = False

   try:
      instance = model.query.filter_by(**kwargs).one()
   except NoResultFound:
      kwargs.update({})
      try:
         instance = model(**kwargs)
         session.add(instance)
         session.commit()
         created = True
      except IntegrityError:
         session.rollback()
         try:
            instance = model.query.filter_by(**kwargs).one()
         except NoResultFound: 
            instance = None
   except MultipleResultsFound:
      instance = model.query.filter_by(**kwargs).first()
   return (instance, created)

def add_event(date, arch, os, release, variant, country, address, uuid, client):

   ## 
   ## FIXME: This is slow to do large number of events. This is mostly
   ## due to how I am doing the inserts with each object getting made first
   ## and then a ORM add at the end. I think what I need is something like
   ## the following or a complete reworking on how to do bulk inserts.
   ##
   ## INSERT INTO Events (date, fk_arch, fk_os, fk_release, fk_variant,
   ##                     fk_country, fk_address, fk_uuid, fk_client)
   ## VALUES 
   ## (date, 
   ##  (SELECT pk_id from LU_Architecture WHERE name=arch OR name=config.DEF_SQL),
   ##  (SELECT pk_id from LU_OS WHERE name=os OR name=config.DEF_SQL),
   ##  (SELECT pk_id from LU_Release WHERE name=release OR name=config.DEF_SQL),
   ##  (SELECT pk_id from LU_Variant WHERE name=variant OR name=config.DEF_SQL),
   ##  (SELECT pk_id from LU_Country WHERE name=country OR name=config.DEF_SQL),
   ##  (SELECT pk_id from LU_UUID WHERE uuid=uuid),
   ##  (SELECT pk_id from LU_IPAddress WHERE address=address),
   ##  (SELECT pk_id from LU_ClientApps WHERE name=client OR name=config.DEF_SQL));
   ##  
   ##

   instance = None
   # Determine if we got a date set up correctly or by string
   if type(date) is not datetime:
      try:
         date = datetime.strptime(date,"%Y-%m-%d  %H:%M:%S")
      except:
         try:
            date = datetime.strptime(date,"%Y-%m-%d")
         except:
            date = config.DEF_DATE

   # These are lookup tables so we do not want to add if not found
   arch    = get_only_one(LU_Architecture,name=arch)
   os      = get_only_one(LU_OS,name=os)
   release = get_only_one(LU_Release,name=release)
   variant = get_only_one(LU_Variant,name=variant)
   country = get_only_one(LU_Country,name=country)
   client  = get_only_one(LU_ClientApp,name=client)
   ## These need to insert an ip or uuid if not found
   address = get_one_or_create(LU_IPAddress,ip_address=address)[0]
   uuid = get_one_or_create(LU_UUID,uuid=uuid)[0]

   try:
      instance = Events.query.filter_by(
         date=date,
         arch=arch,
         os=os,
         release=release,
         variant=variant,
         country=country,
         address=address,
         uuid=uuid,
         client=client,
      ).one()
   except NoResultFound:
      instance = Events(date=date,arch=arch,os=os, release=release, variant=variant, country=country, address=address, uuid=uuid, client=client)
      session.add(instance)
      session.commit()

   except MultipleResultsFound:
      instance =  Events.query.filter_by(
         date=date,
         arch=arch,
         os=os,
         release=release,
         variant=variant,
         country=country,
         address=address,
         uuid=uuid,
         client=client,
      ).first()

   return instance
      

##
##
def get_only_one(model, **kwargs):
   """

   A utility to check to see if an entry exists. If it does not return the default.

   """
   instance = None
   try:
      instance = model.query.filter_by(**kwargs).one()
   except NoResultFound:
      instance = model.query.first()
   except MultipleResultsFound:
      instance = model.query.filter_by(**kwargs).first()
   return instance

## Lookup Table for Architectures
class LU_Architecture(Base):
    """
    +------------------------+
    |  LUArchitectureTable   |
    +========+===============+
    | **PK** | **ArchID**    |
    +========+===============+
    |        | (Short) Name  |
    +--------+---------------+
    |        | Long Name     |
    +--------+---------------+
    |        | Description   |
    +--------+---------------+
    """
    __tablename__ = 'LU_Architecture'

    pk_id       = sa.Column(sa.Integer,primary_key=True, nullable=False)
    name        = sa.Column(sa.String(20), unique=True, nullable=False)
    long_name   = sa.Column(sa.String(80), nullable=False)
    description = sa.Column(sa.String(1024), nullable=True)


    def __repr__(self):
        return "<Architecture(name='%s', long_name='%s',description='%s')>" % (self.name, self.long_name, self.description)


## Lookup Table for OS
class LU_OS(Base):
    """
    +------------------------+
    |  LURelease Table       |
    +========+===============+
    | **PK** | **ReleaseID** |
    +========+===============+
    |        | (Short) Name  |
    +--------+---------------+
    |        | Long Name     |
    +--------+---------------+
    |        | Description   |
    +--------+---------------+
    """
    __tablename__ = 'LU_OS'
    pk_id       = sa.Column(sa.Integer,primary_key=True, nullable=False)
    name        = sa.Column(sa.String(20), unique=True, nullable=False)
    long_name   = sa.Column(sa.String(80),  nullable=False)
    description = sa.Column(sa.String(1024), nullable=True)

    def __repr__(self):
        return "<Operating System(name='%s', long_name='%s',description='%s')>" % (self.name, self.long_name, self.description)


class LU_Release(Base):
    """
    +------------------------+
    |  LURelease Table       |
    +========+===============+
    | **PK** | **ReleaseID** |
    +========+===============+
    +--------+---------------+
    |        | (Short) Name  |
    +--------+---------------+
    |        | Long Name     |
    +--------+---------------+
    |        | Description   |
    +--------+---------------+
    |        | Release Date  |
    +--------+---------------+
    |        | EOL Date      |
    +--------+---------------+
    """

    __tablename__ = 'LU_Release'
    pk_id        = sa.Column(sa.Integer,primary_key=True, nullable=False)
    name         = sa.Column(sa.String(20), unique=True, nullable=False)
    long_name    = sa.Column(sa.String(80),  nullable=False)
    description  = sa.Column(sa.String(1024), nullable=True)
    release_date = sa.Column(sa.DateTime, nullable=True)
    eol_date     = sa.Column(sa.DateTime, nullable=True)

    def __init__(self, name, long_name, description, release_date, eol_date):
       if type(release_date) is datetime:
          rel = release_date
       else:
          try:
             rel=datetime.strptime(release_date,"%Y-%m-%d")
          except:
             rel=config.DEF_DATE

       if type(eol_date) is datetime:
          eol = eol_date
       else:
          try:
             eol=datetime.strptime(eol_date,"%Y-%m-%d")
          except:
             eol=config.DEF_DATE

       self.name = name
       self.long_name = long_name
       self.description = description
       self.release_date = rel
       self.eol_date = eol

    def __repr__(self):
       return "<Release(name='%s', long='%s', description='%s', release='%s', eol='%s')>" % (self.name, self.long_name, self.description, self.release_date.isoformat(),self.eol_date.isoformat())

class LU_Variant(Base):
    """
    +------------------------+
    |  LUVariant Table       |
    +========+===============+
    | **PK** | **VariantKY** |
    +========+===============+
    |        | Name          |
    +--------+---------------+
    |        | Description   |
    +--------+---------------+
    """
    __tablename__ = 'LU_Variant'
    pk_id = sa.Column(sa.Integer,primary_key=True, nullable=False)
    name = sa.Column(sa.String(20), unique=True, nullable=False)
    description = sa.Column(sa.String(1024), nullable=True)
    
    def __repr__(self):
        return "<Release(name='%s', description='%s')>" % (self.name, self.description)

class LU_Country(Base):
    """
    +------------------------+
    |  LUCountry Table       |
    +========+===============+
    | **PK** | **CountryKY** |
    +========+===============+
    |        | Short Name    |
    +--------+---------------+
    |        | Long Name     |
    +--------+---------------+
    """
    __tablename__ = 'LU_Country'
    pk_id = sa.Column(sa.Integer,primary_key=True, nullable=False)
    name = sa.Column(sa.String(4), unique=True, nullable=False)
    long_name = sa.Column(sa.String(80), unique=True, nullable=True)

    def __repr__(self):
       return "<Country(name='%s', long_name='%s',)>" % (self.name, self.long_name)

class LU_ClientApp(Base):
    """
    A table to insert ClientApps's most entries will not have ones so we should allow one Null
    +------------------------+
    |    LU_ClientApp Table  |
    +========+===============+
    | **PK** | **Clnt_Key**  |
    +========+===============+
    |        | Name          |
    +--------+---------------+
    """
    __tablename__ = 'LU_ClientApp'
    pk_id = sa.Column(sa.Integer,primary_key=True, nullable=False)
    name = sa.Column(sa.String(36), unique=True, nullable=True)
    
    def __repr(self):
       return "<UUID('%s')>" % (self.uuid)

class LU_IPAddress(Base):
    """
    +------------------------+
    |  LUIP Address Table    |
    +========+===============+
    | **PK** | **IP_Key**    |
    +========+===============+
    |        | IP_Address    |
    +--------+---------------+
    """
    __tablename__ = 'LU_IPAddress'
    pk_id = sa.Column(sa.Integer,primary_key=True, nullable=False)
    ip_address = sa.Column(sa.String(40), unique=True, nullable=False)

    def __repr__(self):
       return "<IP(address='%s')>" % (self.ip_address)

class LU_UUID(Base):
    """
    A table to insert UUID's most entries will not have ones so we should allow one Null
    +------------------------+
    |    LU_UUID Table       |
    +========+===============+
    | **PK** | **UUID_Key**  |
    +========+===============+
    |        | UUID          |
    +--------+---------------+
    """
    __tablename__ = 'LU_UUID'
    pk_id = sa.Column(sa.Integer,primary_key=True, nullable=False)
    uuid = sa.Column(sa.String(36), unique=True, nullable=True)
    
    def __init__(self, uuid):
       if type(uuid) is uuid:
          self.uuid = str(uuid)
       elif type(uuid) is str:
          self.uuid =  uuid
       else:
          self.uuid =  config.DEF_UUID

    def __repr__(self):
       return "<UUID('%s')>" % (self.uuid)
    

class Events(Base):
    """
    +------------------------+
    |    Daily Count Table   |
    +========+===============+
    | **PK** | **UniqueKey** |
    +========+===============+
    |        | Date          |
    +--------+---------------+
    | **FK** | Arch_ID       |
    +--------+---------------+
    | **FK** | OS_ID         |
    +--------+---------------+
    | **FK** | Release_ID    |
    +--------+---------------+
    | **FK** | Variant_ID    |
    +--------+---------------+
    | **FK** | Country_ID    |
    +--------+---------------+
    | **FK** | IP_Address    |
    +--------+---------------+
    | **FK** | UUID          |
    +--------+---------------+
    | **FK** | ClientApp     |
    +--------+---------------+
    """

    __tablename__ = 'Events'

    pk_id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    date = sa.Column(sa.DateTime)
    fk_arch = sa.Column(sa.Integer,sa.ForeignKey('LU_Architecture.pk_id'), nullable=False)
    fk_os = sa.Column(sa.Integer,sa.ForeignKey('LU_OS.pk_id'), nullable=False)
    fk_release = sa.Column(sa.Integer,sa.ForeignKey('LU_Release.pk_id'), nullable=False)
    fk_variant = sa.Column(sa.Integer,sa.ForeignKey('LU_Variant.pk_id'), nullable=False)
    fk_country = sa.Column(sa.Integer,sa.ForeignKey('LU_Country.pk_id'), nullable=False)
    fk_address = sa.Column(sa.Integer,sa.ForeignKey('LU_IPAddress.pk_id'), nullable=False)
    fk_uuid = sa.Column(sa.Integer,sa.ForeignKey('LU_UUID.pk_id'))
    fk_client = sa.Column(sa.Integer,sa.ForeignKey('LU_ClientApp.pk_id'))

    arch    = relationship('LU_Architecture', backref='Events')
    os      = relationship('LU_OS', backref='Events')
    release = relationship('LU_Release', backref='Events')
    variant = relationship('LU_Variant', backref='Events')
    country = relationship('LU_Country', backref='Events')
    address = relationship('LU_IPAddress', backref='Events')
    uuid    = relationship('LU_UUID', backref='Events')
    client  = relationship('LU_ClientApp', backref='Events')

    def __repr__(self):
       return "<Event(pk='%s', date='%s', arch='%s',os='%s', rel='%s', var='%s', country='%s',client='%s',ip='%s',uuid='%s')>" % (
          self.pk_id, 
          self.date, 
          self.arch,
          self.os,
          self.release,
          self.variant,
          self.country,
          self.client,
          self.address,
          self.uuid
       )

##
## End of file

