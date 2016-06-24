# encoding:utf8

import sys
import time

END = "END"
START = "START"
NODE = "NODE"

class GraphNode(object):

	def __init__(self, word, pos, mode):
		"""
			word is string
			pos : is pos tag
			mode: END, START, NODE
			next: list(GraphNode)
		"""
		self.word = word
		self.pos = pos
		self.mode = mode
		self.next = []

	def add_next(self, node):
		"""
			添加相关联的下一个节点
		"""
		self.next.append(node)

	def get_next_list(self):
		"""
			返回该节点的所有next列表
		"""
		return self.next

	def get_word(self):
		return self.word

	def get_mode(self):
		return self.mode

	def is_end(self):
		if self.mode == END:
			return True
		return False


class Graph(object):
	def __init__(self):
		self.root = None
		self.cur = []  # 这是一个等待连接的节点(GraphNode)列表
		self.start_list = []
		self.result = []


	def add_node(self, words, pos, mode):
		pre = self.cur
		self.cur = []
		tmp_node = None
		for word in words:
			node = GraphNode(word, pos, mode)
			if mode == START:
				self.start_list.append(node)
			if self.root is None:
				self.root = node  # init self node
			self.cur.append(node)
			for nd in pre:
				nd.add_next(node)
			if tmp_node is None:
				tmp_node = node
			else:
				tmp_node.add_next(node)
				tmp_node = node


	def take_all(self, length=7):
		"""
			计算所有的可能句子组合
		"""
		def print_result(res):
			sent = ""
			for node in res:
				sent += node.get_word()
				print node.get_word(),"->",
			self.result.append(sent)
			print len(res),""

		def iterate(node, result):
			if node is None:
				return
			result.append(node)
			next_list = node.get_next_list()
			if len(next_list)==0 or node.is_end():
				if length == -1:
					print_result(result)
				if len(result) == length:
					print_result(result)

				# return
			for next_node in next_list:
				# result.append(next_node)
				iterate(next_node, result)
				result.pop()
		self.result = []
		for nd in self.start_list:
			iterate(nd, [])
		# iterate(self.root, [])
		return self.result




if __name__ == "__main__":
	graph = Graph()
	graph.add_node(u"花白", 'n', "START")
	graph.add_node(u"里", 'n', "NODE")
	graph.add_node(u"透", 'n', "NODE")
	graph.add_node(u"红", 'n', "END")
	graph.add_node(u"花瓣", 'n', "NODE")
	graph.add_node(u"润滑", 'n', "END")
	graph.add_node(u"透明", 'n', "END")
	graph.add_node(u"像", 'n', "NODE")
	graph.add_node(u"一颗颗", 'n', "NODE")
	graph.add_node(u"价值", 'n', "NODE")
	graph.add_node(u"不菲", 'n', "NODE")
	graph.add_node(u"水晶", 'n', "END")

	graph.take_all(7)



