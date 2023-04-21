import json
import sys
import math
import operator
import copy
from collections import defaultdict


def apriori(min_sup, min_conf, L1, D, lineCount):
	L1 = getLargeOneItemsets(L1, min_sup, lineCount)
	L = [L1]
	k = 1

	while (len(L[k-1]) != 0):
		Ck = aprioriGen(L[k - 1], k)
		c = defaultdict(int)

		for t in D:
			Ct = subset(Ck, t)
			for item in Ct:
				itemTuple = tuple(item)
				c[itemTuple] += 1

		Lk = getLargeOneItemsets(c, min_sup, lineCount)
		L.append(Lk)
		k += 1

	writeFrequentItemsets(L, lineCount, min_sup)
	writeAssociationRules(L, lineCount, min_sup, min_conf)

def getLargeOneItemsets(L1, min_sup, lineCount):
    return {key: value for key, value in L1.items() if value / lineCount >= min_sup}


def aprioriGen(Lk_1, k):
    Ck = []
    itemsets = list(Lk_1.keys())
    for index, itemset1 in enumerate(itemsets):
        for itemset2 in itemsets[index+1:]:
            if k == 1:
                candidate = [itemset1] + [itemset2]
                Ck.append(candidate)
            else:
                common_items = [i for i in itemset1 if i in itemset2]
                candidate = set(itemset1 + itemset2)								 
                if len(common_items) == (k-1) and (candidate not in Ck):
                    Ck.append(candidate)

    return Ck


def subset(Ck, t):
    Ct = [itemset for itemset in Ck if set(itemset).issubset(set(t))]
    return Ct

def convertToPercentage(num):
    return float(num) * 100

def writeFrequentItemsets(L, lineCount, min_sup):
    with open('output.txt', 'w') as file:
        file.write("==Frequent itemsets (min_sup={min_sup_percent}%)\n".format(min_sup_percent = convertToPercentage(min_sup)))
        
        frequency_itemset = {item: itemset[item] for itemset in L for item in itemset}
        sorted_frequency_itemset = sorted(frequency_itemset.items(), key=lambda x: x[1], reverse=True)

        for item, count in sorted_frequency_itemset:
            file.write("[{item}], {support}%\n".format(item=item, support = convertToPercentage(count/lineCount)))
    
        file.write("\n")


def writeAssociationRules(L, lineCount, min_sup, min_conf):
    finFreqList = {}
    association_rules = {}
    min_conf_percent = convertToPercentage(min_conf)

    with open('output.txt', 'a') as file:
        file.write(f"==High-confidence association rules (min_conf={min_conf_percent:.2f}%)\n")

        for itemset in L:
            for item in itemset:
                key = (item,) if not isinstance(item, tuple) else item
                finFreqList[key] = itemset[item]

        for itemset in finFreqList:
            # ignore L1 itemsets
            if len(itemset) == 1:
                continue

            for element1 in itemset:
                # Rule: antecedent (if) => consequent (then)
                RHS = (element1,)
                LHS = tuple([item for item in itemset if item not in RHS])
                union = itemset

                if union not in finFreqList or LHS not in finFreqList:
                    continue

                sup_R = finFreqList[union] / lineCount
                conf_R = finFreqList[union] / finFreqList[LHS]

                # rule should satisfy confidence and support constraints
                # there should be at least one antecedent & exactly one consequent in the output
                if sup_R > float(min_sup) and conf_R > float(min_conf):
                    key = "{LHS} => {RHS}".format(LHS = list(LHS), RHS=list(RHS))
                    value = [conf_R * 100, sup_R * 100]
                    association_rules[key] = value

        # sort rules by confidence
        sorted_association_rules = sorted(association_rules.items(), key = lambda x: x[1][0], reverse=True)

        for rule in sorted_association_rules:
            file.write('{} (Conf: {}%, Supp: {} %)\n'.format(rule[0], rule[1][0], rule[1][1]))

