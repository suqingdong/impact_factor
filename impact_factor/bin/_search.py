import json

import click

from impact_factor import util
from impact_factor.core import Factor


EPILOG = click.style('''
\n\b
examples:
    impact_factor search nature         # search journal
    impact_factor search 'nature c%'    # like search journal
    impact_factor search 0028-0836      # search ISSN
    impact_factor search 1476-4687      # search eISSN
    impact_factor search 0410462        # search nlm_id
    impact_factor search nature --color # colorful output
''', fg='yellow', italic=True)

@click.command(
    name='search',
    help=click.style('search record from database', italic=True, fg='magenta'),
    no_args_is_help=True,
    epilog=EPILOG,
)
@click.argument('value')
@click.option('-f', '--field', help='specify a field to search')
@click.option('-C', '--color', help='colorful output', is_flag=True)
@click.pass_context
def main(ctx, **kwargs):

    fa = Factor(ctx.obj['dbfile'])

    res = fa.search(kwargs['value'], key=kwargs['field'])

    if kwargs['color']:
        res = util.highlight_json(json.dumps(res, indent=2))

    print(res)