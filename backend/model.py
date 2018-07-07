# This file contains model class for our database



from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy import relationship

gbcc_associations = Table(
)


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

    my_id = Column(Integer,primary_key=True, nullable=False)
    short_name = Column(String(20), unique=True, nullable=False)
    long_name = Column(String(80), nullable=False)
    description = Column(String(1024), nullable=True)

    def __init__(self, init_short, init_long, init_description):
        self.short_name = init_short
        self.long_name = init_long
        self.description = init_description

    def __repr__(self):
        return "<Architecture(short_name='%s', long_name='%s',description='%s')>" % (self.short_name, self.long_name, self.description)


class LU_Release(Base):
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
    |        | Release Date  |
    +--------+---------------+
    |        | EOL Date      |
    +--------+---------------+
    """

    __tablename__ = 'LU_Release'
    my_id = Column(Integer,primary_key=True, nullable=False)
    short_name = Column(String(20), unique=True, nullable=False)
    long_name = Column(String(80),  nullable=False)
    description = Column(String(1024), nullable=True)
    release_date = Column(Date, nullable=True)
    eol_date = Column(Date, nullable=True)

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
    my_id = Column(Integer,primary_key=True, nullable=False)
    name = Column(String(20), unique=True, nullable=False)
    description = Column(String(1024), nullable=True)
    
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
    my_id = Column(Integer,primary_key=True, nullable=False)
    short_name = Column(String(4), unique=True, nullable=False)
    long_name = Column(String(80), unique=True, nullable=True)

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
    my_id = Column(Integer,primary_key=True, nullable=False)
    ip_address = Column(String(40), unique=True, nullable=False)


class LU_UUID(Base):
    """
    A table to insert UUID's most entries will not have ones so we should allow one Null
    +------------------------+
    |    LU_UUID Table       |
    +========+===============+
    | **PK** | **UUID_Key**  |
    +========+===============+
    """
    my_id = Column(Integer,primary_key=True, nullable=False)
    uuid = Column(String(36), unique=True, nullable=True)
    

class DailyCount(Base):
    """
    +------------------------+
    |    Daily Count Table   |
    +========+===============+
    | **PK** | **UniqueKey** |
    +========+===============+
    |        | Date          |
    +--------+---------------+
    |        | Arch_ID       |
    +--------+---------------+
    |        | Release_ID    |
    +--------+---------------+
    |        | Variant_ID    |
    +--------+---------------+
    |        | Country_ID    |
    +--------+---------------+
    |        | IP_Address    |
    +--------+---------------+
    |        | UUID          |
    +--------+---------------+
    |        | Count         |
    +--------+---------------+
    """

    __tablename__ = 'Daily_Count'

    my_id = Column(Integer, primary_key=True, nullable=False)
    date = Column(DateTIme)
    fk_arch = Column(Integer,ForeignKey('LU_Architecture.my_id'))
    fk_release = Column(Integer,ForeignKey('LU_Release.my_id'))
    fk_variant = Column(Integer,ForeignKey('LU_Variant.my_id'))
    fk_country = Column(Integer,ForeignKey('LU_Country.my_id'))
    fk_address = Column(Integer,ForeignKey('LU_Address.my_id'))
    fk_uuid = Column(Integer,ForeignKey('LU_UUID.my_id'))
    count = Column(Integer)



##
## End of file
