# encoding:utf8

import sys
import time

class GraphNode(object):

	def __init__(self, word, pos, mode, next):
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


class Graph(object):
	def __init__(self):
		pass

	def add_node(self):
