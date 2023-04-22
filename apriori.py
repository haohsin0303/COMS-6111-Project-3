from collections import defaultdict, namedtuple

Rule = namedtuple('Rule', ['LHS', 'RHS', 'Confidence', 'Support'])

def runApriori(D, min_sup, min_conf):
    """
    Runs the Apriori Algorithm as defined in Section 2.1 in 
    Fast Algorithms for Mining Association Rules:
    Resource Link: http://www.cs.columbia.edu/~gravano/Qual/Papers/agrawal94.pdf 
    """
    L1 = getLargeOneItemsets(D, min_sup)
    L = [L1]
    k = 1 # Starts at 1 because we add L1 to the L list

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
    writeHighConfidenceAssociationRules(D, L, min_sup, min_conf)


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
    for index, itemset_1 in enumerate(itemsets):
        for itemset_2 in itemsets[index+1:]:
            if k != 1:
                common_items = set(itemset_1).intersection(set(itemset_2))
                candidate = set(itemset_1 + itemset_2)								 
                if (candidate not in Ck) and len(common_items) == (k-1):
                    Ck.append(candidate)
            else:
                Ck.append([itemset_1, itemset_2])

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
    """
    Handles writing the frequent itemsets to the file text
    """
    
    # Open a file to write to the output
    with open('example-run.txt', 'w') as file:
        file.write("==Frequent itemsets (min_sup={min_sup_percent}%)\n".format(min_sup_percent = round(convertToPercentage(min_sup), 2)))
        
        frequency_itemset = {item: itemset[item] for itemset in L for item in itemset}
        sorted_frequency_itemset = sorted(frequency_itemset.items(), key=lambda x: x[1], reverse=True)

        for item, count in sorted_frequency_itemset:
            if (isinstance(item, tuple)):
                item = "[" + ", ".join(list(item)) + "]"
            else:
                item = "[" + item + "]"
            file.write("{item}, {support}%\n".format(item=item, support = round(convertToPercentage(count/len(D)), 2)))
        file.write("\n")


def writeHighConfidenceAssociationRules(D, L, min_sup, min_conf):
    """
    Handles writing the high confidence association rules to the file text
    """

    min_conf_percent = convertToPercentage(min_conf)

    # Open the file once more to add to the output
    with open('example-run.txt', 'a') as file:
        file.write("==High-confidence association rules (min_conf={}%)\n".format(round(min_conf_percent, 2)))

        # Create an empty dictionary to store the itemsets
        frequency_itemset = {}

        # Create an empty list to store the association rules
        association_rules = []

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
                LHS_RHS = itemset # union
                RHS = (elem, )
                LHS = tuple([item for item in itemset if item not in RHS])

                # Check if the LHS and RHS are both frequent itemsets and build association rule
                if LHS in frequency_itemset and LHS_RHS in frequency_itemset:
                    rule = create_association_rule(D, LHS, RHS, LHS_RHS, frequency_itemset, min_sup, min_conf)
                    if rule:
                        association_rules.append(rule)

        # Sort the association rules by confidence
        sorted_association_rules = sorted(association_rules, key = lambda r: r.Confidence, reverse=True)

        # Write the association rules to the output file
        for rule in sorted_association_rules:
             file.write("{LHS} => {RHS} (Conf: {conf}%, Supp: {supp} %)\n".format(LHS=rule.LHS, RHS = rule.RHS, conf=rule.Confidence, supp=rule.Support))


def create_association_rule(D, LHS, RHS, LHS_RHS, frequency_itemset, min_sup, min_conf ):
    # Calculate the confidence and support of the association rule
    confidence_association_rule = frequency_itemset[LHS_RHS] / frequency_itemset[LHS]
    support_association_rule = frequency_itemset[LHS_RHS] / len(D)

    # Checks if the minimum support and confidence metric thresholds are reached
    metricsAreBigger = confidence_association_rule > float(min_conf) and  support_association_rule > float(min_sup) 

    # Add the association rule to the dictionary if metric thresholds are reached
    if metricsAreBigger :
        LHS_str = "[" + ", ".join(list(LHS)) + "]"
        RHS_str = "[" + ", ".join(list(RHS)) + "]"
        rule = Rule(LHS=LHS_str, RHS=RHS_str, Confidence=convertToPercentage(confidence_association_rule), Support=convertToPercentage(support_association_rule))
        return rule
    