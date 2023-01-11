import json

import click

from impact_factor import util
from impact_factor.core import Factor


@click.command(
    name='search',
    help=click.style('search record from database', italic=True, fg='magenta'),
)
@click.argument('value')
@click.option('-f', '--field', help='specify a field to search')
@click.option('-C', '--color', help='colorful output', is_flag=True)
@click.pass_context
def main(ctx, **kwargs):

    fa = Factor(ctx.obj['dbfile'])

    res = fa.search(kwargs['value'])

    if kwargs['color']:
        res = util.highlight_json(json.dumps(res, indent=2))

    print(res)