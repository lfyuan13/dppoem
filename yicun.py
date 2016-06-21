# encoding:utf8
import sys
import time
import re
import urllib2


child_relation = {"SBV", "VOB", "ATT", "ADV"}
brother_relation = {"COO"}
ignored_pos = {"r", "u"}

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
	def __init__(self, pos="", word="", is_root=False, index=0):
		"""
			构建本节点的：left or right 关系
			新节点的：pre关系
			word: is string

		"""
		if is_root:
			self.word = ""
		self.word = word
		self.pos = pos
		self.index = index
		self.right = []
		self.left = []
		self.pre = []
		

	def add(self, relation=None, word=None):
		"""
			word is Word, not string
		"""
		
		if relation in ['ATT', 'SBV', 'ADV']:
			self.left.append(word)
		elif relation in ['VOB']:
			self.right.append(word)
		else:
			self.left.append(word)
		word.setPre(self)

	def setPre(self, word):
		self.pre.append(word)

	def getLeft(self):
		return self.left

	def getRight(self):
		return self.right

	def getWord(self):
		return "".join([self.word, self.pos, str(self.index)])

	def getPos(self):
		return self.pos


def print_tree(node, level):
	if node is None:
		return
	if node.getLeft() is not None:
		for left in node.getLeft():
			print_tree(left, level+1)
	if node.getPos() not in ignored_pos:
		print " "*level, node.getWord()
	if node.getRight() is not None:
		for right in node.getRight():
			print_tree(right, level+1)


def pop_item(li, kw, idx):
	"""
		从列表里获取满足条件的元素
	"""
	res = []
	flag = True
	while flag:
		flag = False
		for i, item in enumerate(li):
			if item[idx] == kw:
				res.append(li.pop(i)) 
				flag = True
				break
	return res


def add_node(node, word, dp_list, pos_map, relat, dictionary):
	"""
		这一个函数应该是一个递归
		word is string
		dp_list: dp list
		pos_map: pos map
	"""

	node_tmp = Word(pos=pos_map[word], word=word, index=dictionary[word])
	node.add(relation=relat, word=node_tmp)

	res = pop_item(dp_list, word, 1)
	if res is None or len(res) ==0:
		pass
	else:
		for item in res:
			if item[2] in child_relation:
				add_node(node_tmp, item[0], dp_list, pos_map, item[2], dictionary)
			elif item[2] in brother_relation:
				add_node(node, item[0], dp_list, pos_map, item[2], dictionary)


def generate_tree(dp_list=None, pos_map=None, dictionary=None):
	root_tuple = pop_item(dp_list, -1, 1)[0]
	root_node = Word(word="", is_root=True, index=-1)

	add_node(root_node, root_tuple[0], dp_list, pos_map, root_tuple[2], dictionary)

	print_tree(root_node, 0)




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

	print "dp:", dp_list2
	pos = analyze(sent, 'pos')
	pos_list = [p for p in pos.split(" ")]
	pos_map = {}
	root = Word()
	for item in pos_list:
		w1, p1 = item.split("_")
		pos_map[w1] = p1
	print "pos:", pos_map
	generate_tree(dp_list2, pos_map, dictionary)
		# print w1, p1
	#print pos

# generate1("那花白里透红，花瓣润滑透明，像一颗颗价值不菲的水晶。")
# generate1("梅花的色，艳丽而不妖")

generate1("那花白里透红，花瓣润滑透明，像一颗颗价值不菲的水晶。")

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


