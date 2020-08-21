#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""\x1b[1;32m\
=======================================================
 _ __ __ ___  __   ________ ___ __   ________ __  ___  
| |  V  | _,\/  \ / _/_   _| __/  \ / _/_   _/__\| _ \ 
| | \_/ | v_/ /\ | \__ | | | _| /\ | \__ | || \/ | v / 
|_|_| |_|_| |_||_|\__/ |_| |_||_||_|\__/ |_| \__/|_|_\ 

                              \x1b[3m-- Impact Factor Toolkits      
=======================================================\
\x1b[0m"""
import os
import sys
import json
import time
import datetime
import argparse

import colorama

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
PKG_DIR = os.path.dirname(ROOT_DIR)
sys.path.insert(0, PKG_DIR)

from impact_factor import util
from impact_factor import ImpactFactor, DEFAULT_DB, __version__, __epilog__


# init colorama
colorama.init()


def get_args():
    parser = argparse.ArgumentParser(
        description=__doc__,
        prog='impact_factor',
        epilog=__epilog__,
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-db', '--dbfile', help='the database file path [%(default)s]', default=DEFAULT_DB)
    parser.add_argument('-d', '--debug', help='logging in debug mode', action='store_true')
    parser.add_argument('-e', '--echo', help='turn on echo for sqlalchemy', action='store_true')

    parser.add_argument('-v', '--version',
                        help='show program\'s version number and exit', version=__version__, action='version')

    subparser = parser.add_subparsers(title='sub-commands', dest='cmd', metavar='')

    build = subparser.add_parser('build', help='build or update database')
    build.add_argument('-ef', '--entrez-file', help='the NCBI J_Entrez file')
    build.add_argument('-mf', '--medline-file', help='the NCBI J_Medline file')
    build.add_argument('-t', '--threads',
                       help='the threads used for crawling factor [%(default)s]',
                       type=int, default=16)
    build.add_argument('-v', '--dbversion',
                       help='the version of database [%(default)s]',
                       default=datetime.datetime.now().year)
    build.set_defaults(func=main)

    search = subparser.add_parser('search', help='the keyword to search, issn, journal, etc.')
    search.add_argument('keyword', help='the query key word')
    search.add_argument('-k', '--field', help='the field to search, automaticly default')
    search.set_defaults(func=main)

    version = subparser.add_parser('version', help='show the version')
    version.set_defaults(func=main)

    pubmed_filter = subparser.add_parser('pubmed_filter', help='generate filter for NCBI Pubmed')
    pubmed_filter.add_argument('-min', '--min-value', help='the minimum value of IF', type=float)
    pubmed_filter.add_argument('-max', '--max-value', help='the maximum value of IF', type=float)
    pubmed_filter.add_argument('-o', '--outfile', help='the output filename [stdout]')
    pubmed_filter.set_defaults(func=main)

    export = subparser.add_parser('export', help='export data to a file')
    export.add_argument('-o', '--outfile', help='the output filename')
    export.set_defaults(func=main)

    if len(sys.argv) == 1:
        parser.print_help()
        exit()

    args = parser.parse_args()

    return args


def main():

    kwargs = get_args()
    kwargs.func(**vars(kwargs))

    IF = ImpactFactor(**kwargs)

    if kwargs['cmd'] == 'version':
        IF.check_version()
    elif kwargs['cmd'] == 'search':
        res = IF.search(kwargs['keyword'], field=kwargs['field'])
        if res:
            print(json.dumps(res, indent=2))
        else:
            print('no result for keyword: {keyword}'.format(**kwargs))
    elif kwargs['cmd'] == 'build':
        if not (kwargs['entrez_file'] and kwargs['medline_file']):
            print('please supply J_Entrez and J_Medline file!')
        else:
            IF.build(kwargs['entrez_file'], kwargs['medline_file'], threads=kwargs['threads'])
    elif kwargs['cmd'] == 'pubmed_filter':
        IF.pubmed_filter(indexed=True, **kwargs)


if __name__ == '__main__':
    main()    
