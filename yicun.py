# encoding:utf8
import sys
import time
import re
import urllib2



def analyze(text, pattern='dp'):
	url_get_base = "http://api.ltp-cloud.com/analysis/?"
	api_key = 'o7t1j5w53XHlss4ZsOCUfRlmrP9o7TiyMHuBDBeI'
	format = 'plain'
	# pattern = 'dp'
	result = urllib2.urlopen("%sapi_key=%s&text=%s&format=%s&pattern=%s" % (url_get_base,api_key,text,format,pattern))
	content = result.read().strip()
	return content.decode('utf8')


def filter1(text):
	return re.sub('<[^>]+>', '', text)


def filter2(text, word):
	if word in text:
		return True
	else:
		return False


class Word(object):
	def __init__(self, pos=None, word=None, is_root=False):
		"""
			构建本节点的：left or right 关系
			新节点的：pre关系
			word: is string

		"""
		if is_root:
			self.word = ""
		self.word = word
		self.pos = pos
		self.right = None
		self.left = None
		self.pre = None
		

	def add(self, relation=None, word=None):
		"""
			word is Word, not string
		"""
		
		if relation in ['ATT', 'SBV', 'ADV']:
			self.left = word
		elif relation in ['VOB']:
			self.right = word
		else:
			self.left = word
		word.setPre(self)

	def setPre(self, word):
		self.pre = word

	def getLeft(self):
		return self.left

	def getRight(self):
		return self.right

	def getWord(self):
		return self.word


def print_tree(node):
	if node is None:
		return
	if node.getLeft() is not None:
		print_tree(node.getLeft())
	print node.getWord()
	if node.getRight() is not None:
		print_tree(node.getRight())



def generate_tree(dp=None, pos=None):

	root = Word( is_root=True )
	left = Word( pos='n', word=u'你好')
	root.add(relation='HED', word=left)
	right = Word( pos='n', word=u'厉害')
	root.add(relation="VOB", word=right)
	print_tree(root)
	# print_tree(left)



def generate1(sent):
	dictionary = {}
	dp = analyze(sent)
	dp_list = [w for w in dp.split("\n") ]
	dp_list2 = []
	for item in dp_list:
		w1, w2, w3 = item.split(" ")
		word1, num1 = w1.split("_")
		dictionary[word1] = num1

		if w2 == "-1":
			word2 = -1
		else:
			word2, num2 = w2.split("_")
			dictionary[word2] = num2

		dp_list2.append((word1, word2, w3))

	print dp_list2
	pos = analyze(sent, 'pos')
	pos_list = [p for p in pos.split(" ")]
	pos_list2 = []
	root = Word()
	for item in pos_list:
		w1, p1 = item.split("_")

		# print w1, p1
	#print pos

# generate1("那花白里透红，花瓣润滑透明，像一颗颗价值不菲的水晶。")
# generate1("梅花的色，艳丽而不妖")

generate_tree()

# kw = u'梅花'
# url = "http://www.gkstk.com/article/1383483811.html"
# content = urllib2.urlopen(url)
# text = ""
# for line in content:
# 	text += line
# fout = open('test.txt', 'w+')

# text = text.decode('GBK').lower()

# paras = [ filter1(p)  for p in re.split(u'<p[^>]+>', text) if filter2(p, kw)]
# print "size:", len(paras)
# text = "\n".join(paras)
# fout.write(text.encode('utf8'))
# fout.close()
# print text.encode('utf8')

# content.close()


