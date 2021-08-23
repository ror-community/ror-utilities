import requests
from anytree import Node, RenderTree
import argparse
import json

ROR_API_ENDPOINT = "https://api.ror.org/organizations/"


# construct organizational tree recursively starting at given ROR
def construct(ror, parent=None):
    organization = get_data(ror)
    current_node = Node(organization["name"], parent=parent)

    for rel in organization['relationships']:
        if rel["type"]=="Child":
            construct(rel["id"], current_node)

    return current_node

# HTTP request to get data from ROR API
def get_data(ror):
    response = requests.get(ROR_API_ENDPOINT + ror)
    response_text = response.text.encode('ascii', 'ignore')
    return json.loads(response_text)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--ror', type=str, default='https://ror.org/03vek6s52')
    args = parser.parse_args()
    ror = args.ror
    tree = construct(ror)
    print(RenderTree(tree))


if __name__ == '__main__':
    main()
