import click

from impact_factor import version_info, DEFAULT_DB
from impact_factor.core import FactorManager
from impact_factor.bin._build import main as build_cli
from impact_factor.bin._query import main as search_cli
from impact_factor.bin._filter import main as filter_cli


EPILOG = 'contact: {author} <{author_email}>'.format(**version_info)

CONTEXT_SETTINGS = dict(help_option_names=['-?', '-h', '--help'])
@click.group(
    name=version_info['prog'],
    help=click.style(version_info['desc'], italic=True, fg='cyan', bold=True),
    context_settings=CONTEXT_SETTINGS,
    no_args_is_help=True,
    epilog=click.style(EPILOG, fg='bright_white', italic=True),
)
@click.option('-d', '--dbfile', help='the database file path', default=DEFAULT_DB, show_default=True)
@click.version_option(version=version_info['version'], prog_name=version_info['prog'])
@click.pass_context
def cli(ctx, **kwargs):
    ctx.ensure_object(dict)
    ctx.obj['dbfile'] = kwargs['dbfile']
    ctx.obj['manager'] = FactorManager(kwargs['dbfile'])


def main():
    cli.add_command(build_cli)
    cli.add_command(search_cli)
    cli.add_command(filter_cli)
    cli()


if __name__ == '__main__':
    main()
