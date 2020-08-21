import json

from impact_factor.util.webrequest import WebRequest


BASE_URL = 'http://www.greensci.net/search?kw='


def fetch_factor(*kws):
    for kw in kws:
        url = BASE_URL + kw
        resp = WebRequest.get_response(url)
        soup = WebRequest.get_soup(resp)

        context = {}

        trs = soup.select('table tr')
        if len(trs) > 2:
            print('multiple result for kw: {}'.format(kw))
        elif len(trs) < 2:
            print('no result for kw: {}'.format(kw))
        else:
            title = [th.text for th in trs[0].find_all('th')[2:]]
            values = [td.text for td in trs[1].find_all('td')[2:]]
            if values[-1]:
                context['factor_history'] = json.dumps(dict(zip(title, values)))
                context['factor'] = values[-1]
                context['kw'] = kw
        if context:
            return context


if __name__ == '__main__':
    # print(fetch_factor('0028-0836'))
    # print(fetch_factor('0028-0836XXX'))
    # print(fetch_factor('Nature'))
    print(fetch_factor('0959-8138'))  # ISSN
    print(fetch_factor('0959-8138', '1756-1833')) # ISSN, E_ISSN
    print(fetch_factor('0959-8138', 'nature comm')) # ISSN, Journal
