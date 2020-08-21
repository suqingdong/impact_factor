# -*- coding=utf-8 -*-
import datetime
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.state import InstanceState

from impact_factor.db.models import Base, Factor, FactorVersion


class Manager(object):
    """
        uri:
            - sqlite:///relative/path/to/db
            - sqlite:////absolute/path/to/db
    """
    def __init__(self, dbfile, echo=True):
        self.uri = 'sqlite:///{}'.format(dbfile)
        self.engine = sqlalchemy.create_engine(self.uri, echo=echo)
        self.session = self.connect()

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.close()
        print('database closed.')

    def close(self):
        self.session.commit()
        self.session.close()

    def connect(self):
        self.engine.logger.info('connecting to: {}'.format(self.uri))
        DBSession = sessionmaker(bind=self.engine)
        return DBSession()

    def create_table(self, drop=False):
        if drop:
            Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine, checkfirst=True)

    def count(self, key):
        return self.session.query(sqlalchemy.func.count(key))

    def query(self, Meta, key=None, value=None, as_dict=True, like=False):
        res = self.session.query(Meta)
        if key and value:
            if key in ('issn', 'e_issn', 'nlm_id'):
                like = False
            if like:
                res = res.filter(Meta.__dict__[key].like(value))
            else:
                res = res.filter(Meta.__dict__[key]==value)
    
        if res.first():
            context = res.first()
            if as_dict:
                context = {k: v for k, v in context.__dict__.items() if not isinstance(v, InstanceState)}
            return context
        return None

    def upsert(self, Meta, on, datas):
        if isinstance(datas, Base):
            datas = [datas]

        for data in datas:
            context = {k: v for k, v in data.__dict__.items() if not isinstance(v, InstanceState)}

            res = self.session.query(Meta)
            if on:
                res = res.filter(Meta.__dict__[on]==data.__dict__[on])
                
            if not res.first():
                self.engine.logger.info('\x1b[33minsert: {}\x1b[0m'.format(context))
                self.session.add(data)
            else:
                self.engine.logger.info('\x1b[32mupdate: {}\x1b[0m'.format(context))
                res.update(context)


if __name__ == '__main__':

    uri = 'sqlite:///test.db'

    with Manager(uri) as m:
        m.create_table(drop=True)
        m.upsert(FactorVersion, None, FactorVersion(version=2020, datetime=datetime.datetime.now()))
        m.upsert(Factor, 'issn', Factor(issn='0160-6999', iso_abbr='AADE Ed J', factor=0.05))
