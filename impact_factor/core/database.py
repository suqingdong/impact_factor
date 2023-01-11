import functools

from sql_manager import DynamicModel, Manager
from sqlalchemy import Column, Float, String


columns = {
    'nlm_id': Column(String, comment='the unique ID of NLM', default='.'),
    'factor': Column(Float(3), comment='the IF of journal'),
    'jcr': Column(String, comment='the partition of JCR', default='.'),
    'journal': Column(String, comment='the title of journal', primary_key=True),
    'journal_abbr': Column(String, comment='the abbreviation of journal', default='.'),
    'issn': Column(String, comment='the ISSN of journal', default='.'),
    'eissn': Column(String, comment='the eISSN of journal', default='.'),
}

FactorData = DynamicModel('Factor', columns, 'factor')

FactorManager = functools.partial(Manager, FactorData)
