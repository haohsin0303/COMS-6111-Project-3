import sys
import pandas as pd
from collections import defaultdict

L_k_minus_1 = set()
K = 2

while (len(L_k_minus_1) != 0) :
    C_k = aprioriGen(L_k_minus_1, k)
    

# Global Variables
CSV_FILE_NAME = ""
MIN_SUP = 0
MIN_CONF = 0
TRANSACTIONS = []


def setupTransactions():

    global TRANSACTIONS

    df = pd.read_csv(CSV_FILE_NAME)
    for index, row in df.iterrows():
        market_basket = ' '.join(row)
        itemset = market_basket.split(",")
        TRANSACTIONS.append(itemset)
        # transaction = [column for column, value in row.iteritems() if value]
        # TRANSACTIONS.add(transaction)
        # print(row['PRODUCT_TYPE'], row['METAL'])
    print(TRANSACTIONS[:10])


def apriori():
    L1 = generateLargeOneItemSet()
    L = [0]
    L.append(L1) # L1
    k = 2
    c = defaultdict(int)
    while (len(L[k-1]) != 0):
        C_k = aprioriGen(L[k-1], k) # generate new candidates
        for t in TRANSACTIONS:
            C_t = subset(C_k, t)
            for c_item in C_t:
                c[(c_item)] += 1

        L.append({c for c in C_k if C_k[c] >= MIN_SUP}) # Lk
        k += 1
    
    result_set = set().union(*L[1:])   
    frequentItemsets(result_set)
    highConfidenceAssociationRules(result_set)     


def generateLargeOneItemSet(transactions):
    large_one_item_set = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            large_one_item_set[(item)] += 1
    return large_one_item_set


# Generates candidates
def aprioriGen(L_k_minus_1, k):
    candidates = set()

    # Join: join large itemsets having k-1 items
    for item1 in L_k_minus_1:
        for item2 in L_k_minus_1:
            candidate = item1.union(item2)
            if len(candidate) == k:
                candidates.add(candidate)
    
    # Prune: remove from C_k all itemsets whose (k- 1)-subsets are not in Lk-1
    for candidate in candidates:
        k_minus_1_subsets = generateSubsets(candidate)
        remove = False
        for sub in k_minus_1_subsets:
            if sub not in L_k_minus_1:
                remove = True
                break
        if remove:
            candidates.discard(candidate)
    
    return candidates


def generateSubsets(s):
    k_minus_1_subsets = []
    for item in s:
        sub = s - {item}
        k_minus_1_subsets.append(sub)
    return sub


def subset(C_k, t):
    return [itemset for itemset in C_k if set(t) >= set(itemset)]


def frequentItemsets(result_set):
    min_sup_percentage = MIN_SUP * 100
    output_lines = ["==Frequent itemsets (min_sup={percentage})\n".format(percentage=round(min_sup_percentage, 2))]
    output_lines += ["{result}, {percentage}%".format(result=list(result), percentage=result_set[result]*100) for result in result_set]

    with open("output.txt", "w") as file:
        file.write("\n".join(output_lines))


def highConfidenceAssociationRules(result_set):

    # Generate confidence association rules
    confidenceAssociationRules = defaultdict(float)
    for result in result_set:
        for item in result:
            left = result - {item}
            conf = result_set[left] / result_set[item]
            confidenceAssociationRules[(left, item)] = [conf, result_set[result]]
    
    # Sort the rules by the decreasing order of their confidence
    confidenceAssociationRules = dict(sorted(confidenceAssociationRules.items(), key=lambda item: item[1][0]))

    # Write
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


if __name__ == "__main__":
    main()
