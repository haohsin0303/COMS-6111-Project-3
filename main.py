import sys
import pandas as pd
from collections import defaultdict



L_k_minus_1 = set()
K = 2

while (len(L_k_minus_1) != 0) :
    C_k = aprioriGen(L_k_minus_1)
    

# Global Variables
CSV_FILE_NAME = ""
MIN_SUP = 0
MIN_CONF = 0
TRANSACTIONS = set()


def setupTransactions():

    global TRANSACTIONS

    df = pd.read_csv(CSV_FILE_NAME)
    # result = df.head(10)
    # print(result)
    for index, row in df.iterrows():
        transaction = [column for column, value in row.iteritems() if value]
        TRANSACTIONS.add(transaction)
        # print(row['PRODUCT_TYPE'], row['METAL'])
    print(TRANSACTIONS)


def apriori():
    L = [0]
    L.append(generateLargeOneItemSet()) # L1
    k = 2
    L_k_minus_1 = L[1]
    while (len(L[k-1]) != 0):
        C_k = aprioriGen(TRANSACTIONS, k, L[k-1])
        for t in TRANSACTIONS:
            for c in C_k:
                pass # TODO
        L.append({c for c in C_k if c.count >= MIN_SUP}) # Lk

        k += 1
    
    result_set = set().union(*L[1:])        


def generateLargeOneItemSet(transactions):
    large_one_item_set = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            large_one_item_set[(item)] += 1
    return large_one_item_set


def aprioriGen(transactions, k, L_k_minus_1):
    new_item_set = defaultdict(int)
    candidates = set()
    
    # Join: join large itemsets having k-1 items
    for item1 in L_k_minus_1:
        for item2 in L_k_minus_1:
            candidate = item1.union(item2)
            if len(candidate) == k:
                candidates.add(candidate)
    
    # Prune: delete from Ck all itemsets whose (k- 1)-subsets are not in Lk-1
    for candidate in candidates:
        for transaction in transactions:
            if candidate.issubset(transaction):
                new_item_set[candidate] += 1
    
    return new_item_set


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
