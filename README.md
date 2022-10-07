# ror-utilities
Utility scripts for working with the [ROR API](https://github.com/ror-community/ror-api)

## Prerequisites

- [Install and configure Python](https://wiki.python.org/moin/BeginnersGuide/Download) on your machine
- Clone/download this repository to your computer, ex ```git clone git@github.com:ror-community/ror-utilities.git```
- Move to the directory you just cloned, ex ```cd ./ror-utilities```

## Search ROR API for a list of organization names
The ROR API can be used to find records matching an organization name, alias or acronynm, either by using a simple [query parameter search](https://ror.readme.io/docs/rest-api#query-parameter) or the [affialiation matching service](https://ror.readme.io/docs/rest-api#affiliation-parameter). These scripts accept a CSV list of organization names as input and return a CSV with possible match(es) and other details, depending on which query type is used.

Usage:

### Simple query

1. Prepare a comma-separated list of organization names you wish to search in ROR, save as a CSV file, and place it in the /input directory inside the ror-utilities directory, ex ```input/org_names.csv```

2. Run the script, specifying the name of the input file you just created as an argument, including the .csv extension. Do not include the full filepath; script will look for this file in ./input

        python search-by-name-query.py -f org_names.csv

3. A CSV file with the results will be generated in ```./output/YYYY-MM-DD_search_results_query.csv```

### Affiliation matching

1. Prepare a comma-separated list of organization names you wish to search in ROR, save as a CSV file, and place it in the /input directory inside the ror-utilities directory, ex ```input/org_names.csv```

2. Run the script, specifying the name of the input file you just created as an argument, including the .csv extension. Do not include the full filepath; script will look for this file in ./input

        python search-by-name-affiliation.py -f org_names.csv

3. A CSV file with the results will be generated in ```./output/YYYY-MM-DD_search_results_affiliation_matching.csv```

## Match a list of other organization IDs to ROR
The ROR API can be used to find the ROR ID equivalent for other organization identifers included the external_ids of ROR records, such Crossref Funder ID, GRID, ISNI, OrgRef and Wikidata. Not all identifier types are available for every organization and Ringgold identifiers are not available in ROR at this time.

This script accepts a CSV list of other organzation IDs as input and returns a CSV with each input ID and its corresponding ROR ID (full URL) as output.

- If no match was found for a given other ID, the ROR ID field will be blank.
- In the (unlikely) case the multiple matches were found, the ROR ID field will contain a comma separated list of ROR IDs.
- If the ROR API returned an eror, the ROR ID field will contain "Error"

Usage:

1. Prepare a comma-separated list of other IDs you wish to match to ROR, save as a CSV file, and place it in the /input directory inside the ror-utilities directory. An example file is located in ```input/example-input-ids.csv```

        vim ./input/example-input-ids.csv

2. Run the script, specifying the name of the input file you just created as an argument, including the .csv extension. Do not include the full filepath; script will look for this file in ./input

        python match-other-ids-to-ror.py -f example-input-ids.csv

3. A CSV file with the results will be generated in ```./output/YYYY-MM-DD_matched_ror_ids.csv```

## Create an organization tree based on child relationships

Begining from a specific parent organization, you can create an organization tree by recursively traversing elationships with type=child.

This script accepts a ROR ID as an argument, and prints an organization tree in the console, with the specified ROR ID as the top-most node in the tree.

Usage:

    python organization-tree.py -r 'https://ror.org/01an7q238'

Note: ROR ID argument can also be specified as just the ID path, ex ```01an7q238```



