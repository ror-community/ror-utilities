import re
import json
import numpy as np
import csv
import sys

#This script was created by Ramon Granell ramon.granell@oerc.ox.ac.uk to math ROR (https://ror.org/) organisations with FAIRsharing (https://fairsharing.org/) organisations.

#To execute the script: python matching_name_shortname.py ror_file file_to_match where:
# ror_file is the json dump database file obtained from the ROR website
# file_to_match is text file using as separator field "|" with the following fields in each line:
# field 1: organisation ID
# field 2: organisation name
# field 3: organisation homepage

#Function copied from https://stackabuse.com/levenshtein-distance-and-text-similarity-in-python/
def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    #matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    #print (matrix)
    return (matrix[size_x - 1, size_y - 1])

nameRorFile = sys.argv[1]
nameMatchingFile = sys.argv[2]

pattern = re.compile('[^A-Za-z0-9 ]+')

#1 Load the nameMatchingFile
#pick organisations that are not found after step2
dbOrgs_analysed= []
dbOrgs_new= []
l =0

with open(nameMatchingFile, 'r', encoding='utf8') as f:
    read_tsv = csv.reader(f, delimiter="|")
    for line in read_tsv:
            dbOrg = {}
            dbOrg['urlFairsharing'] = line[2].strip()
            dbOrg['name'] = line[1]
            dbOrg['myName'] = pattern.sub('', dbOrg['name']).lower()
            dbOrg['lenMyName'] = len(dbOrg['myName'])
            dbOrg['url'] = line[2]
            dbOrg['id'] = line[0]
            dbOrgs_new.append(dbOrg)




n=0
noURL=0
parsed_json_aliases = []
parsed_names = []

with open(nameRorFile, 'r', encoding='utf8') as f:
    text = f.read()
    #print(text)
    parsed_json = json.loads(text)

for i in range(len(parsed_json)):
    if len(parsed_json[i]['links'])>0:
        url= parsed_json[i]['links'][0]
    else:
        noURL+=1
        url='NOEXISTINGGGGGGGGGG'


    parsed_json[i]['link'] = url
    parsed_json[i]['myName'] = pattern.sub('', parsed_json[i]['name']).lower()
    parsed_json[i]['lenMyName'] = len(parsed_json[i]['myName'])

    v = {}
    v['link'] = parsed_json[i]['link']
    v['name'] = parsed_json[i]['name']
    v['myName'] = parsed_json[i]['myName']
    v['lenMyName'] = parsed_json[i]['lenMyName']
    v['id'] = parsed_json[i]['id']
    parsed_names.append(v)

    if len(parsed_json[i]['aliases']) > 0:
        for j in range(len(parsed_json[i]['aliases'])):
            t = {}
            t['link'] = parsed_json[i]['link']
            t['name'] = parsed_json[i]['name']
            t['myName'] = pattern.sub('', parsed_json[i]['aliases'][j]).lower()
            t['id'] = parsed_json[i]['id']

            parsed_json_aliases.append(t)

    if len(parsed_json[i]['labels']) > 0:
        for j in range(len(parsed_json[i]['labels'])):
            t = {}
            t['link'] = parsed_json[i]['link']
            t['name'] = parsed_json[i]['name']
            t['myName'] = pattern.sub('', parsed_json[i]['labels'][j]['label']).lower()
            t['id'] = parsed_json[i]['id']

            parsed_json_aliases.append(t)

    if len(parsed_json[i]['acronyms']) > 0:
        for j in range(len(parsed_json[i]['acronyms'])):
            t = {}
            t['link'] = parsed_json[i]['link']
            t['name'] = parsed_json[i]['name']
            t['myName'] = pattern.sub('', parsed_json[i]['acronyms'][j]).lower()
            t['id'] = parsed_json[i]['id']

            parsed_json_aliases.append(t)
list_orgs = []
list_orgs.append(dbOrgs_new)
num_file = 0
for orgst in list_orgs:
    fileToPrint = open("new_org_compare_names.tsv", "w")
    for orgTocheck in orgst:
        closestNames = []
        for i in range(3):
            elIds = {'id': -1,
                     'dist': 999999
                     }
            closestNames.append(elIds)
        for i in range(len(parsed_names)):
            edit_distanceName = levenshtein(orgTocheck['myName'], parsed_names[i]['myName'])
            if edit_distanceName < closestNames[-1]['dist']:
                toInsert = 2
                for r in range(1, -1, -1):
                    if edit_distanceName > closestNames[r]['dist']:
                        break
                    else:
                        toInsert = r
                # print(str(toInsert))
                if toInsert != 2:
                    for r in range(2, toInsert, -1):
                        # print(str(r)+str(closestURLs[r]['id']))
                        closestNames[r]['id'] = closestNames[r - 1]['id']
                        # print(str(r) + str(closestURLs[r]['id']))
                        closestNames[r]['dist'] = closestNames[r - 1]['dist']
                closestNames[toInsert]['dist'] = edit_distanceName
                closestNames[toInsert]['id'] = i
        if closestNames[0]['dist'] > 4:
            for j in range(len(parsed_json_aliases)):
                edit_distanceName = levenshtein(orgTocheck['myName'], parsed_json_aliases[j]['myName'])
                if edit_distanceName < closestNames[-1]['dist']:
                    toInsert = 2
                    for r in range(1, -1, -1):
                        if edit_distanceName > closestNames[r]['dist']:
                            break
                        else:
                            toInsert = r
                    # print(str(toInsert))
                    if toInsert != 2:
                        for r in range(2, toInsert, -1):
                            # print(str(r)+str(closestURLs[r]['id']))
                            closestNames[r]['id'] = closestNames[r - 1]['id']
                            # print(str(r) + str(closestURLs[r]['id']))
                            closestNames[r]['dist'] = closestNames[r - 1]['dist']
                    closestNames[toInsert]['dist'] = edit_distanceName
                    closestNames[toInsert]['id'] = -1*j
        fileToPrint.write(str(closestNames[0]['dist'])+"\t"+str(orgTocheck['id']))
        fileToPrint.write("\t"+orgTocheck['name']+" ("+orgTocheck['url']+")")
        for i in range(3):
            if closestNames[i]['id'] < 0:
                elem = parsed_json_aliases[-1*closestNames[i]['id']]
            else:
                elem = parsed_names[closestNames[i]['id']]
            #print(elem)
            fileToPrint.write('\t' + str(closestNames[i]['dist']) + ' +++ ' + str(elem['id']) + '+++ (' + str(
                elem['name']) + '+++' + str(
                elem['link']) + ')')
        fileToPrint.write("\n")
    num_file+=1
    fileToPrint.close()
