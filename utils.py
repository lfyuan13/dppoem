# encoding:utf8


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