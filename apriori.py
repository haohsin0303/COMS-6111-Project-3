"""
1. Computing the support for each individual item
    Iterate through the dataset and count the number of occurrences of each item.
    This count is then divided by the total number of transactions to obtain the 
    support value for each item.

2. Deciding on the support threshold
    This is the minimum support value that an itemset must have to be considered
    "frequent." The support threshold is typically chosen based on domain knowledge
    and the desired level of pattern specificity.

3. Selecting the frequent items
    Using the support values calculated in step 1, select the individual items
    that meet the minimum support threshold.

4. Finding the support of the frequent itemsets
    Generate candidate itemsets by combining the frequent items from step 3. Then 
    count the number of transactions that contain each candidate itemset, and 
    calculate the support value for each candidate itemset.

5. Repeat for larger sets
    Steps 3 and 4 are repeated for larger itemsets until no more frequent itemsets
    can be found.

6. Generate Association Rules and compute confidence
    Once the frequent itemsets have been identified, we can generate association rules
    by selecting subsets of the frequent itemsets and calculating their confidence
    values. Confidence represents the conditional probability of a consequent item
    given an antecedent item.

7. Compute lift
    Lift is a measure of the strength of an association rule and represents the ratio
    of the observed support for the rule to the expected support if the items were
    independent. Lift values greater than 1 indicate a positive association between
    the antecedent and consequent items, while values less than 1 indicate a negative
    association.
"""

class Apriori:
    def __init__(self):
        pass
