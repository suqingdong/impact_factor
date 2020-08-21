import random

import bs4
import time
import requests




class WebRequest(object):

    UA_LIST = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
        'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',

    ]

    @classmethod
    def get_response(cls, url, method='GET', **kwargs):

        if 'headers' not in kwargs or 'User-Agent' not in kwargs['headers']:
            kwargs['headers'] = {
                'User-Agent': random.choice(cls.UA_LIST)
            }
            
        try:
            resp = requests.request(method, url, **kwargs)
            if resp.status_code != 200:
                exit(1)
            return resp
        except Exception as e:
            print('request failed for url: {} [as {}]'.format(url, e.message))
            time.sleep(3)
            return cls.get_response(url, method='GET', **kwargs)

    @classmethod
    def get_soup(cls, text):
        if isinstance(text, requests.models.Response):
            text = text.text
        try:
            soup = bs4.BeautifulSoup(text, 'lxml')
        except:
            soup = bs4.BeautifulSoup(text, 'html.parser')
        return soup


if __name__ == '__main__':
    url = 'http://www.greensci.net/search?kw=0028-0836'

    resp = WebRequest.get_response(url)
    soup = WebRequest.get_soup(resp.text)

    trs = soup.select('table tr')
    if len(trs) != 2:
        exit('multiple result ...')
    
    title = [th.text for th in trs[0].find_all('th')[2:]]
    values = [td.text for td in trs[1].find_all('td')[2:]]
    print(title)
    print(values)
    print(dict(zip(title, values)))