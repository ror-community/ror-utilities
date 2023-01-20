import re
import json
import numpy as np
import csv
import sys

#This script was created by Ramon Granell ramon.granell@oerc.ox.ac.uk to math ROR (https://ror.org/) organisations with FAIRsharing (https://fairsharing.org/) organisations.

#To execute the script: python matching_urls.py ror_file file_to_match where:
# ror_file is the json database dump file obtained from the ROR website
# file_to_match is text file using as separator field "|" with the following fields in each line:
# field 1: organisation ID
# field 2: organisation name
# field 3: organisation homepage



#Function obtained from https://stackabuse.com/levenshtein-distance-and-text-similarity-in-python/
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
                    matrix[x, y-1] + 1
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
parsed_urls = []

with open(nameRorFile, 'r', encoding='utf8') as f:
    text = f.read()
    #print(text)
    parsed_json = json.loads(text)

for i in range(len(parsed_json)):
    if len(parsed_json[i]['links'])>0:
        url= parsed_json[i]['links'][0]
    else:
        noURL+=1
        url='NOEXISTING'


    parsed_json[i]['link'] = url
    parsed_json[i]['myName'] = pattern.sub('', parsed_json[i]['name']).lower()
    parsed_json[i]['lenMyName'] = len(parsed_json[i]['myName'])
    v = {}
    v['link'] = parsed_json[i]['link']
    v['name'] = parsed_json[i]['name']
    v['myName'] = parsed_json[i]['myName']
    v['lenMyName'] = parsed_json[i]['lenMyName']
    v['id'] = parsed_json[i]['id']
    parsed_urls.append(v)


list_orgs = []
list_orgs.append(dbOrgs_new)

list_file_print = "new_org_compare_urls.tsv"
for orgst in list_orgs:
    fileToPrint = open(list_file_print, "w")
    for orgTocheck in orgst:
        closestNames = []
        for i in range(3):
            elIds = {'id': -1,
                     'dist': 999999
                     }
            closestNames.append(elIds)
        for i in range(len(parsed_urls)):
            edit_distanceName = levenshtein(orgTocheck['url'], parsed_urls[i]['link'])
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
        fileToPrint.write(str(closestNames[0]['dist'])+"\t"+"\t"+"https://fairsharing.org/organisations/"+str(orgTocheck['id']))
        fileToPrint.write("\t"+orgTocheck['name']+" ("+orgTocheck['url']+")")
        for i in range(3):
            fileToPrint.write('\t' + str(closestNames[i]['dist']) + ' +++ ' + str(parsed_urls[closestNames[i]['id']]['id']) + '+++ (' + str(
                parsed_urls[closestNames[i]['id']]['name']) + '+++' + str(
                parsed_urls[closestNames[i]['id']]['link']) + ')')
        fileToPrint.write("\n")
    fileToPrint.close()
