import os


from impact_factor.util.webrequest import WebRequest

BASE_URL = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
API_KEY = os.getenv('NCBI_API_KEY')


def get_nlmid(term='currentlyindexed', retstart=0, retmax=250):
    payload = {
        'db': 'nlmcatalog',
        'term': term,
        'retmode': 'json',
        'retstart': retstart,
        'retmax': retmax,
    }
    if API_KEY:
        payload['api_key'] = API_KEY

    resp = WebRequest.get_response(BASE_URL, params=payload).json()
    result = resp['esearchresult']
    
    next_start = int(result['retstart']) + int(result['retmax'])
    yield result['idlist']

    if next_start < int(result['count']):
        for each in get_nlmid(term, retstart=next_start, retmax=retmax):
            yield each


if __name__ == '__main__':
    nlmid_list = [nid for each in get_nlmid() for nid in each]
    print(nlmid_list[:10])
    print(len(nlmid_list))

    


