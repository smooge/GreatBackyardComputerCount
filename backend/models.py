# This file contains model class for our database

from datetime import datetime

import sqlalchemy as sa

from sqlalchemy.orm import relationship, backref, sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

import sys
sys.path.append('../')
import config


Base = declarative_base()

def create_db( db_url, db_debug=False):
   """
   A tool to set up the database
   """

   engine = sa.create_engine(db_url, echo=db_debug)
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



def get_only_one(session, model, **kwargs):
   """

   A utility to check to see if an entry exists. If it does not add
   it to the database.

   """
   ## TODO: FIX THIS AS I AM USING A MAGIC VALUE HERE.
   try:
      instance = session.query(model).filter_by(**kwargs).one()
   except NoResultFound:
      instance =session.query(model).filter_by(config.DEFAULT_SQL).one()
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
    |        | Short Name    |
    +--------+---------------+
    |        | Long Name     |
    +--------+---------------+
    |        | Description   |
    +--------+---------------+
    """
    __tablename__ = 'LU_Architecture'

    my_id = sa.Column(sa.Integer,primary_key=True, nullable=False)
    short_name = sa.Column(sa.String(20), unique=True, nullable=False)
    long_name = sa.Column(sa.String(80), nullable=False)
    description = sa.Column(sa.String(1024), nullable=True)


    def __init__(self, short_name, long_name, description):
        self.short_name = short_name
        self.long_name = long_name
        self.description = description

    def __repr__(self):
        return "<Architecture(short_name='%s', long_name='%s',description='%s')>" % (self.short_name, self.long_name, self.description)


## Lookup Table for OS
class LU_OS(Base):
    """
    +------------------------+
    |  LURelease Table       |
    +========+===============+
    | **PK** | **ReleaseID** |
    +========+===============+
    |        | Short Name    |
    +--------+---------------+
    |        | Long Name     |
    +--------+---------------+
    |        | Description   |
    +--------+---------------+
    """
    __tablename__ = 'LU_OS'
    my_id = sa.Column(sa.Integer,primary_key=True, nullable=False)
    short_name = sa.Column(sa.String(20), unique=True, nullable=False)
    long_name = sa.Column(sa.String(80),  nullable=False)
    description = sa.Column(sa.String(1024), nullable=True)

    def __init__(self, short_name, long_name, description):
        self.short_name = short_name
        self.long_name = long_name
        self.description = description

    def __repr__(self):
        return "<Operating System(short_name='%s', long_name='%s',description='%s')>" % (self.short_name, self.long_name, self.description)


class LU_Release(Base):
    """
    +------------------------+
    |  LURelease Table       |
    +========+===============+
    | **PK** | **ReleaseID** |
    +========+===============+
    +--------+---------------+
    |        | Short Name    |
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
    my_id = sa.Column(sa.Integer,primary_key=True, nullable=False)
    short_name = sa.Column(sa.String(20), unique=True, nullable=False)
    long_name = sa.Column(sa.String(80),  nullable=False)
    description = sa.Column(sa.String(1024), nullable=True)
    release_date = sa.Column(sa.DateTime, nullable=True)
    eol_date = sa.Column(sa.DateTime, nullable=True)

    def __init__(self, short_name, long_name, description, release_date, eol_date):
       if type(release_date) is datetime:
          rel = release_date
       else:
          try:
             rel=datetime.strptime(release_date,"%Y-%m-%d")
          except:
             rel=datetime(1970,1,2)

       if type(eol_date) is datetime:
          eol = eol_date
       else:
          try:
             eol=datetime.strptime(eol_date,"%Y-%m-%d")
          except:
             eol=datetime(1970,1,2)

       self.short_name = short_name
       self.long_name = long_name
       self.description = description
       self.release_date = rel
       self.eol_date = eol

    def __repr__(self):
       return "<Release(short='%s', long='%s', description='%s', release='%s', eol='%s')>" % (self.short_name, self.long_name, self.description, self.release_date.isoformat(),self.eol_date.isoformat())

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
    my_id = sa.Column(sa.Integer,primary_key=True, nullable=False)
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
    my_id = sa.Column(sa.Integer,primary_key=True, nullable=False)
    short_name = sa.Column(sa.String(4), unique=True, nullable=False)
    long_name = sa.Column(sa.String(80), unique=True, nullable=True)

    def __init__(self, short_name, long_name):
       self.short_name = short_name
       self.long_name = long_name

    def __repr__(self):
       return "<Country(short_name='%s', long_name='%s',)>" % (self.short_name, self.long_name)

class LU_Address(Base):
    """
    +------------------------+
    |  LUIP Address Table    |
    +========+===============+
    | **PK** | **IP_Key**    |
    +========+===============+
    """
    __tablename__ = 'LU_Address'
    my_id = sa.Column(sa.Integer,primary_key=True, nullable=False)
    ip_address = sa.Column(sa.String(40), unique=True, nullable=False)

    def __init__(self, ip_address):
       self.ip_address = ip_address

    def __repr(self):
       return "<IP(address='%s')>" % (self.ip_address)

class LU_UUID(Base):
    """
    A table to insert UUID's most entries will not have ones so we should allow one Null
    +------------------------+
    |    LU_UUID Table       |
    +========+===============+
    | **PK** | **UUID_Key**  |
    +========+===============+
    """
    __tablename__ = 'LU_UUID'
    my_id = sa.Column(sa.Integer,primary_key=True, nullable=False)
    uuid = sa.Column(sa.String(36), unique=True, nullable=True)
    
    def __init__(self, uuid):
       self.uuid =  uuid

    def __repr(self):
       return "<UUID('%s')>" % (self.uuid)
    

class DailyCount(Base):
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
    |        | Count         |
    +--------+---------------+
    """

    __tablename__ = 'Daily_Count'

    my_id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    date = sa.Column(sa.DateTime)
    fk_arch = sa.Column(sa.Integer,sa.ForeignKey('LU_Architecture.my_id'), nullable=False)
    fk_os = sa.Column(sa.Integer,sa.ForeignKey('LU_OS.my_id'), nullable=False)
    fk_release = sa.Column(sa.Integer,sa.ForeignKey('LU_Release.my_id'), nullable=False)
    fk_variant = sa.Column(sa.Integer,sa.ForeignKey('LU_Variant.my_id'), nullable=False)
    fk_country = sa.Column(sa.Integer,sa.ForeignKey('LU_Country.my_id'), nullable=False)

    fk_address = sa.Column(sa.Integer,sa.ForeignKey('LU_Address.my_id'), nullable=False)
    fk_uuid = sa.Column(sa.Integer,sa.ForeignKey('LU_UUID.my_id'))
    count = sa.Column(sa.Integer)

    arch    = relationship('LU_Architecture')
    os      = relationship('LU_OS')
    release = relationship('LU_Release')
    variant = relationship('LU_Variant')
    country = relationship('LU_Country')
    address = relationship('LU_Address')
    uuid    = relationship('LU_UUID')



##
## End of file

