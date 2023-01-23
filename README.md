# ror-utilities
This repository contains Python utility scripts written by ROR staff and third parties that work with the [ROR API](https://github.com/ror-community/ror-api) or [ROR data](https://github.com/ror-community/ror-data) to perform various useful functions such as matching other organization identifiers to ROR IDs. Please note that these scripts are not officially supported by ROR and may be out of date with current versions of the ROR API or schema. They are provided here primarily to serve as models for those who wish to write their own ROR-related Python scripts.

## List of scripts

* ```fairsharing-match-scripts``` 
	* Contributor: [Ramon Granell](https://github.com/ramGranell) of [FAIRsharing](https://fairsharing.org)
	* [README](https://github.com/ror-community/ror-utilities/blob/main/fairsharing-match-scripts/README.md)
	* `matching_name_shortname.py` - Accepts a CSV list of organization names, matches them to ROR records, and produces a TSV file that includes Levenshtein distances between the text strings. 
	* `matching_urls.py` - Accepts a CSV list of organization home pages, matches them to ROR records, and produces a TSV file that includes Levenshtein distances between the text strings. 
* ```general-scripts```
	* [README](https://github.com/ror-community/ror-utilities/blob/main/general-scripts/README.md)
	* `map-ringgold-via-wikidata.py` - Accepts a single ROR ID as input and suggests the corresponding Ringgold ID  when the ROR ID's corresponding Wikidata page includes a Ringgold ID. 
	* `match-other-ids-to-ror.py` - Accepts a CSV list of other organization IDs (e.g., GRID, ISNI) as input and returns a CSV with corresponding ROR IDs.
	* `search-by-name-affiliation.py` - Searches the ROR API for organization names from a CSV file using the ROR API [?affiliation endpoint](https://ror.readme.io/docs/match-organization-names-to-ror-ids#affiliation-parameter-approach). Does not return corresponding ROR IDs.
	* `search-by-name-query` -  Searches the ROR API for organization names from a CSV file using the ROR API [?query endpoint](https://ror.readme.io/docs/match-organization-names-to-ror-ids#query-parameter-approach). Does not return corresponding ROR IDs.
* ```organization-tree-scripts```
	 * Contributor: [Sandra Mierz](https://github.com/smierz)
	* [README](https://github.com/ror-community/ror-utilities/blob/main/organization-tree-scripts/README.md)
	* `organization-tree.py` - This script accepts a ROR ID as an argument and prints an organization tree in the console with the specified parent ROR ID as the top-most node in the tree and child organizations as lower nodes.

## Contributing scripts
To contribute one or more scripts to this repository, please open a pull request structured as follows:

1. Place all your contributions in a directory with a name that indicates the source and/or function of the scripts: e.g., ```myorgname-match-scripts```
2. Include a README file, your scripts, and any subdirectories in your directory. Optionally, you may also include a LICENSE file; otherwise, your contributions will be covered by the top-level [LICENSE](LICENSE) in ror-utilities. We also encourage you to include sample files that can be used to test your scripts.
3. In the README file in your directory, provide clear and detailed usage instructions and list any required Python packages. You may also include your name, GitHub handle, and contact information if you wish.
4. If your scripts require Python packages that are not part of the Python Standard Library, include a ```requirements.txt``` file to your directory in the format ```nameofpackage==version``` (for example, ```requests==2.27.1```). You can use [pipreqs](https://github.com/bndr/pipreqs) to generate requirements.txt automatically.

## Using scripts

### Prerequisites

- [Install and configure Python](https://wiki.python.org/moin/BeginnersGuide/Download) on your machine
- Clone/download this repository to your computer, ex ```git clone git@github.com:ror-community/ror-utilities.git```
- Move to the directory you just cloned, ex ```cd ./ror-utilities```

### Create a virtual environment & install packages

1. Create a Python virtual environment using [venv](https://docs.python.org/3/library/venv.html)

        python3 -m venv ~/venv

The venv path and directory name can be anything you like, ex ```~/ror-utilities```, but it's best to put it outside your ror-utilities repository so that you don't accidentally commit it.

2. Activate the virtual environment

        source ~/venv/bin/activate

The virtual environment name should now appear in your command prompt, ex ```(venv)```. If you used a different path or directory name in step 1, replace ```~/venv``` with that path/directory name.

3. Move to the directory that the script you'd like to run is located in and add required packages into the virtual environment

        cd general-scripts
        python -m pip install -r requirements.txt

**Note that each directory inside ror-utilities has its own requirements.txt file, so you will need to perform the steps above inside each directory you would like to run scripts from.**

4. When you are finished, deactivate the virtual environment (you can reactivate it by running the command in step 2 above)

        deactivate


