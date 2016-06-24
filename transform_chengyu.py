# encoding:utf8

f = open('/Users/lfyuan/Downloads/成语词典.txt')
fout = open('./chengyu.txt', 'w+')
for line in f:
	try:
		line = line.decode('GBK')
	except Exception as e:
		print e
		continue
	fout.write(line.encode('utf8'))

fout.close()
f.close()