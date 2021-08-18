import requests
from anytree import Node, RenderTree

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
    return response.json()


def main():
    ror_harvard = "https://ror.org/03vek6s52"
    tree = construct(ror_harvard)
    print(RenderTree(tree))


if __name__ == '__main__':
    main()
