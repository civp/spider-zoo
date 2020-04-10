import requests
from bs4 import BeautifulSoup

src_url = 'https://vjudge.net/'

def fetch(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
    resp = requests.get(url, headers=headers)
    return resp

def parse(resp):
    soup = BeautifulSoup(resp.text, 'lxml')
    content = soup.find('div', attrs = {'class': 'col-md-8 push-md-4'})
    
    oj_url = []
    oj_img = []
    for oj in content.find_all('a'):
        #there are two irrelevant links in content
        if oj.find('img'):    
            oj_url.append(oj['href'])
            oj_img.append(oj.find('img')['src'])
    
    return oj_img, oj_url

def main():
    res = fetch(src_url)
    img, url = parse(res)
    
    with open('oj.txt', 'w') as fp:
        for u in url:
            fp.write(u + '\n')
    
    cnt = 0
    for i in img:
        link = src_url + i
        responce = fetch(link)
        with open(u'{name}.jpg'.format(name=cnt), 'wb') as fp:
            fp.write(responce.content)
            cnt += 1
    
if __name__ == '__main__':
    main()     
