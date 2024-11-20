from sqlalchemy import func


from impact_factor import DEFAULT_DB, util
from .database import FactorData, FactorManager


class Factor(object):
    """Impact Factor ToolKits

    examples:
        >>> from impact_factor.core import Factor
        >>> fa = Factor()
        >>> fa.search('nature')
        >>> fa.search('nature c%')
        >>> fa.search('1579-3680', key='eissn')
        >>> fa.filter(min_value=5, max_value=6)
    """

    def __init__(self, dbfile=DEFAULT_DB):
        self.dbfile = dbfile
        self.manager = FactorManager(dbfile)
        self.query = self.manager.session.query(FactorData)

    def search(self, value, key=None):
        """
            search something
        """
        default_keys = ['issn', 'eissn', 'nlm_id', 'journal', 'journal_abbr']
        keys = [key] if key else default_keys

        for field in keys:
            if '%' in value:
                result = self.query.filter(
                    FactorData.__dict__[field].like(value))
            else:
                result = self.query.filter(
                    func.lower(FactorData.__dict__[field]) == func.lower(value))

            if result.count():
                data = [util.record_to_dict(record) for record in result]
                return data

        return []

    def filter(self, min_value=None, max_value=None, pubmed_filter=False, limit=None, **kwargs):
        """
            filter factor, or generate pubmed filter
        """
        query = self.query

        if min_value is not None:
            query = query.filter(FactorData.factor >= min_value)

        if max_value is not None:
            query = query.filter(FactorData.factor <= max_value)

        if pubmed_filter:
            query = query.filter(FactorData.nlm_id != '.', FactorData.factor != 0)
            return util.pubmed_filter_builder(query)
        
        if limit and (count := query.count()) > limit:
            self.manager.logger.warning(f'{count} records found, but limit is {limit}')
            query = query.limit(limit)
    
        return [util.record_to_dict(record) for record in query]
