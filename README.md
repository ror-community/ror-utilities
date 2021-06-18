# ror-utilities
Utility scripts for working with the [ROR API](https://github.com/ror-community/ror-api)

## Prerequisites

- [Install and configure Python](https://wiki.python.org/moin/BeginnersGuide/Download) on your machine

## Match a list of other organization IDs to ROR
The ROR API can be used to find the ROR ID equivalent for other organization identifers included the external_ids of ROR records, such Crossref Funder ID, GRID, ISNI, OrgRef and Wikidata. Not all identifier types are available for every organization and Ringgold identifiers are not available in ROR at this time.

This script accepts a CSV list of other organzation IDs as input and returns a CSV with each input ID and its corresponding ROR ID as output. [TODO] If no match was found for a given other ID, the ROR ID field will be blank. In the (unlikely) case the multiple matches were found, the ROR ID field will contain a comma separated list of ROR IDs.

To use this script:
1. Clone/download this repository to your computer 
        git@github.com:ror-community/ror-utilities.git

2. Move to the directory you just cloned
        cd ./ror-utilities

3. Prepare a comma-separated list of other IDs you wish to match to ROR, save as a CSV file, and place it in the /input directory inside the ror-utilities directory.
        vim ./input/example_input_ids_list.csv
        
3. Run the script, specifying the name of the input file you just created as an argument, including the .csv extension. Do not include the full filepath; script will look for this file in ./input 
        python match-other-ids-to-ror.py -f example_input_ids_list.csv

4. 


