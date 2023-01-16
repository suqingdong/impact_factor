import json

import click

from impact_factor import util
from impact_factor.core import Factor


EPILOG = click.style('''
\n\b
examples:
    impact_factor filter -m 50
    impact_factor filter -m 50 -M 100
    impact_factor filter -m 50 -M 100 -C
    impact_factor filter -m 50 -M 100 -P
''', fg='yellow', italic=True)

@click.command(
    name='filter',
    help=click.style('filter according to factor', italic=True, fg='cyan'),
    no_args_is_help=True,
    epilog=EPILOG,
)
@click.option('-m', '--min-value', help='the min factor', type=float)
@click.option('-M', '--max-value', help='the max factor', type=float)
@click.option('-C', '--color', help='colorful output', is_flag=True)
@click.option('-P', '--pubmed-filter', help='output pubmed filter format', is_flag=True)
@click.option('-L', '--limit', help='the limit of results', type=int, default=100, show_default=True)
@click.pass_context
def main(ctx, **kwargs):

    fa = Factor(ctx.obj['dbfile'])

    res = fa.filter(**kwargs)

    if kwargs['pubmed_filter']:
        print(res)
    else:
        if kwargs['color']:
            res = util.highlight_json(json.dumps(res, indent=2))
        print(res)
