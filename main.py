# encoding:utf8

import sys
import urllib2
import time
import re

from yicun import SentenceGenerator, Word


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

	text = text.decode('GBK').lower()
	# 过滤掉不要的，而且只取要的
	paras = [ filter1(p)  for p in re.split(u'<p[^>]+>', text) if filter2(p, kw)]
	
	text = filter3("\n".join(paras))

	fout.write(text.encode('utf8'))
	fout.close()
	content.close()

	return text

if __name__ == '__main__':
	kw = u'梅花'
	url = "http://www.gkstk.com/article/1383483811.html"
	print get_content_from_web(kw, url)