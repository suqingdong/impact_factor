import json

import click

from impact_factor import util
from impact_factor.core import Factor


@click.command(
    name='filter',
    help=click.style('filter according to factor', italic=True, fg='cyan'),
)
@click.option('-m', '--min-value', help='the min factor', type=float)
@click.option('-M', '--max-value', help='the max factor', type=float)
@click.option('-C', '--color', help='colorful output', is_flag=True)
@click.option('-P', '--pubmed-filter', help='output pubmed filter format', is_flag=True)
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
