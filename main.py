import sys
import pandas as pd
from collections import defaultdict
from itertools import combinations

L_k_minus_1 = set()
K = 2

# while (len(L_k_minus_1) != 0) :
#     C_k = aprioriGen(L_k_minus_1, k)
    

# Global Variables
CSV_FILE_NAME = ""
MIN_SUP = 0
MIN_CONF = 0
TRANSACTIONS = []


def setupTransactions():

    global TRANSACTIONS

    df = pd.read_csv(CSV_FILE_NAME)
    for index, row in df.iterrows():
        itemset = [item for item in row][1:-2]
        TRANSACTIONS.append(itemset)
        # transaction = [column for column, value in row.iteritems() if value]
        # TRANSACTIONS.add(transaction)
        # print(row['PRODUCT_TYPE'], row['METAL'])
    for idx, row in enumerate(TRANSACTIONS):
        if idx < 10:
            print(row)
    # print(TRANSACTIONS[:10])


def apriori():
    L1 = generateLargeOneItemSet() # L1 = {large 1-itemsets};
    L = [0, L1]
    k = 2
    c = defaultdict(int)
    while (len(L[k-1]) != 0):
        print("L[k-1]", L[k-1])
        C_k = aprioriGen(L[k-1], k) # generate new candidates.
        print("C_k: ", C_k)
        for t in TRANSACTIONS:
            C_t = subset(C_k, t) # Candidates contained in t
            for c_item in C_t:
                if (c_item) not in c:
                    c[(c_item)] = 1
                else:
                    c[(c_item)] += 1
            

        Lk = {",".candidate: c[candidate] for candidate in C_k if c[candidate]/len(TRANSACTIONS) >= MIN_SUP} #Lk
        L.append(Lk)
        k += 1
    
    # result_set = set().union(*L[1:])
    result_set = dict()
    for Lk in L[1:]:
        result_set.update(Lk)
    print("")
    print("result_set", result_set)
    frequentItemsets(result_set)
    highConfidenceAssociationRules(result_set)     


def generateLargeOneItemSet():
    large_one_item_set = defaultdict(int)
    for transaction in TRANSACTIONS:
        for item in transaction:
            large_one_item_set[str(item)] += 1
    for idx, x in enumerate(large_one_item_set):
        if idx < 10:
            print(x, large_one_item_set[x])
    # print("'Dietary Supplement/Medications/Remedy'", large_one_item_set['Dietary Supplement/Medications/Remedy'])
    return large_one_item_set


# Generates candidates
def aprioriGen(L_k_minus_1, k):
    print("aprioriGen:", k)
    C_k = set()
    print("start joining")
    # Join: join large itemsets having k-1 items
    for item1 in L_k_minus_1:
        for item2 in L_k_minus_1:
            set1 = set(str(item1).split(","))
            set2 = set(str(item2).split(","))
            candidate = set1.union(set2)
            if len(candidate) == k-1:
                C_k.add(",".join(candidate))

    print("start pruning")
    # Prune: remove from C_k all itemsets whose (k- 1)-subsets are not in Lk-1
    result_Ck = set()
    for c in C_k:
        candidate_set = set(c.split(",")) 
        k_minus_1_subsets = generateSubsets(candidate_set) #(k-1) s
        remove = False
        for subset in k_minus_1_subsets:
            if subset not in L_k_minus_1:
                remove = True
                break

        if not remove:
            result_Ck.add(c)
    
    # print("C_k after prune", result_Ck)
    # print("Equal", C_k == result_Ck)

    return result_Ck


def generateSubsets(s):
    k_minus_1_subsets = []
    for item in s:
        sub = s - {item}
        k_minus_1_subsets.append(sub)
    return sub


def subset(C_k, t):
    return [itemset for itemset in C_k if set(t) >= set(itemset)]


def frequentItemsets(result_set):

    # Output the frequent itemsets
    min_sup_percentage = MIN_SUP * 100
    output_lines = ["==Frequent itemsets (min_sup={percentage}%)".format(percentage=round(min_sup_percentage, 2))]
    output_lines += ["[{result}], {percentage}%".format(result=result, percentage=result_set[result]*100) for result in result_set]

    with open("output.txt", "w") as file:
        file.write("\n".join(output_lines))


