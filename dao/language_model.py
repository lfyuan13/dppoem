# encoding:utf8
__author__ = 'lfyuan'

import sys
import re
import math

def read_in(file_name, data):
    max_score = 0.0
    with open(file_name) as fin:

        for line in fin:
            try:
                k, v = line.strip().decode("utf8").split("\t")

                # k1, k2 = k.split("_")
                v = float(v)
                if v > max_score:
                    max_score = v
                data[k] = v
            except Exception as e:
                pass
                # print line.strip(), e

    return max_score


def normalize(data, max_score):
    for k in data.keys():
        data[k] = math.sqrt(data[k])*1.0/math.sqrt(max_score)


class LanguageModel(object):
    def __init__(self):
        self.term_inner_relation = {}
        self.term_outer_relation = {}
        inner_max = read_in("data/term_inner_relation.txt", self.term_inner_relation)
        outer_max = read_in("data/term_outer_relation.txt", self.term_outer_relation)
        normalize(self.term_inner_relation, inner_max)
        normalize(self.term_outer_relation, outer_max)



    def get_score(self, word1, word2, is_inner):
        k = "_".join([word1, word2])
        if is_inner:
            if self.term_inner_relation.has_key(k):
                return self.term_inner_relation[k]
        else:
            if self.term_outer_relation.has_key(k):
                return self.term_outer_relation[k]
        return 0.0


if __name__ == "__main__":
    lm = LanguageModel()
    print lm.get_score(u"柳", u"树", True)
    print lm.get_score(u"柳", u"树", False)








