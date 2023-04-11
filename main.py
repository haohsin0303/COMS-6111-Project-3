import sys


# Global Variables
CSV_FILE_NAME = ""
MIN_SUP = 0
MIN_CONF = 0


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
    if (len(terminal_arguments) != 4):
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


if __name__ == "__main__":
    main()
