import requests
from bs4 import BeautifulSoup
import datetime
from os import mkdir


url = 'SOME BAD WEBSITE'
now = datetime.datetime.now()
date = str(now.year) + '_' + str(now.month) + '_' + str(now.day)
path = './' + date


def fetch(url):
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
	resp = requests.get(url, headers=headers)

	return resp


def get_tails(resp):
	soup = BeautifulSoup(resp.text, 'lxml')
	main_item = soup.find('li', attrs={'class':'teaser stco__teaser--main-story'})
	rest_items = soup.find_all('li', attrs={'class':'teaser st-co__teaser--rest-story stco__rest'})

	tails = []
	tails.append(main_item.find('a').get('href'))
	for item in rest_items:
		tails.append(item.find('a').get('href'))

	return tails


def get_news(resp):
	soup = BeautifulSoup(resp.text, 'lxml')
	article = soup.find('article')
	titles = article.find('h1').find_all('span')
	flytitle, title = titles[0].string, titles[1].string
	description = article.find(itemprop='description').string
	post_inner = article.find('div', attrs={'class':'blog-post__inner'})
	
	content = flytitle + '\n' + title + '\n' + description + '\n'
	texts = post_inner.find_all('p')
	for text in texts:
		content += text.getText() + '\n'

	return content, title


def regularize_fn(fn):
	fn = fn.replace('/', ' or ')
	fn = fn.replace(':', '-')
	fn = fn.replace('|', '-')
	fn = fn.replace('\"', '\'')
	fn = fn.replace('<', '')
	fn = fn.replace('>', '')
	fn = fn.replace('\\', '')
	fn = fn.replace('?', '')

	return fn


def write_data(data, title):
	fn = path + '/' + regularize_fn(title) + '.txt'
	with open(fn, 'w', errors='ignore') as f:
		f.write(data)


def main():
	tails = get_tails(fetch(url))

	news_list = []
	for tail in tails:
		news_list.append(get_news(fetch(url + tail)))

	try:
		mkdir(path)
	except FileExistsError:
		pass
	for content, title in news_list:
		write_data(content, title)


if __name__ == '__main__':
	main()