def highConfidenceAssociationRules(result_set):

    # Generate confidence association rules
    confidenceAssociationRules = defaultdict(float)
    for result in result_set:
        result_s = set(result.split(","))
        if len(result_s) >= 2:
            for item in result_s:  
                left = ",".join(result_s - {item})
                print("left", left)
                print("item", item)
                conf = result_set[left] / result_set[item]
                confidenceAssociationRules[(left, item)] = [conf, result_set[result]]
    
    # Sort the rules by the decreasing order of their confidence
    confidenceAssociationRules = dict(sorted(confidenceAssociationRules.items(), key=lambda item: item[1][0]))

    # Output the high-confidence association rules
    min_conf_percentage = MIN_CONF * 100
    output_lines = ["==High-confidence association rules (min_conf={percentage}%)".format(percentage=min_conf_percentage)]    
    output_lines += ["{result} => {item} (Conf: {conf_percent}%, Supp: {sup_percent}%)".format(
        result=list(result),
        item=list(item),
        conf_percent=result_set[(result, item)][0]*100,
        sup_percent=result_set[(result, item)][1]*100
    ) for result, item in result_set]

    with open("output.txt", "w") as file:
        file.write("\n".join(output_lines))
    

def main():
    """
    Starting point of program that parses the terminal arguments
    and verifies that arguments are valid. 
    Once arguments are deemed valid, the querying function will be called
    """

    # Format Required: <csv_file_name> <min_sup> <min_conf>
    global CSV_FILE_NAME, MIN_SUP, MIN_CONF

    terminal_arguments = sys.argv[1:]
    # Return if the number of arguments provided is incorrect
    if (len(terminal_arguments) != 3):
        print("Format must be <csv_file_name> <min_sup> <min_conf>")
        return
    
    CSV_FILE_NAME = terminal_arguments[0]

    MIN_SUP = eval(terminal_arguments[1])
    if (not ((isinstance(MIN_SUP, int) or isinstance(MIN_SUP, float)) and 0 <= MIN_SUP <= 1)):
        print("MIN_SUP must be an real number between 0 and 1")
        return
    
    MIN_CONF = eval(terminal_arguments[2])
    if (not ((isinstance(MIN_CONF, int) or isinstance(MIN_CONF, float)) and 0 <= MIN_CONF <= 1)):
        print("MIN_CONF must be an real number between 0 and 1")
        return


    setupTransactions()
    # apriori()
    apriori2()


def apriori2():
    L1 = generateLargeOneItemSet()
    # for transaction in TRANSACTIONS:
    #     for item in transaction:
    #         if item not in L1:
    #             L1.append(str(item))

    print("L1: ", L1)

    L = [0, L1] # list of frequent itemsets
    k = 2

    while len(L[k-1]) > 0:
        Ck = aprioriGen2(L[k-1], k) # generate new candidate itemsets
        count = {}
        for transaction in TRANSACTIONS:
            candidates = [itemset for itemset in Ck if set(itemset).issubset(set(transaction))]
            for candidate in candidates:
                candidate_str = ",".join(candidate)
                if candidate_str not in count:
                    count[candidate_str] = 1
                else:
                    count[candidate_str] += 1
        Lk = {itemset: count[itemset] for itemset in count if count[itemset]/len(TRANSACTIONS) >= MIN_SUP}
        L.append(Lk)
        k += 1

    # Answer = set.union(*L[1:])
    Answer = dict()
    for lk in L[1:]:
        Answer.update(lk)

    frequentItemsets(Answer)
    highConfidenceAssociationRules(Answer)     


def aprioriGen2(Lk_minus_1, k):
    Ck = []
    print("Lk_minus_1", Lk_minus_1)
    for i, item1 in enumerate(Lk_minus_1.keys()):
        for j, item2 in enumerate(Lk_minus_1.keys()):
            if j <= i:
                continue
            # join step
            if k != 2:
                temp = [item for item in item1 if item in item2]
                joined_candidate = set(item1 + item2)
                if (len(temp) == k-1) and (joined_candidate not in Ck):
                    Ck.append(joined_candidate)
            else:
                joined_candidate = [item1] + [item2]
                Ck.append(joined_candidate)
            # print("Lk_minus_1[i]", Lk_minus_1[i], "Lk_minus_1[j]", Lk_minus_1[j])
            # l1 = list(Lk_minus_1[i])[:k-2]
            # # print("l1: ", l1)
            # l2 = list(Lk_minus_1[j])[:k-2]
            # # print("l2: ", l2)
            # if l1 == l2:
            #     # print("Lk_minus_1[i,j]", Lk_minus_1[i], Lk_minus_1[j])
            #     Ck.append(Lk_minus_1[i]+","+Lk_minus_1[j])
    # # prune step
    # for itemset in Ck:
    #     subsets = combinations(itemset, k-1)
    #     for subset in subsets:
    #         if frozenset(subset) not in Lk_minus_1:
    #             Ck.remove(itemset)
    #             break
    return Ck

if __name__ == "__main__":
    main()
