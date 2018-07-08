# This file contains model class for our database

from datetime import datetime

import sqlalchemy as sa

from sqlalchemy.orm import relationship, backref, sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

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


    def __init__(self, s_name, l_name, desc):
        self.short_name = s_name
        self.long_name = l_name
        self.description = desc

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

    def __init__(self, s_name, l_name, desc):
        self.short_name = s_name
        self.long_name = l_name
        self.description = desc

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
    release_date = sa.Column(sa.Date, nullable=True)
    eol_date = sa.Column(sa.Date, nullable=True)

    def __init__(self, init_short, init_long, init_description, init_rel, init_eol):
        self.short_name = init_short
        self.long_name = init_long
        self.description = init_description
        self.release_date = init_rel
        self.eol_date = init_eol

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
    
    def __init__(self, init_name, init_description):
        self.name = init_short
        self.description = init_description

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

    def __init__(self, init_short, init_long):
        self.short_name = init_short
        self.long_name = init_long

    def __repr__(self):
        return "<Release(short_name='%s', long_name='%s',)>" % (self.short_name, self.long_name)

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

