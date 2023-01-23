## Author
Name: Sandra Mierz
GitHub: https://github.com/smierz


## Create an organization tree based on child relationships

Beginning from a specific parent organization, you can create an organization tree by recursively traversing relationships with type=child.

This script accepts a ROR ID as an argument, and prints an organization tree in the console, with the specified ROR ID as the top-most node in the tree.

Usage:

    python organization-tree.py -r 'https://ror.org/01an7q238'

Note: ROR ID argument can also be specified as just the ID path, ex ```01an7q238```
