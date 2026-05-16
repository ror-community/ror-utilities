import urllib.parse
import argparse
import csv
import requests
from os import path
from datetime import datetime

ROR_API_ENDPOINT = "https://api.ror.org/v2/organizations"
INPUT_DIR = "input/"
OUTPUT_DIR = "output/"
ES_RESERVED_CHARS = [ "+", "-", "&", "|", "!", "(", ")", "{", "}", "[", "]", "^", '"', "~", "*", "?", ":", "\\", "/" ]

def extract_names_by_type(names_list, name_type):
    """Extract name values from v2 'names' array for a given type (e.g. 'ror_display', 'alias', 'acronym', 'label')."""
    return [entry['value'] for entry in names_list if name_type in entry.get('types', [])]

def process_file(inputFile):
    now = datetime.now()
    output_file = OUTPUT_DIR + now.strftime("%Y-%m-%d") + "_search_results_query.csv"
    fields = ['search_term', 'query_results', 'has_good_match', 'matched_field', 'first_match_names', 'first_match_aliases', 'first_match_acronyms', 'first_match_labels']
    with open(inputFile) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        with open(output_file, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(fields)
            for row in reader:
                search_term = row[0]
                print("Searching for: " + search_term)
                for i in search_term:
                    if i in ES_RESERVED_CHARS:
                        search_term = search_term.replace(i, "\\" + i)
                params = {'query': search_term}
                query_response = requests.get(ROR_API_ENDPOINT + '?' + urllib.parse.urlencode(params)).json()
                query_results = query_response['number_of_results']
                first_match_names = []
                first_match_aliases = []
                first_match_acronyms = []
                first_match_labels = []
                has_good_match = False
                matched_field = ''

                if query_results > 0:
                    items = query_response['items']
                    top_items = items if len(items) <= 5 else items[:5]

                    for item in top_items:
                        names_list = item.get('names', [])
                        # v2: 'ror_display' type is the primary display name (replaces v1 'name')
                        first_match_names.extend(extract_names_by_type(names_list, 'ror_display'))
                        first_match_aliases.extend(extract_names_by_type(names_list, 'alias'))
                        first_match_acronyms.extend(extract_names_by_type(names_list, 'acronym'))
                        first_match_labels.extend(extract_names_by_type(names_list, 'label'))

                if first_match_names:
                    if search_term in first_match_names:
                        has_good_match = True
                        matched_field = 'name'
                    elif search_term in first_match_aliases:
                        has_good_match = True
                        matched_field = 'aliases'
                    elif search_term in first_match_acronyms:
                        has_good_match = True
                        matched_field = 'acronyms'
                    elif search_term in first_match_labels:
                        has_good_match = True
                        matched_field = 'labels'
                    else:
                        has_good_match = False

                writer.writerow([search_term, query_results, has_good_match, matched_field, first_match_names, first_match_aliases, first_match_acronyms, first_match_labels])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', type=str)
    args = parser.parse_args()
    input_file = INPUT_DIR + args.filename
    if path.exists(input_file):
        process_file(input_file)
    else:
        print("File " + input_file + " does not exist. Cannot process file.")

if __name__ == '__main__':
    main()