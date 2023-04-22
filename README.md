# COMS-6111-Project-3

In this project, we use a-priori algorithm to extract association rules from the data set we chose from the NYC Open Data Site.

## Team Members
- Christopher Asfour: cra2139
- Nina Hsu: hh2961

## Relevant Files
- `main.py`: This file is used to run the whole program. It performs all validation checks when user enters the program parameters, organizes the csv file, and runs the a-priori algorithm.
- `apriori.py`: This file is where we implement the a-priori algorithm described in Section 2.1 of the Agrawal and Srikant paper: Fast Algorithms for Mining Association Rules. It also output a txt file which included the item sets with supports of at least MIN_SUP, and the association rules with confidents of at least MIN_CONF.
- `README.md`: The README file.
- `example-run.txt`: This file is an example output of our project.
- `INTEGRATED-DATASET.csv`: This file is downloaded from NYC Open Data Site without any modification. You can find the detail description of the data set below.

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
The data set we chose is "Metal Content of Consumer Products Tested by the NYC Health Department". This data set provides the laboratory test results of consumer products. The data set includes 5,114 rows and 10 columns.

The fields included in the dataset are:
- PRODUCT_TYPE: (Type of consumer product tested)
- PRODUCT_NAME: (Name of product as it appears on product label or as reported to staff during investigation)
- METAL: (Name of metal for which product was tested)
- CONCENTRATION: (The amount of metal found in the sample of product tested. Sample with a metal concentration below the laboratory reporting limit is marked “-1”, meaning “Not Detected”)
- UNITS (Unit of measurement)
- MANUFACTURER: (The name of the manufacturer as it appears on product label or as reported to staff during investigation.)
- MADE_IN_COUNTRY: (Name of country where the product was made as it appears on product label or as reported to staff during investigation)
- COLLECTION_DATE: (Date the product sample was collected)
- DELETED: (Column on whether row is deleted)

### Pre-processing & Mapping
For our integrated dataset, we omitted several columns in the `generate_transactions()` function in `main.py` in order to generate interesting high-confidence association rules. The columns ommitted were ROW_ID, COLLECTION_DATE, UNITS, and DELETED, which we believe have no interesting with the other columns.

The ROW_ID and DELETED columns are information relevant to the CSV file. ROW_ID column is a unique identifier for each row in a dataset, and the DELETED column is a binary column that indicates whether a row has been deleted or not. 

The COLLECITON_DATE only provides information as to when the product was tested for metals. If the dataset is taken over a long period of time, the collection date may not be consistent and might not provide valuable, insighting information. Therefore, we drop this column to focus on more important information. 

Since metals have different units of measurements for each metal tested, we decided it was best to simply convert all the concentrations into ppm (parts per million) units and drop the UNITS column. This way, we no longer have to account for different units as we are iterating through the rows in the dataset. 

There was no mapping performed on the dataset. The dataset was used as provided in the original link.

### Why we choose this data set?
This data set contains the laboratory test results of the metal in consumer products. We want to know if there is any association between PRODUCT_TYPE, METAL, MANUFACTURER, and MADE_IN_COUNTRY. By analyzing this dataset, we can identify patterns in metal content that could be indicative of potential health hazards or violations. The large sample size of approximately 5,000 products is a great choice for conducting analysis and building igh confidence association rules. In short, this dataset can provide valuable insights into consumer product safety and can help customers make a holistic decision on what products they should purchase. 

## Project Design
In this project, we implemented the a-priori algorithm described in Section 2.1 of the Agrawal and Srikant paper: Fast Algorithms for Mining Association Rules. We decided to implement the original a-priori algorithm because the memory is enough for our data set.

Our program intiially starts at `main.py`, where we check the terminal arguments to ensure that a valid `INTEGRATED-DATASET.csv` file exists, and minimum support and confidence arguments are valid. Once all arguments are validated, we generate our transactions that will be used in `apriori.py` by calling `generate_transactions()`. See Pre-processing & Mapping section for more information on what dataset columns are discarded and manipulated. 

After the transactions have been all added with the formatted itemsets, we now call the `runApriori()` function in `apriori.py` 
to start running the a-priori algorithm. 

When we start running `runApriori()`, we immediately generate the set of large 1-itemsets by calling `getLargeOneItemsets()`. As Section 2.1 states, we need to generate the itemsets with those that have the minimum support, so we filter the dictionary with
itemsets that satisfy the minimum support. After the set is generated, we append it to the list of sets with increasing k, which wil be used in the iteration. 
The function then iteratively generates larger itemsets by first generating candidate itemsets using `aprioriGen()`, and then filtering them using `filterItemsets()`, which discards those that do not meet the `min_sup` threshold. The algorithm continues looping until no more frequent itemsets can be found, and it writes the frequent itemsets and high-confidence association rules to an output file using `writeFrequentItemsets()` and `writeHighConfidenceAssociationRules()`. The description on their implementation are described below.

### aprioriGen()
The aprioriGen function generates new candidate itemsets Ck by joining the previous frequent itemsets Lk_1 (size k-1). 

