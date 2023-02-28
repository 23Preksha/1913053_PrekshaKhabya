# -*- coding: utf-8 -*-
"""
# READING DATASET
"""

import pandas as pd

from google.colab import drive 
drive.mount('/content/drive')

#reading dataset from url
dataset = pd.read_csv('/content/drive/MyDrive/dataset_apriori.csv')

dataset

"""# SPLITTING DATASET"""

#splitting tid and items columns of df into two different dataframe
df_items = dataset['items']
df_tid = dataset['tid']

df_items

df_tid

"""# Convert Items to Number"""

#assigning unique index for different unique items
dictionaries = {'Handphone': 1, 'Laptop': 2, 'Charger': 3, 'Powerbank': 4, 'Tablet': 5 }

comma_splitted_df = df_items.apply(lambda x: x.split(','))

comma_splitted_df

numbered_col = []
for i in range(len(comma_splitted_df)):
    list_numbered = list(map(lambda x: dictionaries[x], comma_splitted_df[i]))
    sort_numbered = sorted(list_numbered)
    numbered_col.append(sort_numbered)

numbered_col

"""# Create Dataframe from Numbered Items"""

#creating dataframe of numbered_col
dict_data = {'items': numbered_col}
df = pd.DataFrame.from_dict(dict_data)

df

pd.concat([df_tid, df], axis=1)

items = []
for i in range(len(df)):
    for j in range(len(df['items'][i])):
        items.append(df['items'][i][j])
items

"""# Creating First Candidate (C1)"""

#Get unique element from list/array
unique_item = set(items)
unique_item

#Convert it to list
list_unique_item = list(unique_item)
list_unique_item

#counting frequency of every unique items
count_unique = []
for value in (list_unique_item):
    count_unique.append((value, items.count(value)))
count_unique

candidate1_df = pd.DataFrame(count_unique, columns=["itemset", "sup"])

candidate1_df

"""# Creating first Frequent Itemset (L1)"""

#filtering items having minimum support count 6
def filter_sup(candidate):
    minimum_sup = 6
    filtering = candidate['sup'] > minimum_sup
    freq = candidate[filtering]
    return freq

freq_itemset1 = filter_sup(candidate1_df)

freq_itemset1

"""# Create the Second Candidate (C2)

**SELF JOIN**
"""

import numpy
def self_join(prev_freq_itemset):
    self_join_candidate = []
    for i in range(len(prev_freq_itemset['itemset'])):
        for j in range((i+1), len(prev_freq_itemset['itemset'])):
            itemset_i = prev_freq_itemset['itemset'][i]
            itemset_j = prev_freq_itemset['itemset'][j]
            if(type(itemset_i) == numpy.int64 and type(itemset_j) == numpy.int64):
                itemset_i = {itemset_i}
                itemset_j = {itemset_j}
            union_candidate = itemset_i.union(itemset_j)

            if union_candidate not in self_join_candidate:
                self_join_candidate.append(union_candidate)
    return self_join_candidate

candidate2_list = self_join(freq_itemset1)

candidate2_list

count_candidate2 = []

#Set the Initial value of Second Count Candidate (C2)
for i in range(len(candidate2_list)):
    count_candidate2.append((candidate2_list[i], 0))

count_candidate2

initial_df_candidate = pd.DataFrame(count_candidate2, columns=['itemset', 'sup'])

initial_df_candidate

df

#Let's add it with 1 whenever we found every candidate is a subset from Database D


def count_support(database_dataframe, prev_candidate_list):
    #initial_df_candidate['sup'] = 0 #set All value into 0 only for initial value for consistency value when running this cell everytime.
    count_prev_candidate = []

    #Set the Initial value of Previous Candidate
    for i in range(len(prev_candidate_list)):
        count_prev_candidate.append((prev_candidate_list[i], 0))
    
    df_candidate = pd.DataFrame(count_prev_candidate, columns=['itemset', 'sup'])
    print('Database D dataframe\n', database_dataframe)
    print('(Initial) Dataframe from Candidate with All zeros sup\n', df_candidate)
    
    for i in range(len(database_dataframe)):
        for j in range(len(count_prev_candidate)):
            #using issubset() function to check whether every itemset is a subset of Database or not
            if (df_candidate['itemset'][j]).issubset(set(database_dataframe['items'][i])): 
                df_candidate.loc[j, 'sup'] += 1
            
    return df_candidate

count_candidate2_df = count_support(df, candidate2_list)

count_candidate2_df

"""# Creating Second Frequent Itemset (L2)"""

#Filter the itemset based on minimum support (occurences of items)
freq_itemset2 = filter_sup(count_candidate2_df)

freq_itemset2

freq_itemset2_reset = freq_itemset2.reset_index(drop=True)

#We need to reset the index, because need to access the index later.
freq_itemset2_reset

"""# Creating the Third Candidate (C3) - Using the Candidate Forming Technique

**SELF JOIN**
"""

print(freq_itemset2_reset)
self_join_result = self_join(freq_itemset2_reset)
print('self join result')
print(self_join_result)

"""**PRUNING**"""

def get_subset(candidate):
    temp = []
    final = []
    for i in range(len(candidate)):
        for j in range(len(candidate)):
            if i != j:
                temp.append(candidate[j])
        temp_set = set(temp)
        final.append(temp_set)
        temp.clear()
    print('Subset from {} : {}'.format(candidate, final))
    return final

def pruning(candidate_set, prev_freq_itemset):
    print('Candidate set', candidate_set)
    temp = []
    
    for idx, value in enumerate(candidate_set):
        list_candidate = list(value)
        temp_candidate = (get_subset(list_candidate))
        
        for temp_item in temp_candidate:
            print('Temp item', temp_item)
            check = temp_item == prev_freq_itemset['itemset']
            print('\nCheck candidate from Previous Frequent Itemset\n', check)
            
            if any(check) == False:
                print(any(check))
                print('Val', value)
            else:
                print('\nAll of {} subset contained in \n{}'.format(candidate_set, prev_freq_itemset))
                if value not in temp:
                    temp.append(value)
                
    return temp

freq_itemset2_reset

subset = [{2, 3}, {1, 3}, {1, 2}]

self_join_result

for i in range(len(self_join_result)):
    get_subset(list(self_join_result[i]))

freq_itemset2_reset

for item in subset:
    print(item)
    check = item == freq_itemset2_reset['itemset']
    print('Check', any(check))

self_join_result

candidate3_list = pruning(self_join_result, freq_itemset2_reset)

candidate3_list

"""# Creating the Third Frequent Itemset (L3)"""



#Let's see the database again
df

#Then check the newest candidate value
candidate3_list

count_candidate3_df = count_support(df, candidate3_list)

count_candidate3_df

freq_itemset3 = filter_sup(count_candidate3_df)

freq_itemset3

"""#All Frequent Itemset"""

#Let'see each frequent itemset (L)
freq_itemset1

freq_itemset2

freq_itemset3

frequent_itemset = pd.concat([freq_itemset1, freq_itemset2, freq_itemset3], axis=0)

frequent_itemset

#Reset the index
frequent_itemset_final = frequent_itemset.reset_index(drop=True)



"""#Final Output of Freq. Itemset (L1-L3)"""

frequent_itemset_final
