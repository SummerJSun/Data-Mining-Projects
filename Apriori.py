#Collaboration statement: Resources used: course material;towardsdatascience.com;geeksforgeeks.org;stackoverflow.com;
#http://fimi.uantwerpen.be/src/apriori.c;My own code from CS334 course and my own previous project codes.    

def calculate_support(transactions, itemsets):
    count = {}
    for itemset in itemsets:
        count[itemset] = 0
        for transaction in transactions:
            if set(itemset).issubset(set(transaction)):
                count[itemset] += 1
    return count

def generate_candidates(frequent_itemsets,k):
    candidates = set()
    sorted_itemsets = sorted([tuple(sorted(itemset)) for itemset in frequent_itemsets])
    for i in range(len(sorted_itemsets)):
        for j in range(i+1, len(sorted_itemsets)):
            itemset1 = sorted_itemsets[i]
            itemset2 = sorted_itemsets[j]

            if itemset1[:k-2] == itemset2[:k-2]:
                new_candidate = itemset1[:k-2] + (itemset1[k-2],) + (itemset2[k-2],)
                candidates.add(new_candidate)
    return candidates

def Apriori(data, min_supp_count,output):
    result = []
    transactions = data["text_keywords"]
    transactions = transactions.str.split(';')
    transactions = transactions.apply(lambda x: [str(i) for i in x])
    k=1
    #Generating 1-itemsets
    itemsets = set()
    for transaction in transactions:
        for item in transaction:
            itemsets.add((item,))
    
    #Calculating support for 1-itemsets
    support_count = calculate_support(transactions, itemsets)
    frequent_itemsets = [itemset for itemset in itemsets if support_count[itemset] >= min_supp_count]
    result.extend([(itemset, support_count[itemset]) for itemset in frequent_itemsets])

    k=2
    #loop until no frequent itemsets are found
    while len(frequent_itemsets) > 0:
        #Generating candidates
        candidates = generate_candidates(frequent_itemsets, k)
        #Calculating support for candidates
        support_count = calculate_support(transactions, candidates)
        frequent_itemsets = [itemset for itemset in candidates if support_count[itemset] >= min_supp_count]
        k+=1
        result.extend([(itemset, support_count[itemset]) for itemset in frequent_itemsets])

    result.sort(key=lambda x: x[1], reverse=True)
    with open(output, 'w') as f:
        for itemset, count in result:
            items = ' '.join(sorted(itemset))
            f.write(f"{items} ({count})\n")
    
    return output


if __name__ == "__main__":
    import pandas as pd
    data = pd.read_csv("data.csv")
    Apriori(data, 500, "output.txt")