It extracts the list of itemsets from the previous frequent itemsets Lk_1.
It loops through each itemset in the list and compares it to every other itemset after it in the list to check for common items.
If the candidate is not already in Ck, it is added to the list of candidate itemsets, but if the common items count is k-1, it creates a new candidate itemset candidate by taking the union of the two itemsets.
Once all itemsets in Lk_1 have been compared with one another, the list of candidate itemsets Ck is returned

### filterItemsets()
The function takes a dictionary of candidate itemsets c and returns only those itemsets whose count is greater than or equal to min_sup, or the minimum support.

### writeFrequentItemsets()
The function writes the frequent itemsets to the output file. It first generates a dictionary that combines all the frequent itemsets from each iteration of the algorithm and is sorted in descending order by frequency. We write each itemset and its support as a percentage to the output file.

### writeHighConfidenceAssociationRules()
The function then creates an empty dictionary called frequency_itemset and an empty list called association_rules. The dictionary will store the frequency of each frequent itemset, while the list will store the generated association rules. As a design choice, we decided to create a `namedtuple` field called Rule that will store the left-hand-side and right-hand-side of the association rule, as well as the confidence and support for each rule. This way, all relevant data does not need to be parsed as we add the 
rule to the list of generated association rules. 

We start by combining all frequent itemsets into a singular dictionary. Each itemset in L (i.e. the list of large k-itemsets) is checked for each of its items, and a key is created in the frequency_itemset dictionary with the item as the key and the frequency of the itemset as the value.

We then generate association rules from the frequent itemsets in the frequency_itemset dictionary. For each itemset, it generates all possible LHS (left-hand side) and RHS (right-hand side) arguments, and checks if they are both frequent itemsets. We also perform a check to make sure that at least >=1 LHS argument and exists,  exactly 1 RHS argument exists, and that the RHS argument is not in the LHS argument. 

Finally, we call `createAssociationRule()` to generate the rules that will be appended to the list of generated association rules. 
The function then sorts the association rules by confidence in decreasing order (i.e. highest to lowest) and writes them to the output file.


### createAssociationRule()
The function calculates the confidence and support of the association rule, and checks if the minimum support and confidence metric thresholds are reached. If they are, it creates a Rule object and returns it. If not, it returns None and is not appended to the list of association rules. 

## Compelling Results
When running the following command:
python3 main.py INTEGRATED-DATASET.csv 0.01 0.75

we get interesting results. For example, a rule that was generated was:
`[Arsenic] => [Dietary Supplement/Medications/Remedy] (Conf: 97.14285714285714%, Supp: 1.994524833789597 %)`

The association rule states that if Arsenic is detected, it is likely that the product type was Dietary Supplements/Medications/Remedies with a high confidence of 97.14%. The support value of 1.99% indicates that the itemset (Arsenic and Dietary Supplements/Medications/Remedies) appeared in 1.99% of all transactions. Although the support is not high, it matches with real-world scientific studies from the CDC that dietary supplements can contain dangerous amounts of arsenic. [1] 

Another rule that was generated was :
`[Lead, MADE IN BANGLADESH] => [Food-Spice] (Conf: 95.55555555555556%, Supp: 5.0449745795854515 %)`
The association rule states that if Lead is detected and it was made in Bangladesh, it is likely that the product type was Food-Spice with a high confidence of 95.55%. The support value of 5.04% indicates that the itemset (Food-Spice) appeared in 5.04% of all transactions. Although the support is not high, it also matches with real-world data showing that Lead is commonly food in food spices from Bangladesh, because the country utilizes bright yellow curry led turmeric processors to add lead chromate into the spice [2].

The last interesting rule that was generated was:
`[Tableware/Pottery] => [Lead] (Conf: 86.3013698630137%, Supp: 4.9276495893625345 %)`
The association rule states that if we have Tableware/Pottery, it is likely that there is Lead with a high confidence of 86.3%. The support value of 4.927% indicates that the itemset (Food-Spice) appeared in 5.04% of all transactions. Although the support is not high, it also matches with real-world data, since Lead has long been used in ceramicware, both in tableware and in decorations [3]. 

## References
- [NYC Open Data - Metal Content of Consumer Products Tested by the NYC Health Department](https://data.cityofnewyork.us/Health/Metal-Content-of-Consumer-Products-Tested-by-the-N/da9u-wz3r)
- Rakesh Agrawal and Ramakrishnan Srikant: Fast Algorithms for Mining Association Rules in Large Databases, VLDB 1994
[1] https://www.cdc.gov/eis/conference/dpk/Arsenic-Toxicity.html#:~:text=Dietary%20mineral%20supplements%20are%20commonly,multiple%20supplements%20are%20taken%20together.
[2] https://woods.stanford.edu/news/lead-found-commonly-used-spice
[3] https://www.cdph.ca.gov/Programs/CCDPHP/DEODC/CLPPB/Pages/Q-A-Lead-in-Tableware.aspx#:~:text=Lead%20has%20long%20been%20used,from%20penetrating%20into%20the%20dish.
