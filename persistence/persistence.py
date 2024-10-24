import sys
import copy
from typing import List
import locale


class Simplex:
    def __init__(self, line: str):
        # Parse the string input (line) into float and integers
        tokens = list(map(float, line.split()))
        self.val = tokens[0]
        self.dim = int(tokens[1])
        # Extract vertex indices from the line and store them in a set
        self.vert = set(map(int, tokens[2:2 + self.dim + 1]))

    def __str__(self):
        return f"{{val={self.val}; dim={self.dim}; {sorted(self.vert)}}}\n"

def read_filtration(filename: str) -> List[Simplex]:
    """
    Parameters
    ----------
    filename : str
    Ex. filename = "./filtrations/filtration_A.txt"

    Returns
    -------
    filtration : list
    In [2]: filtration
    Out[2]:
    [<persistence.persistence.Simplex at 0x7fdc3571c650>,
    <persistence.persistence.Simplex at 0x7fdc35801f10>,
    <persistence.persistence.Simplex at 0x7fdc35802110>,
    ...
    """
    filtration = []
    # Set locale to ensure consistent float number parsing (for example with commas)
    locale.setlocale(locale.LC_NUMERIC, 'en_US.UTF-8')
    
    with open(filename, 'r') as file:
        # Read each line and create a Simplex object
        for line in file:
            filtration.append(Simplex(line.strip()))
    
    return filtration

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Run Syntax: python persistence.py <path to filteration data>")
        sys.exit(0)

    filtration = read_filtration(sys.argv[1])
    for simplex in filtration:
        print(simplex)
