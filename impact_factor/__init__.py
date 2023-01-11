import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

DEFAULT_DB = BASE_DIR.joinpath('data', 'impact_factor.sqlite3')
DEFAULT_EXCEL = BASE_DIR.joinpath('data', '2022_JCR_IF.xlsx')

version_info = json.load(BASE_DIR.joinpath('version.json').open())

__version__ = version_info['version']
