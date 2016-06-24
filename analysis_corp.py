# encoding:utf8

import sys 
import jieba
import time

import re


class Analyzer(object):
	def __init__(self, stop_words=[]):
		self.stop_words = stop_words
		self.term_inner_relation = {}
		self.term_outer_relation = {}


	def analyze(self, sentence):
		res = jieba.cut(sentence, cut_all=False)
		pre_term = "^"  # 表示开头
		for term in res:
			if term in self.stop_words:
				continue
			else:
				if len(term) > 1:
					pre_word = term[0]
					for word in term[1:]:
						k = "_".join([pre_word, word])
						if not self.term_inner_relation.has_key(k):
							self.term_inner_relation[k] = 0
						self.term_inner_relation[k] += 1
						pre_word = word
				k = "_".join([pre_term[-1], term[0]])
				if not self.term_outer_relation.has_key(k):
					self.term_outer_relation[k] = 0
				self.term_outer_relation[k] += 1
				pre_term = term

	def parse(self, corp):
		"""
			corp是训练语料，是一个句子组成的列表
		"""
		for sentence in corp:
			self.analyze(sentence)

	def save(self, inner_file_name, outer_file_name):
		def write(data, file_name):
			with open(file_name, 'w+') as fout:
				for k, v in data.items():
					line = k + "\t" + str(v) + "\n"
					fout.write(line.encode("utf8"))
		write(self.term_outer_relation, outer_file_name)
		write(self.term_inner_relation, inner_file_name)

def read_in(file_name):
	res = []
	with open(file_name) as fin:
		for line_ in fin:
			try:
				line = line_.strip().decode("utf8").split("$")
				if line == "":
					continue
				line_str = ".".join(line[1:])
				res.append(line_str)
			except Exception as e:
				print line_, e
	return res


if __name__ == '__main__':
	stop_words = [
	u"的", u"啊", u"那", u"这", u"那个", u"这个", u"得"
	]
	corp = []
	# corp += read_in("isoverseas0.txt")
	# corp += read_in("isoverseas1.txt")
	corp.append("今天的天气不错啊")
	corp.append("明天我就要去世纪公园玩")
	a = Analyzer( stop_words)
	a.parse(corp)
	a.save("term_inner_relation.txt", "term_outer_relation.txt")





				


				


