# encoding:utf8

import sys
import urllib2
import time
import re

from yicun import SentenceGenerator, Word
from bs4 import BeautifulSoup as BS

perfect_website = [
"www.sanwen.net", 
"blog.sina.com.cn"
]

baidu_search_url = "http://www.baidu.com/s?wd=%s"
sanwen_search_url = "http://s.sanwen.net/cse/search?q=%s&s=16369095755888262684&nsid=1"

def filter1(text):
	return re.sub('<[^>]+>', '', text)


def filter2(text, word):
	if word in text:
		return True
	else:
		return False

def filter3(text):
	return re.sub('[a-zA-Z0-9&]', '', text)


def get_content_from_web(kw, url):
	content = urllib2.urlopen(url)
	text = ""
	for line in content:
		text += line
	fout = open('test.txt', 'w+')

	text = text.decode('utf8').lower()
	# 过滤掉不要的，而且只取要的
	paras = [ filter1(p)  for p in re.split(u'<p[^>]+>', text) if filter2(p, kw)]
	
	text = filter3("\n".join(paras))

	fout.write(text.encode('utf8'))
	fout.close()
	content.close()

	return text


def search_from_web_baidu(kw):
	search_url = baidu_search_url % kw
	fin = urllib2.urlopen(search_url).readlines()
	content = ""
	for line in fin:
		content += line
	content = content.decode("utf8")
	bs = BS(content)

	content_left = bs.find(id="content_left")

	urls = []
	divs = content_left.find_all(class_="c-container")
	# print "div size:", len(divs)
	for i, div in enumerate(divs):
		if i == 3:
			break
		# print i, "======", div
		a = div.find_all("a")
		if a is None or len(a)==0:
			continue
		urls.append(a[0]['href'])
	return urls


def search_from_web_sanwen(kw):
	search_url = sanwen_search_url % kw
	fin = urllib2.urlopen(search_url).readlines()
	content = ""
	for line in fin:
		content += line
	content = content.decode("utf8")
	bs = BS(content)

	content_left = bs.find(id="results")

	urls = []
	divs = content_left.find_all(class_="result")
	# print "div size:", len(divs)
	for i, div in enumerate(divs):
		if i == 3:
			break
		# print i, "======", div
		a = div.find_all("a")
		if a is None or len(a)==0:
			continue
		urls.append(a[0]['href'])
	return urls


if __name__ == '__main__':
	kw = '梅花散文'
	url = u"http://www.gkstk.com/article/1383483811.html"
	urls = search_from_web_sanwen(kw)

	test_file_base = "test_%s"
	kwd = u"梅花"
	for i, url in enumerate(urls):
		print url
		with open(test_file_base % i, 'w+') as fout:
			text = get_content_from_web(kwd, url)
			fout.write(text.encode("utf8"))



	# print get_content_from_web(kw, url)