import argparse
import json
import requests
from benedict import benedict

ROR_API_ENDPOINT = "https://api.ror.org/v2/organizations/"  # updated to v2
WIKIDATA_API_ENDPOINT = "https://www.wikidata.org/w/api.php?action=wbgetentities&ids={wikidata_id}&languages=en&props=labels|descriptions|claims&format=json"
WIKIDATA_SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"

### Mapping ROR to Ringgold as seen in Datacite Commons ###
# (https://github.com/datacite/lupo/blob/master/app/models/concerns/wikidatable.rb)
def map_ror_to_ringgold(ror):
    # get organization data from ROR and extract Wikidata IDs
    organization = get_data_from_ror(ror)

    # v2: external_ids is now an array of objects with a 'type' key (lowercase)
    # instead of a keyed dict, so we find the wikidata entry by filtering on type
    wikidata_entry = next(
        (entry for entry in organization.get('external_ids', []) if entry.get('type') == 'wikidata'),
        None
    )
    wikidata_ids = wikidata_entry['all'] if wikidata_entry else []

    ringgold_ids = []
    # for every Wikidata ID:
    for wikidata_id in wikidata_ids:
        # get data from Wikidata
        wikidata = benedict(get_data_from_wikidata(wikidata_id))
        # .. and extract Ringgold ID if present
        WIKIDATA_RINGGOLD_PATH = f"entities.{wikidata_id}.claims.P3500[0].mainsnak.datavalue.value"
        if WIKIDATA_RINGGOLD_PATH in wikidata:
            ringgold_ids.append(wikidata[WIKIDATA_RINGGOLD_PATH])
    return ringgold_ids

# HTTP request to get data from ROR API
def get_data_from_ror(ror):
    response = requests.get(ROR_API_ENDPOINT + ror)
    response.raise_for_status()    
    response_text = response.text.encode('ascii', 'ignore')
    return json.loads(response_text)

# HTTP request to get data from Wikidata API
def get_data_from_wikidata(wikidata_id):

    headers = {
        'User-Agent': 'map-ringgold-via-wikidata/1.0 (https://github.com/ror-community/ror-utilities; mailto:support@ror.org)'
    }
    response = requests.get(
        WIKIDATA_API_ENDPOINT.format(wikidata_id=wikidata_id),
        headers=headers
    )
    response.raise_for_status()
    response_text = response.text.encode('ascii', 'ignore')
    return json.loads(response_text)
 
####  Mapping Ringgold to ROR ####
# query Wikidata via SPARQL API to get ROR ID given a Ringgold ID

def map_ringgold_to_ror(ringgold):
    query = ("SELECT DISTINCT ?rorid WHERE {"
             "?item p:P3500 ?statement0."
             f"?statement0 (ps:P3500) '{ringgold}'."
             "?item p:P6782 ?statement1."
             "?statement1 (ps:P6782) ?rorid.}")
    headers = {
        'User-Agent': 'map-ringgold-via-wikidata/1.0 (https://github.com/ror-community/ror-utilities; mailto:support@ror.org)',
        'Accept': 'application/sparql-results+json'
    }
    response = requests.get(
        WIKIDATA_SPARQL_ENDPOINT,
        params={'query': query},
        headers=headers
    )
    response.raise_for_status()
    sparql_results = benedict(response.json())
    ror_ids = []
    for result in sparql_results['results.bindings']:
        result_ben = benedict(result)
        ror_ids.append(result_ben['rorid.value'])
    return ror_ids

# Usage example:
# ROR -> Ringgold: python map-ringgold-via-wikidata.py -t ror -v https://ror.org/04aj4c181
# Ringgold -> ROR: python map-ringgold-via-wikidata.py -t ringgold -v 28359
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--idtype', "-t", type=str, choices=["ror", "ringgold"], required=True)
    parser.add_argument('--value', "-v", type=str, required=True)
    args = parser.parse_args()
    if args.idtype == "ror":
        ror = args.value
        print(f"Input : {ror}")
        candidates_ringgold = map_ror_to_ringgold(ror)
        print(f"{len(candidates_ringgold)} candidates for Ringgold IDs: {candidates_ringgold}")
    else:
        ringgold = args.value
        print(f"Input : {ringgold}")
        candidates_ror = map_ringgold_to_ror(ringgold)
        print(f"{len(candidates_ror)} candidates for ROR IDs: {candidates_ror}")

if __name__ == '__main__':
    main()