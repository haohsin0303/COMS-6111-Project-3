import apriori
import csv
import sys
from collections import defaultdict


# Global Variables
CSV_FILE_NAME = ""
MIN_SUP = 0
MIN_CONF = 0
TRANSACTIONS = []
L1 = defaultdict(int)


# Define a dictionary to map concentration units to conversion factors
conversion_factors = {
    'ppm': 1,
    'mg/cm^2': 10000,
    'mg/l': 1,
    # add more units and conversion factors as needed
}
        

def generate_transactions():
    """
    Opens and iterates through the CSV file to generate the transactions
    that will be used for apriori

    We do preprocessing steps like removing unnecessary information,
    replacing rows with values where metal concentration is not found
    """
    
    global L1, TRANSACTIONS
    try:
        with open(CSV_FILE_NAME, 'r') as file:
            reader = csv.reader(file)
            next(reader) # Skips first header line

            # Iterate through rows
            for row in reader:
                itemset = row[1:-4]

                if (len(itemset) > 5):
                    itemset = itemset[:5]
                if (itemset[-2] == '-1'):
                    itemset[-2] = '0'
                                
                itemset[-2] = conversion_factors[itemset[-1].lower()] * float(itemset[-2])
                if (itemset[-2] == 0.0):
                    itemset[-2] = ("No Metal Detected")
                    del itemset[2]
                else:
                    del itemset[-2]

                itemset.append(row[7]) # include MADE_IN_COUNTRY column
                del itemset[-2] # remove UNITS colum
                TRANSACTIONS.append(itemset)

    except FileNotFoundError:
        print("Error opening CSV file:", CSV_FILE_NAME)


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
    apriori.runApriori(TRANSACTIONS, MIN_SUP, MIN_CONF)


if __name__ == '__main__':
    main()    
