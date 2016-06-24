# encoding:utf8
import sys
import time
import re
import urllib2
from graph import Graph, GraphNode
from utils import pop_item


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
		self.mode = "NODE"
		

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
		return self.word

	def toString(self):
		return " ".join([self.word, self.pos, str(self.index), self.mode])

	def getPos(self):
		return self.pos
	def setMode(self, mode):
		self.mode = mode
	def getMode(self):
		return self.mode


class SentenceGenerator(object):
	def __init__(self):
		self.graph = Graph()

	def init_start_node(self, root_node):
		"""
			设置句法树可能的开始节点
		"""
		start_node_list = []

		def iterate(node, res):
			if node is None:
				return
			if len(node.getLeft()) > 0:
				for nd in node.getLeft():
					iterate(nd, res)
			else:
				return res.append(node)

		iterate(root_node, start_node_list)
		
		for node in start_node_list:
			# print node.getWord()
			node.setMode("START")



	def init_end_node(self, root_node):
		"""
			设置句法树可能的结束节点
		"""
		end_node_list = []

		def iterate(node, res):
			if node is None:
				return
			
			if len(node.getRight()) > 0:
				for nd in node.getRight():
					iterate(nd, res)
			else:
				return res.append(node)

		iterate(root_node, end_node_list)
		
		for node in end_node_list:
			node.setMode("END")


	def add_node(self, node, word, dp_list, pos_map, relat, dictionary):
		"""
			生成句法树的递归函数:这一个函数应该是一个递归
			word is string
			dp_list: dp list
			pos_map: pos map
		"""
		node_tmp = None
		if pos_map[word] in ignored_pos:
			node_tmp = node
		else:
			node_tmp = Word(pos=pos_map[word], word=word, index=dictionary[word])
			node.add(relation=relat, word=node_tmp)

		res = pop_item(dp_list, word, 1)
		if res is None or len(res) ==0:
			pass
		else:
			for item in res:
				# 这里对不需要的字进行过滤
				# if pos_map[item[0]] in ignored_pos:
				# 	continue
				if item[2] in child_relation:
					self.add_node(node_tmp, item[0], dp_list, pos_map, item[2], dictionary)
				elif item[2] in brother_relation:
					self.add_node(node, item[0], dp_list, pos_map, item[2], dictionary)


	def generate_tree(self, dp_list=None, pos_map=None, dictionary=None):
		"""
			根据句子依存关系生成一个句法依存树
		"""
		root_tuple = pop_item(dp_list, -1, 1)[0]
		root_node = Word(word="", is_root=True, index=-1)

		self.add_node(root_node, root_tuple[0], dp_list, pos_map, root_tuple[2], dictionary)

		for nd in root_node.getLeft():
			self.init_end_node(nd)
			self.init_start_node(nd)
		
		self.generate_graph(root_node, 0)
		print "build tree ok..."
		self.graph.take_all(7)


	def generate_graph(self, node, level):
		"""
			根据句法依存树生成一个 句法图
		"""
		if node is None:
			return
		
		if node.getLeft() is not None:
			for left in node.getLeft():
				self.generate_graph(left, level+1)
		# if node.getPos() not in ignored_pos:
		if node.getWord() == "-1":
			pass
		else:

			self.graph.add_node(node.getWord(), node.getPos(), node.getMode())
			print " "*level, node.toString()
		if node.getRight() is not None:
			for right in node.getRight():
				self.generate_graph(right, level+1)


	def generate(self, sent):
		"""
			根据传入进来的原句生成一句诗句
		"""
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
		self.generate_tree(dp_list2, pos_map, dictionary)
	

def generate(sent):
	sg = SentenceGenerator()
	sg.generate(sent)

if __name__ == '__main__':
	# generate("梅花的色，艳丽而不妖")
	# generate("那花白里透红，花瓣润滑透明，像一颗颗价值不菲的水晶。")
	# generate("梅花那顽强不屈的精神却更令我赞叹")
	generate("梅花在中华传统文化中象征着傲骨，高洁")

# generate1("那花白里透红，花瓣润滑透明，像一颗颗价值不菲的水晶。")
# generate1("梅花的色，艳丽而不妖")

# generate1("那花白里透红，花瓣润滑透明，像一颗颗价值不菲的水晶。")

# generate1("梅花乃是岁寒三友中的领头羊，它生性坚毅、不服输")
# generate1("梅花之所以香气袭人，是因为他不畏寒冷")



