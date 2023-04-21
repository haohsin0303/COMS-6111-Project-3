import json
import sys
import math
import csv
import apriori
import time


L1 = {}

# Global Variables
CSV_FILE_NAME = ""
MIN_SUP = 0
MIN_CONF = 0
TRANSACTIONS = []

def generate_transactions():
    global L1, TRANSACTIONS
    try:
            with open(CSV_FILE_NAME, 'r') as csvfile:
                reader = csv.reader(csvfile, delimiter=' ',
                                    quotechar='|')
                next(reader)
                for row in reader:
                    market_basket = ' '.join(row)
                    itemset = market_basket.split(',')
                    itemset = itemset[1:-2]
                    # count = 1

                # remove first element of itemset ('year'=> ignore value)

                    itemset.pop(0)

                # remove 'percent' and 'count' from itemset, count appended later

                    itemset.pop()
                    itemset.pop()

                    # itemset.append(count)

                    TRANSACTIONS.append(itemset)

                # calculate support
                    for item in itemset[:-1]:
                        if item not in L1:
                            L1[item] =1
                        else:
                            L1[item] += 1

            csvfile.close()
    except:
        print("Cannot open CSV file: ", CSV_FILE_NAME)

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


    generate_transactions()
    apriori.apriori(MIN_SUP, MIN_CONF, L1, TRANSACTIONS, len(TRANSACTIONS))

if __name__ == '__main__':
    main()    

