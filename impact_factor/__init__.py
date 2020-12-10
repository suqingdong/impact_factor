"""
    Impact Factor Toolkits
"""
import os
import sys
import json
import datetime
import textwrap
from functools import partial

from multiprocessing.dummy import Pool as ThreadPool

import click

from impact_factor import util
from impact_factor.util.factor import fetch_factor
from impact_factor.util.journal import parse_journal
from impact_factor.db.manager import Manager, Factor, FactorVersion

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DEFAULT_DB = os.path.join(BASE_DIR, 'data', 'impact_factor.db')

version_info = json.load(open(os.path.join(BASE_DIR, 'version', 'version.json')))
__version__ = version_info['version']
__author__ = version_info['author']
__author_email__ = version_info['author_email']


class ImpactFactor(object):
    def __init__(self, dbfile=DEFAULT_DB, echo=False, **kwargs):
        self.dbfile = dbfile
        self.manager = Manager(dbfile, echo=echo)

    def check_version(self):
        context = self.manager.query(FactorVersion)
        res = self.manager.count(Factor.nlm_id)
        context['total_count'] = res.scalar()
        context['indexed_count'] = res.filter(Factor.indexed == True).scalar()

        click.secho(textwrap.dedent('''
            ==========================================================
            program version:\t{__version__}
            database version:\t{version} [{datetime}]
            total journals:\t\t{total_count}
            indexed journals:\t{indexed_count}
            database filepath:\t{dbfile}
            ==========================================================
        ''').format(__version__=__version__, dbfile=self.dbfile, **context), fg='green', bold=True)

    def search(self, value, field=None, like=True):
        fields = [field] if field else ['issn', 'e_issn', 'journal', 'med_abbr', 'nlm_id']

        for key in fields:
            context = self.manager.query(Factor, key, value, like=like)
            if context:
                factor_history = json.loads(context['factor_history'])
                context['factor_history'] = {int(k): float(v) for k, v in factor_history.items() if v}
                return context

    def pubmed_filter(self, min_value=None, max_value=None, indexed=None, outfile=None, **kwargs):
        res = self.manager.session.query(Factor)
        if indexed is not None:
            res = res.filter(Factor.indexed == indexed)
        if min_value is not None:
            res = res.filter(Factor.factor >= min_value)
        if max_value is not None:
            res = res.filter(Factor.factor < max_value)

        issn_list = '|'.join(each.issn or '"{}"[Journal]'.format(each.med_abbr) for each in res)

        if len(issn_list) > 4000:
            print('total {n} journals with IF: {min_value} - {max_value} (exceed 4000 characters)'.format(n=res.count(), **locals()))
        else:
            print('{n} journals with IF: {min_value} - {max_value}'.format(n=res.count(), **locals()))
            if outfile:
                with util.safe_open(outfile, 'w') as out:
                    out.write(issn_list)
                print('save file: {}'.format(outfile))
            else:
                print(issn_list)

    def save_json(self, out,  context, data):
        if data:
            data =  dict(context, **data)
            print('>>> save nlm_id: {nlm_id}'.format(**context))
            out.write(json.dumps(data) + '\n')
        else:
            print('<<< no factor for nlm_id: {nlm_id}'.format(**context))

    def build(self, entrez_file, medline_file, threads=4, tmpfile=None):

        tmpfile = tmpfile or entrez_file.rsplit('.', 1)[0] + '.jl'

        with util.safe_open(tmpfile, 'w') as out:
            pool = ThreadPool(threads)
            for context in parse_journal(entrez_file):
                kws = (context.get('issn'), context.get('e_issn'))
                if any(kws):
                    pool.apply_async(fetch_factor,
                                     args=kws,
                                     callback=partial(self.save_json, out, context))
            pool.close()
            pool.join()

        self.manager.create_table(drop=True)

        indexed_ids = {each['nlm_id']: 1 for each in parse_journal(medline_file)}

        with util.safe_open(tmpfile) as f:
            for line in f:
                data = json.loads(line.strip())
                data['indexed'] = True if data['nlm_id'] in indexed_ids else False
                self.manager.upsert(Factor, 'nlm_id', Factor(**data))

        self.manager.upsert(FactorVersion,
                            None,
                            FactorVersion(version=2020, datetime=datetime.datetime.now()))
        self.manager.close()


if __name__ == '__main__':
    IF = ImpactFactor()
    IF.check_version()