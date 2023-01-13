from sqlalchemy.orm.state import InstanceState
from pygments import highlight, lexers, formatters

from .excel_parser import parse_excel


def highlight_json(jsons):
    """
        highlight json string with pygments
    """
    return highlight(
        jsons,
        lexers.JsonLexer(),
        formatters.TerminalFormatter()
    )


def record_to_dict(records):
    """
        convert Query result to dict
    """
    return {
        k: v
        for k, v in records.__dict__.items()
        if not isinstance(v, InstanceState)
    }


def pubmed_filter_builder(records):
    res = '|'.join(
        # f'{record.nlm_id}[Journal]'
        record.issn
        for record in records
        if record.nlm_id
    )
    if (length := len(res)) > 4000:
        raise Exception(
            f'pubmed filter limit 4000 characters, yours is {length}, please change your factor range'
        )
    return res
