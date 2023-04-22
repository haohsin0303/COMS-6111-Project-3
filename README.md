# COMS-6111-Project-3

In this project, we use a-priori algorithm to extract association rules from the data set we chose from the NYC Open Data Site: https://opendata.cityofnewyork.us/.

## Team Members
- Christopher Asfour: cra2139
- Nina Hsu: hh2961

## Relevant Files
- main.py
- apriori.py
- README.md
- example-run.txt
- INTEGRATED-DATASET.csv

## How to run
1. Run the program in the project repository using the following command:
```
python3 main.py <csv_file_name> <min_sup> <min_conf>
```

- csv_file_name: the name of a file from which to extract association rules
- min_sup=[0,1]: the support threshold of the itemsets
- min_conf=[0,1]: the confidence threshold of the association rules

## Description
### Data set
Data set URL: https://data.cityofnewyork.us/Health/Metal-Content-of-Consumer-Products-Tested-by-the-N/da9u-wz3r

The data set we chose is "Metal Content of Consumer Products Tested by the NYC Health Department". This data set provides the laboratory test results of consumer products. The data includes 5,114 rows and 10 columns.

### Mapping
We only ommited the first column and the last two columns in the `generate_transactions` function in `main.py`. These columns are ROW_ID, COLLECTION_DATE, and DELETED, which we believe have no association with the other columns.

### Why we choose this data set?
This data set contains the laboratory test results of the metal in consumer products. We want to know if there is any association between PRODUCT_TYPE, METAL, MANUFACTURER, and MADE_IN_COUNTRY.

## Project Design
In this project, we implemented the a-priori algorithm described in Section 2.1 of the Agrawal and Srikant paper: Fast Algorithms for Mining Association Rules. We decided to implement the original a-priori algorithm because the memory is enough for our data set.
