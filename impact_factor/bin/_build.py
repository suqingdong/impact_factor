import os

import click

from impact_factor import util, DEFAULT_EXCEL
from impact_factor.core import NlmCatalog


EPILOG = click.style('''
\n\b
examples:
    impact_factor build -i tests/IF.xlsx
\b
    # with a ncbi api_key
    impact_factor build -k YOUR_NCBI_API_KEY
\b
    # use a new dbfile [*recommend*]
    impact_factor -d test.db build -i tests/IF.xlsx
\b
    # without nlm_catalog
    impact_factor -d test.db build -i tests/IF.xlsx -n
''', fg='yellow', italic=True)


@click.command(
    name='build',
    help=click.style('build/update the database', italic=True, fg='green'),
    no_args_is_help=True,
    epilog=EPILOG,
)
@click.option('-i', '--excel', help='the excel file with IF')
@click.option('-u', '--update', help='update all records', is_flag=True)
@click.option('-f', '--force', help='force update when database already exists', is_flag=True)
@click.option('-k', '--ncbi_api_key', help='specify a NCBI_API_KEY', envvar='NCBI_API_KEY', show_envvar=True)
@click.option('-n', '--no-nlm', help='do not use nlm catalog', is_flag=True)
@click.pass_context
def main(ctx, **kwargs):

    with ctx.obj['manager'] as manager:
        if (key := kwargs['ncbi_api_key']):
            NlmCatalog._api_key = key

        if manager.query().count() > 0 and not kwargs['force']:
            dbfile = ctx.obj['dbfile']
            overwrite = click.confirm(f'db already exists, overwrite? [{dbfile}]')
            if not overwrite:
                exit()

        for context in util.parse_excel(kwargs['excel']):
            issn = context['issn']
            eissn = context['eissn']
            journal = context['journal']

            record = manager.query('journal', journal).first()

            # update when record is not in database, or force update
            if record is None or kwargs['update']:

                if not kwargs['no_nlm']:
                    res = None
                    if eissn:
                        res = NlmCatalog.search(f'{eissn}[ISSN]')
                    if not res and issn:
                        res = NlmCatalog.search(f'{issn}[ISSN]')
                    if not res:
                        res = NlmCatalog.search(journal)

                    if res:
                        context.update(res)
                    else:
                        manager.logger.warning(f'no result for: {context}')

                try:
                    float(context['factor'])
                except ValueError:
                    continue

                manager.insert(context, key='journal')

