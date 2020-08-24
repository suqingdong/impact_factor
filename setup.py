# -*- encoding: utf8 -*-
import os
from setuptools import setup, find_packages


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
from impact_factor import __version__, __author__, __author_email__


setup(
    name='impact_factor',
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    description='Impact Factor Toolkits for Pubmed',
    long_description=open(os.path.join(BASE_DIR, 'README.md')).read(),
    long_description_content_type="text/markdown",
    url='https://github.com/suqingdong/impact_factor',
    project_urls={
        'Documentation': 'https://impact-factor.readthedocs.io',
        'Tracker': 'https://github.com/suqingdong/impact_factor/issues',
    },
    license='BSD License',
    install_requires=open(os.path.join(BASE_DIR, 'requirements.txt')).read().split('\n'),
    packages=find_packages(),
    include_package_data=True,
    entry_points={'console_scripts': [
        'impact_factor = impact_factor.bin.main:run',
        'IF = impact_factor.bin.main:run',
    ]},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ]
)
