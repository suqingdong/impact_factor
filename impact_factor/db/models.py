import datetime

from sqlalchemy import create_engine, Column, Integer, Float, String, DATETIME, BOOLEAN
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Factor(Base):

    __tablename__ = 'factor'

    nlm_id = Column(String(15), comment='The Unique NLM ID', primary_key=True, )

    issn = Column(String(10), comment='ISSN Print', index=True)
    e_issn = Column(String(10), comment='ISSN Online', index=True)
    
    journal = Column(String(50), comment='Journal Title', index=True)
    iso_abbr = Column(String(30), comment='ISO Abbreviation', index=True)
    med_abbr = Column(String(30), comment='Medline Abbreviation', index=True)

    kw = Column(String(20), comment='The Keyword of Crawling')
    factor = Column(Float(3), comment='Impact Factor Latest', index=True)
    factor_history = Column(String(30), comment='Impact Factor History')

    indexed = Column(BOOLEAN, comment='Indexed in Medline or Not', index=True)


class FactorVersion(Base):

    __tablename__ = 'factor_version'

    version = Column(String(4), primary_key=True, comment='The Year of IF from greensci.net')
    datetime = Column(DATETIME, default=datetime.datetime.now()) 
