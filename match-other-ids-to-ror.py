import argparse
import csv
import requests
import urllib
from os import path
from datetime import datetime

ROR_API_ENDPOINT = "https://api.ror.org/organizations"
INPUT_DIR = "input/"
OUTPUT_DIR = "output/"

def process_file(inputFile):
    now = datetime.now()
    output_file = OUTPUT_DIR + now.strftime("%Y-%m-%d") + "_matched_ror_ids.csv"
    fields = ['input_id', 'ror_id']
    with open(inputFile) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        with open(output_file, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(fields)
            for row in reader:
                input_id = row[0]
                print("Finding ROR for: " + input_id)
                search_term = '"' + input_id + '"'
                params = {'query': search_term}
                ror_id=''
                try:
                    response = requests.get(ROR_API_ENDPOINT + '?' + urllib.parse.urlencode(params)).json()
                    if response['number_of_results'] == 0:
                        ror_id = ''
                    elif response['number_of_results'] == 1:
                        ror_id = response['items'][0]['id']
                    else:
                        ror_id = ''
                        for items in response:
                            ror_id = ror_id + ", " + response['items'][0]['id']
                    print("Found match: " + ror_id)
                except ValueError:
                    ror_id = 'Error'
                    pass
                finally:
                    writer.writerow([input_id, ror_id])
                    c.close()

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