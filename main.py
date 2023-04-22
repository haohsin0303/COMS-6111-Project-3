import apriori
import csv
import sys

# Global variables
CSV_FILE_NAME = ""
MIN_SUP = 0
MIN_CONF = 0
TRANSACTIONS = []

conversion_factors = {
    'ppm': 1,
    'mg/cm^2': 10000,
    'mg/l': 1,
}

def generate_transactions():
    global TRANSACTIONS
    try:
        with open(CSV_FILE_NAME, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)

            for row in csv_reader:
                itemset = row[1:-4][:5]
                if itemset[-2] == '-1':
                    itemset[-2] = '0'
                itemset[-2] = conversion_factors[itemset[-1].lower()] * float(itemset[-2])
                if itemset[-2] == 0.0:
                    itemset[-2] = "No Metal Detected"
                    del itemset[2]
                else:
                    del itemset[-2]
                
                if (row[7].upper() == "UNKNOWN OR NOT STATED"):
                    row[7] = "COUNTRY NOT LISTED"
                else:
                    row[7] = "MADE IN " + row[7]
                itemset.append(row[7])
                del itemset[-2]

                TRANSACTIONS.append(itemset)

    except FileNotFoundError:
        print("Error opening CSV file:", CSV_FILE_NAME)

def main():
    global CSV_FILE_NAME, MIN_SUP, MIN_CONF

    terminal_arguments = sys.argv[1:]
    if len(terminal_arguments) != 3:
        print("Format must be <csv_file_name> <min_sup> <min_conf>")
        return
    
    CSV_FILE_NAME = terminal_arguments[0]

    MIN_SUP = eval(terminal_arguments[1])
    if not (isinstance(MIN_SUP, (int, float)) and 0 <= MIN_SUP <= 1):
        print("MIN_SUP must be a real number between 0 and 1")
        return
    
    MIN_CONF = eval(terminal_arguments[2])
    if not (isinstance(MIN_CONF, (int, float)) and 0 <= MIN_CONF <= 1):
        print("MIN_CONF must be a real number between 0 and 1")
        return

    generate_transactions()
    apriori.runApriori(TRANSACTIONS, MIN_SUP, MIN_CONF)

if __name__ == '__main__':
    main()
