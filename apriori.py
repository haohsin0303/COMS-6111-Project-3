import json
import sys
import math
import operator
import copy
from collections import defaultdict


def runApriori(min_sup, min_conf, L1, D, totalNumOfRows):
	L1 = getLargeOneItemsets(L1, min_sup, totalNumOfRows) # generate L1 = {large 1-itemsets}
	L = [L1]
	k = 1

	while (len(L[k-1]) != 0):
		Ck = aprioriGen(L[k-1], k) # New candidates
		c = defaultdict(int)

		for t in D:
			Ct = subset(Ck, t) # Candidates contained in t
			for candidate in Ct:
				candidateTuple = tuple(candidate)
				c[candidateTuple] += 1     # c.count++

		Lk = filterItemsets(c, min_sup, totalNumOfRows)
		L.append(Lk)
		k += 1

	writeFrequentItemsets(L, totalNumOfRows, min_sup)
	writeAssociationRules(L, totalNumOfRows, min_sup, min_conf)


def filterItemsets(c, min_sup, totalNumOfRows):
    """
    Filters the candidates whose count is greater than minsup
    Lk = {c ∈ Ck | c.count >= minsup} 
    
    """
    return {item: candidate_count for item, candidate_count in c.items() if candidate_count / totalNumOfRows >= min_sup}

def getLargeOneItemsets(L1, min_sup, totalNumOfRows):
    """
    Generates the large 1-itemsets at the start of apriori
    
    """
    return {item: candidate_count for item, candidate_count in L1.items() if candidate_count / totalNumOfRows >= min_sup}


def aprioriGen(Lk_1, k):
    Ck = []
    itemsets = list(Lk_1.keys())
    for index, itemset1 in enumerate(itemsets):
        for itemset2 in itemsets[index+1:]:
            if k == 1:
                Ck.append([itemset1, itemset2])
            else:
                common_items = [item for item in itemset1 if item in itemset2]
                candidate = set(itemset1 + itemset2)								 
                if len(common_items) == (k-1) and (candidate not in Ck):
                    Ck.append(candidate)

    return Ck



def subset(Ck, t):
    """
    Finds which generated candidates from Ck are a subset of the transaction t
    and returns a list.
    """
    
    Ct = [itemset for itemset in Ck if set(itemset).issubset(set(t))]
    return Ct

def convertToPercentage(num):
    """
    Helper function to convert min_sup or min_conf to percentages
    Used for file writing
    """
    return float(num) * 100

def writeFrequentItemsets(L, totalNumOfRows, min_sup):
    with open('output.txt', 'w') as file:
        file.write("==Frequent itemsets (min_sup={min_sup_percent}%)\n".format(min_sup_percent = convertToPercentage(min_sup)))
        
        frequency_itemset = {item: itemset[item] for itemset in L for item in itemset}
        sorted_frequency_itemset = sorted(frequency_itemset.items(), key=lambda x: x[1], reverse=True)

        for item, count in sorted_frequency_itemset:
            file.write("[{item}], {support}%\n".format(item=item, support = convertToPercentage(count/totalNumOfRows)))
    
        file.write("\n")

def writeAssociationRules(L, totalNumOfRows, min_sup, min_conf):

    min_conf_percent = convertToPercentage(min_conf)

    # Open a file to write the output
    with open('output.txt', 'a') as file:
        file.write("==High-confidence association rules (min_conf={}%)\n".format(round(min_conf_percent,2)))

        # Create an empty dictionary to store the itemsets
        frequency_itemset = {}

        # Create an empty dictionary to store the association rules
        association_rules = {}

        # Combine the frequent itemsets into a single dictionary
        for itemset in L:
            for item in itemset:
                key = (item,) if not isinstance(item, tuple) else item
                frequency_itemset[key] = itemset[item]

        # Generate association rules from the frequent itemsets
        for itemset in frequency_itemset:
            if len(itemset) == 1:
                continue

            # Generate all possible LHS and RHS arguments
            for elem in itemset:
                RHS = (elem,)
                LHS = tuple([item for item in itemset if item not in RHS])
                LHS_RHS = itemset

                # Check if the LHS  and RHS are both frequent itemsets
                if LHS not in frequency_itemset or LHS_RHS not in frequency_itemset:
                    continue

                # Calculate the confidence and support of the association rule
                confidence_association_rule = frequency_itemset[LHS_RHS] / frequency_itemset[LHS]
                support_association_rule = frequency_itemset[LHS_RHS] / totalNumOfRows

                # Checks if the minimum support and confidence thresholds are reached
                metricsAreBigger = confidence_association_rule > float(min_conf) and  support_association_rule > float(min_sup) 

                # Add the association rule to the dictionary if thresholds are reached
                if metricsAreBigger :
                    print(list(LHS))
                    association_rule = "{LHS} => {RHS}".format(LHS = list(LHS), RHS=list(RHS))
                    metrics = (convertToPercentage(confidence_association_rule), convertToPercentage(support_association_rule))
                    association_rules[association_rule] = metrics

        # Sort the association rules by confidence
        sorted_association_rules = sorted(association_rules.items(), key = lambda x: x[1][0], reverse=True)

        # Write the association rules to the output file
        for rule in sorted_association_rules:
            file.write('{} (Conf: {}%, Supp: {} %)\n'.format(rule[0], rule[1][0], rule[1][1]))

