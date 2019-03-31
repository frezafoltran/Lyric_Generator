# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 09:42:16 2018

@author: Adm
"""

import word_processor as wp
import scraper
import helper_methods as helper
import rhyme_distances as rdist
import scrapping_methods as sm
import boto3

word_relation_table = dynamodb.Table("WordRelation")

# main file
# Read phonetics and words from file
dic_phon = []
file = open('phonetic_word.txt', 'r')

for line in file:
    word = line[:line.find(':')]
    phon = line[line.find(':')+1:-1]
    dic_phon.append({'id': word, 'phonetic': phon})

size = len(dic_phon)
distances = []
param = []

for i in range(1,5):
    for j in range(1,i):
        param.append((i,j))

print(param)

#

# iterate through each word in dic_phon
for i in range(10,10000,100):
    print(dic_phon[i])
    print(i)

    #for each word, calculate ordered list of words that rhyme
    for l in range(len(param)):
        temp = []

        for j in range(size):
            d = rdist.phonetic_dist(dic_phon[i]['phonetic'],dic_phon[j]['phonetic'], list(param[l]), True)
            temp.append({'': dic_phon[j]['id'],'d': d})

        temp = sorted(temp, key=lambda k: k['d'])
        distances.append(list(param[l])+temp[1:10])

    distances.append("-------End of " + dic_phon[i]['id']+", next word below")


# Write results to .txt
file = open('rhyme_list.txt', 'w')

for i in range(len(distances)):
    print(i)
    entry = str(distances[i])
    entry = entry.replace('{','')
    entry = entry.replace('}','')
    entry = entry.replace('\'', '')
    entry = entry.replace(':', '')
    file.write(entry)
    file.write('\n')
    file.write('\n')

file.close()


# Store phonetics in .txt for easy and offline access
"""
viable = wp.find_viable_words()
dic = []

for i in range(len(viable)):

    print(i)
    try:
        entry = helper.get_by_id(viable[i], word_relation_table)
        dic.append({'word':entry['id'], 'phonetic':entry['phonetic']})

    except KeyError:
        print('item not found')

print(len(dic))

file = open('phonetic_word.txt', 'w')

for i in range(len(dic)):
    print(i)
    file.write(''.join(dic[i]['word']))
    file.write(':')
    file.write(''.join(dic[i]['phonetic']))
    file.write('\n')

file.close()

"""

