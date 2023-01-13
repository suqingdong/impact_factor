from pathlib import Path

import click

from impact_factor import util, DEFAULT_EXCEL
from impact_factor.core import NlmCatalog


@click.command(
    name='build',
    help=click.style('build/update the database', italic=True, fg='green'),
)
@click.option('-i', '--excel', help='the excel file with IF', default=DEFAULT_EXCEL, show_default=True)
@click.option('-u', '--update', help='update all records', is_flag=True)
@click.option('-f', '--force', help='force update when database already exists', is_flag=True)
@click.pass_context
def main(ctx, **kwargs):

    with ctx.obj['manager'] as manager:

        if Path(ctx.obj['dbfile']).exists() and not kwargs['force']:
            overwrite = click.confirm('db already exists, overwrite?')
            if not overwrite:
                exit()

        for context in util.parse_excel(kwargs['excel']):
            issn = context['issn']
            eissn = context['eissn']
            journal = context['journal']

            record = manager.query('journal', journal).first()

            # update when record is not in database, or force update
            if record is None or kwargs['update']:

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

                manager.insert(context, key='journal')

