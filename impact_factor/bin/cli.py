#!/usr/bin/env python
# -*- coding=utf-8 -*-
import json
import datetime

import click

from impact_factor import util
from impact_factor import ImpactFactor, DEFAULT_DB, version_info, __doc__


@click.group(help=click.style(__doc__, fg='cyan', bold=True))
@click.option('-d', '--dbfile', help='the path of database file', default=DEFAULT_DB, show_default=True)
@click.version_option(version=version_info['version'], prog_name=version_info['prog'])
@click.pass_context
def main(ctx, **kwargs):
    ctx.obj = {
        'IF': ImpactFactor(**kwargs)
    }


@main.command(help='search with a keyword, journal, issn, etc.')
@click.argument('keyword')
@click.option('-f', '--field', help='the field to search, automaticly default')
@click.pass_obj
def search(obj, **kwargs):
    res = obj['IF'].search(kwargs['keyword'], field=kwargs['field'])
    if res:
        print(json.dumps(res, indent=2))
    else:
        print('no result for keyword: {keyword}'.format(**kwargs))


@main.command(help='show the version of program')
@click.pass_obj
def version(obj, **kwargs):
    obj['IF'].check_version()

    
@main.command(help='generate filter for NCBI Pubmed')
@click.option('-min', '--min-value', help='the minimum value of IF', type=float)
@click.option('-max', '--max-value', help='the maximum value of IF', type=float)
@click.option('-o', '--outfile', help='the output filename [stdout]')
@click.pass_obj
def pubmed_filter(obj, **kwargs):
    obj['IF'].pubmed_filter(indexed=True, **kwargs)


@main.command(help='build or update database')
@click.option('-ef', '--entrez-file', help='the NCBI J_Entrez file')
@click.option('-mf', '--medline-file', help='the NCBI J_Medline file')
@click.option('-t', '--threads', help='the threads used for crawling factor', type=int, default=16, show_default=True)
@click.option('-v', '--dbversion', help='the build version of database', default=datetime.datetime.now().year, show_default=True)
@click.pass_obj
def build(obj, **kwargs):
    if not (kwargs['entrez_file'] and kwargs['medline_file']):
        print('please supply J_Entrez and J_Medline file!')
    else:
        obj['IF'].build(kwargs['entrez_file'], kwargs['medline_file'], threads=kwargs['threads'])


if __name__ == '__main__':
    main()
