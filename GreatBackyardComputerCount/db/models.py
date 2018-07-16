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

# sys.path.append('../')
# import config


Base = declarative_base()

def init_db( db_url, db_debug=False, create=False):
   """
   A tool to set up the database
   """

   engine = sa.create_engine(db_url, echo=db_debug)
   if create:
      Base.metadata.create_all(bind=engine)

   # Source: https://docs.sqlalchemy.org/en/latest/dialects/sqlite.html
   # see section 'sqlite-foreign-keys'
   if db_url.startswith('sqlite:'):
      def _fk_pragma_on_connect(dbapi_con, con_record):
         dbapi_con.execute("PRAGMA foreign_keys=ON")
         sa.event.listen(my_engine, 'connect', _fk_pragma_on_connect)

   db_session = scoped_session(sessionmaker(bind=engine))
   db_session.commit()

   return db_session

##
## Source https://stackoverflow.com/questions/2546207/does-sqlalchemy-have-an-equivalent-of-djangos-get-or-create
## http://skien.cc/blog/2014/01/15/sqlalchemy-and-race-conditions-implementing/
## Credit: Patrick Uiterwijk for mentioning it.
def get_one_or_create(session, model, **kwargs):
   """
   A utility to check to see if an entry exists. If it does not add
   it to the database.
   Derived from: http://skien.cc/blog/2014/01/15/sqlalchemy-and-race-conditions-implementing/

   """
   created = False

   try:
      instance = session.query(model).filter_by(**kwargs).one()
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
            instance = session.query(model).filter_by(**kwargs).one()
         except NoResultFound: 
            instance = None
   except MultipleResultsFound:
      instance =session.query(model).filter_by(**kwargs).first()
   return (instance, created)

def add_event(session, date, arch, os, release, variant, country, address, uuid, client):
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

   # Determine if we got an arch object and if not make one
   if type(arch) is not LU_Architecture:
      arch = get_only_one(session,LU_Architecture,name=arch)
             
   if type(os) is not LU_OS:
      os = get_only_one(session,LU_OS,name=os)
                         
   if type(release) is not LU_Release:
      release = get_only_one(session,LU_Release,name=release)

   if type(variant) is not LU_Variant:
      variant = get_only_one(session,LU_Variant,name=variant)
      
   if type(country) is not LU_Country:
      country = get_only_one(session,LU_Country,name=country)

   if type(address) is not LU_IPAddress:
      address = get_one_or_create(session,LU_IPAddress,ip_address=address)[0]

   if type(uuid) is not LU_UUID:
      uuid = get_one_or_create(session,LU_UUID,uuid=uuid)[0]

   if type(client) is not LU_ClientApp:
      client = get_only_one(session,LU_ClientApp,name=client)

   try:
      instance = session.query(Events).filter_by(
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
      try:
         instance = Events(date=date,arch=arch,os=os, release=release, variant=variant, country=country, address=address, uuid=uuid, client=client)
      except Exception, e:
         print "AAAA",e, date,arch,os,release,variant,country,address,uuid,client
      session.add(instance)
      session.commit()
   except MultipleResultsFound:
      instance =  session.query(Events).filter_by(
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
   except Exception, e:
      print "FFFF", e, date,arch,os,release,variant,country,address,uuid,client

   return instance
      

##
##
def get_only_one(session, model, **kwargs):
   """

   A utility to check to see if an entry exists. If it does not return the default.

   """
   instance = None
   try:
      instance = session.query(model).filter_by(**kwargs).one()
   except NoResultFound:
      instance = session.query(model).first()
   except MultipleResultsFound:
      instance =session.query(model).filter_by(**kwargs).first()
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


    def __init__(self, name, long_name, description):
        self.name = name
        self.long_name = long_name
        self.description = description

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

    def __init__(self, name, long_name, description):
        self.name = name
        self.long_name = long_name
        self.description = description

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
    
    def __init__(self, name, description):
        self.name = name
        self.description = description

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

    def __init__(self, name, long_name):
       self.name = name
       self.long_name = long_name

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
    
    def __init__(self, name):
       self.name =  name

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

    def __init__(self, ip_address):
       self.ip_address = ip_address

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

    arch    = relationship('LU_Architecture',foreign_keys=[fk_arch])
    os      = relationship('LU_OS', foreign_keys=[fk_os])
    release = relationship('LU_Release', foreign_keys=[fk_release])
    variant = relationship('LU_Variant', foreign_keys=[fk_variant])
    country = relationship('LU_Country', foreign_keys=[fk_country])
    address = relationship('LU_IPAddress', foreign_keys=[fk_address])
    uuid    = relationship('LU_UUID', foreign_keys=[fk_uuid])
    client  = relationship('LU_ClientApp', foreign_keys=[fk_client])

    ## FIXME: This is definitely overly complicated and shouldn't need this much to do basic foreign key relations
    def __init__(self, date, arch, os, release, variant, country, address, uuid, client):
       if type(date) is datetime:
          self.date = date
       else:
          try:
             self.date = datetime.strptime(date,"%Y-%m-%d %H:%M:%S")
          except:
             self.date = config.DEF

       if type(arch) is LU_Architecture:
          self.fk_arch = arch.pk_id
       elif type(arch) is int:
          self.fk_arch = arch
       else:
          self.fk_arch = config.DEF_PK

       if type(os) is LU_OS:
          self.fk_os = os.pk_id
       elif type(os) is int:
          self.fk_os = os
       else:
          self.fk_os = config.DEF_PK

       if type(release) is LU_Release:
          self.fk_release = release.pk_id
       elif type(release) is int:
          self.fk_release = release
       else:
          self.fk_release = config.DEF_PK

       if type(variant) is LU_Variant:
          self.fk_variant = variant.pk_id
       elif type(variant) is int:
          self.fk_variant = variant
       else:
          self.fk_variant = config.DEF_PK

       if type(country) is LU_Country:
          self.fk_country = country.pk_id
       elif type(country) is int:
          self.fk_country = country
       else:
          self.fk_country = config.DEF_PK

       if type(address) is LU_IPAddress:
          self.fk_address = address.pk_id
       elif type(address) is int:
          self.fk_address = address
       else:
          self.fk_address = config.DEF_PK

       if type(uuid) is LU_UUID:
          self.fk_uuid = uuid.pk_id
       elif type(uuid) is int:
          self.fk_uuid = uuid
       else:
          self.fk_uuid = config.DEF_PK

       if type(client) is LU_ClientApp:
          self.fk_client = client.pk_id
       elif type(client) is int:
          self.fk_client = client
       else:
          self.fk_client = config.DEF_PK

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

