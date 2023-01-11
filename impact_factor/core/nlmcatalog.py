import os
from webrequests import WebRequest as WR

try:
    import lxml.etree as ET
except ImportError:
    import xml.etree.cElementTree as ET


class NlmCatalog(object):

    base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'

    _common_params = {'db': 'nlmcatalog'}

    _api_key = os.getenv('NCBI_API_KEY')
    if _api_key:
        print(f'use api_key: {_api_key}')
        _common_params['api_key'] = _api_key

    @classmethod
    def search(cls, term):
        """
            search term with efetch api,
            and return nlm_id and journal_abbr
        """
        url = f'{cls.base_url}esearch.fcgi'
        payload = {
            **cls._common_params,
            'term': term,
            'format': 'json',
        }
        result = WR.get_response(url, params=payload).json()['esearchresult']

        if (count := result['count']) != '1':
            print(f'{term} has {count} result!')
            return False

        nlm_id = result['idlist'][0]
        xml = cls.fetch(nlm_id)
        tree = cls.parse(xml)

        context = {}
        context['nlm_id'] = nlm_id
        context['journal_abbr'] = tree.findtext('NLMCatalogRecord/MedlineTA')
        
        return context

    @classmethod
    def fetch(cls, id):
        """
            fetch xml string from nlm_id
        """
        url = f'{cls.base_url}efetch.fcgi'
        payload = {
            **cls._common_params,
            'id': id,
            'format': 'xml',
        }
        resp = WR.get_response(url, params=payload)

        return resp.text

    @classmethod
    def parse(cls, xml):
        """
            return an etree object from xml
        """
        tree = ET.fromstring(xml)
        return tree


if __name__ == '__main__':
    NlmCatalog.search('0334-9152[ISSN]')
    NlmCatalog.fetch('101474857')