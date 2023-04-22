from collections import defaultdict

def runApriori(D, min_sup, min_conf):
    """
    Runs the Apriori Algorithm as defined in Section 2.1 in 
    Fast Algorithms for Mining Association Rules:
    Resource Link: http://www.cs.columbia.edu/~gravano/Qual/Papers/agrawal94.pdf 
    """
    L1 = getLargeOneItemsets(D, min_sup)
    L = [L1]
    k = 1 # Starts at 1 because we L1 to the L list

    while (len(L[k-1]) != 0):
        Ck = aprioriGen(L[k-1], k) # New candidates
        c = defaultdict(int)

        for t in D:
            Ct = subset(Ck, t) # Candidates contained in t
            for candidate in Ct:
                candidateTuple = tuple(candidate)
                c[candidateTuple] += 1 # c.count++

        Lk = filterItemsets(D, c, min_sup)
        L.append(Lk)
        k += 1

    writeFrequentItemsets(D, L, min_sup)
    writeAssociationRules(D, L, min_sup, min_conf)


def filterItemsets(D, c, min_sup):
    """
    Filters the candidates whose count is greater than minsup
    Lk = {c ∈ Ck | c.count >= minsup} 
    """
    return {item: candidate_count for item, candidate_count in c.items() if (candidate_count / len(D)) >= min_sup}


def getLargeOneItemsets(D, min_sup):
    """
    Generates the large 1-itemsets at the start of apriori
    """
    L1 = defaultdict(int)
    for transaction in D:
        for item in transaction:
            L1[item] += 1

    # Return dictionary with items that are greater than minsup
    return filterItemsets(D, L1, min_sup)


def aprioriGen(Lk_1, k):
    """
    Generates new candidates Ck
    """
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
    return [itemset for itemset in Ck if set(itemset).issubset(set(t))]


def convertToPercentage(num):
    """
    Helper function to convert min_sup or min_conf to percentages
    Used for file writing
    """
    return float(num) * 100


def writeFrequentItemsets(D, L, min_sup):
    with open('output.txt', 'w') as file:
        file.write("==Frequent itemsets (min_sup={min_sup_percent}%)\n".format(min_sup_percent = round(convertToPercentage(min_sup), 2)))
        
        frequency_itemset = {item: itemset[item] for itemset in L for item in itemset}
        sorted_frequency_itemset = sorted(frequency_itemset.items(), key=lambda x: x[1], reverse=True)

        for item, count in sorted_frequency_itemset:
            if (isinstance(item, tuple)):
                item = "[" + ", ".join(list(item)) + "]"
            else:
                item = "[" + item + "]"
            file.write("{item}, {support}%\n".format(item=item, support = round(convertToPercentage(count/len(D)), 2)))


def writeAssociationRules(D, L, min_sup, min_conf):

    min_conf_percent = convertToPercentage(min_conf)

    # Open a file to write the output
    with open('output.txt', 'a') as file:
        file.write("==High-confidence association rules (min_conf={}%)\n".format(round(min_conf_percent, 2)))

        # Create an empty dictionary to store the itemsets
        frequency_itemset = {}

        # Create an empty dictionary to store the association rules
        association_rules = {}

        # Combine the frequent itemsets into a single dictionary
        for itemset in L:
            for item in itemset:
                if isinstance(item, tuple):
                    key = item
                else:
                    key = (item, )
                frequency_itemset[key] = itemset[item]

        # Generate association rules from the frequent itemsets
        for itemset in frequency_itemset:
            if len(itemset) == 1:
                continue

            # Generate all possible LHS and RHS arguments
            for elem in itemset:
                RHS = (elem, )
                LHS = tuple([item for item in itemset if item not in RHS])
                LHS_RHS = itemset

                # Check if the LHS  and RHS are both frequent itemsets
                if LHS not in frequency_itemset or LHS_RHS not in frequency_itemset:
                    continue

                # Calculate the confidence and support of the association rule
                confidence_association_rule = frequency_itemset[LHS_RHS] / frequency_itemset[LHS]
                support_association_rule = frequency_itemset[LHS_RHS] / len(D)

                # Checks if the minimum support and confidence metric thresholds are reached
                metricsAreBigger = confidence_association_rule > float(min_conf) and  support_association_rule > float(min_sup) 

                # Add the association rule to the dictionary if metric thresholds are reached
                if metricsAreBigger :
                    LHS_str = "[" + ", ".join(list(LHS)) + "]"
                    RHS_str = "[" + ", ".join(list(RHS)) + "]"
                    association_rule = "{LHS} => {RHS}".format(LHS=LHS_str, RHS=RHS_str)
                    metrics = (convertToPercentage(confidence_association_rule), convertToPercentage(support_association_rule))
                    association_rules[association_rule] = metrics

        # Sort the association rules by confidence
        sorted_association_rules = sorted(association_rules.items(), key = lambda x: x[1][0], reverse=True)

        # Write the association rules to the output file
        for rule in sorted_association_rules:
            conf = rule[1][0]
            support = rule[1][1]
            file.write('{} (Conf: {}%, Supp: {} %)\n'.format(rule[0], conf, support))
