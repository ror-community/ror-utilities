# Matching organisations
Scripts for matching existing organisations from any database to ROR organisations using files.


## Description

These scripts allow a user to compare and match his/her organisations to the ROR organisations. The main goal is to find if these organisations exist in the ROR database performing automatic comparisions over two different text fields (organisation name and homepage). 

There are two independent scripts: 1) "matching_name_shortname.py" to compare organisations names (it also uses ROR alternative names) and 2) "matching_urls.py" to match organisation homepages. The ouput of each one of the scripts is a file with the three ROR organisations with the smallest distance from the user input organisation. Distances are based on text comparision using [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance). 

After the scripts are run, manually checks are recommendaded to be sure that a real match is among the closest matches. Please, note that scripts can take a long time to run if the whole ROR database is used (>100,000 organisations). Details about a real application of the scripts are in [FAIRsharing blog](https://blog.fairsharing.org/?p=239).

## Usage
### Name matching
To run the script matching_name_shortname.py do ```python matching_name_shortname.py ror_file.json file_to_match.csv``` where ror_file.json is the json database dump file obtained from the ROR website and file_to_match.csv is a text file with the user organisations to be matched. In this file, a separator field "|" is used in each line with the following fields:
- field 1: organisation ID
- field 2: organisation name
- field 3: organisation homepage

The output file is "new_org_compare_names.tsv" and uses tab separation ('\t') fields:
- field 1: smallest distance value between the input organisation and the ROR organisations
- field 2: organisation ID of the input
- field 3: organisation name (organisation URL) of the input
- field 4: smallest distance value between the input organisation and the ROR organisations "+++" ROR ID of the closest ROR organisation "+++(" name of this ROR organisation "+++" URL of this ROR organisation ")"
- field 5: second smallest distance value between the input organisation and the ROR organisations "+++" ROR ID of the second closest ROR organisation "+++(" name of this ROR organisation "+++" URL of this ROR organisation ")"
- field 6: third smallest distance value between the input organisation and the ROR organisations "+++" ROR ID of the third closest ROR organisation "+++(" name of this ROR organisation "+++" URL of this ROR organisation ")"

Example to run this script with two small files is: ```python matching_name_shortname.py example/ror_subset.json example/three_organisations.csv``` 

### Homepage matching
To run the script matching_urls.py do ```python matching_urls.py ror_file.json file_to_match.csv``` where ror_file.json is the json database dump file obtained from the ROR website and file_to_match.csv is a text file with the user organisations to be matched. In this file, a separator field "|" is used in each line with the following fields:
- field 1: organisation ID
- field 2: organisation name
- field 3: organisation homepage

The output file is "new_org_compare_urls.tsv" and uses tab separation ('\t') fields:
- field 1: smallest distance value between the input organisation and the ROR organisations
- field 2: organisation ID of the input
- field 3: organisation name (organisation URL) of the input
- field 4: smallest distance value between the input organisation and the ROR organisations "+++" ROR ID of the closest ROR organisation "+++(" name of this ROR organisation "+++" URL of this ROR organisation ")"
- field 5: second smallest distance value between the input organisation and the ROR organisations "+++" ROR ID of the second closest ROR organisation "+++(" name of this ROR organisation "+++" URL of this ROR organisation ")"
- field 6: third smallest distance value between the input organisation and the ROR organisations "+++" ROR ID of the third closest ROR organisation "+++(" name of this ROR organisation "+++" URL of this ROR organisation ")"

Example to run this script with two small files is: ```python matching_urls.py example/ror_subset.json example/three_organisations.csv``` 


Code created by Ramon Granell, ramon.granell@oerc.ox.ac.uk working for [FAIRsharing](https://fairsharing.org/) at Oxford University.
