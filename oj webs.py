# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 16:38:07 2017

@author: Chief-P
"""

import requests
from bs4 import BeautifulSoup

URL = 'https://vjudge.net/'

def fetch(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
    resp = requests.get(url, headers = headers)
    return resp

def parse(resp):
    soup = BeautifulSoup(resp.text, 'lxml')
    content = soup.find('div', attrs = {'class': 'col-md-8 push-md-4'})
    
    oj_url = []
    oj_img = []
    for oj in content.find_all('a'):
       oj_url.append(oj['href'])
       oj_img.append(oj.find('img'))
    
    return oj_img, oj_url

def main():
    res = fetch(URL)
    img, url = parse(res)
    
    with open('oj.txt', 'w') as fp:
        for u in url:
            fp.write(u + '\n')
    
    cnt = 0
    for i in img:
        web = URL + i['src']
        responce = fetch(web)
        with open(u'{name}.jpg'.format(name = cnt), 'wb') as fp:
            fp.write(responce.content)
            cnt += 1
    
if __name__ == '__main__':
    main()    