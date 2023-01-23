import argparse
import json
import requests
from SPARQLWrapper import SPARQLWrapper, JSON
from benedict import benedict

ROR_API_ENDPOINT = "https://api.ror.org/organizations/"
WIKIDATA_API_ENDPOINT = "https://www.wikidata.org/w/api.php?action=wbgetentities&ids={wikidata_id}&languages=en&props=labels|descriptions|claims&format=json"
WIKIDATA_SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"


### Mapping ROR to Ringgold as seen in Datacite Commons ###
# (https://github.com/datacite/lupo/blob/master/app/models/concerns/wikidatable.rb)
def map_ror_to_ringgold(ror):
    # get organization data from ROR and extract Wikidata IDs
    organization = benedict(get_data_from_ror(ror))
    ROR_WIKIDATA_PATH = "external_ids.Wikidata.all"
    wikidata_ids = organization[ROR_WIKIDATA_PATH] if ROR_WIKIDATA_PATH in organization else []

    ringgold_ids = []
    # for every Wikidata ID :
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
    response_text = response.text.encode('ascii', 'ignore')
    return json.loads(response_text)

# HTTP request to get data from Wikidata API
def get_data_from_wikidata(wikidata_id):
    response = requests.get(WIKIDATA_API_ENDPOINT.format(wikidata_id=wikidata_id))
    response_text = response.text.encode('ascii', 'ignore')
    return json.loads(response_text)


####  Mapping Ringgold to ROR ####
# query Wikidata via SPARQL API to get ROR ID given a Ringgold ID
def map_ringgold_to_ror(ringgold):
    sparql = SPARQLWrapper(WIKIDATA_SPARQL_ENDPOINT)
    sparql.setQuery("SELECT DISTINCT ?rorid WHERE {"
                    "?item p:P3500 ?statement0."
                    f"?statement0 (ps:P3500) '{ringgold}'."
                    "?item p:P6782 ?statement1."
                    "?statement1 (ps:P6782) ?rorid.}")
    sparql.setReturnFormat(JSON)
    sparql_results = benedict(sparql.query().convert())

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
