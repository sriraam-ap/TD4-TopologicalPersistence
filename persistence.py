import sys
from typing import List
import locale
import pandas as pd

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
    filtration = []
    # Set locale to ensure consistent float number parsing (for example with commas)
    locale.setlocale(locale.LC_NUMERIC, 'en_US.UTF-8')
    
    with open(filename, 'r') as file:
        # Read each line and create a Simplex object
        for line in file:
            filtration.append(Simplex(line.strip()))
    
    return filtration

def convert_filtration_df(filtration: list) -> pd.DataFrame:
    val_list = []
    dim_list = []
    vert_list = []
    for i, s in enumerate(filtration):
        print(f"{i}/{len(filtration)}")
        val_list.append(s.val)
        dim_list.append(s.dim)
        vert_list.append(s.vert)
    df = pd.DataFrame({"val": val_list, "dim": dim_list, "vert": vert_list})
    df_sorted = df.sort_values(by=['val', 'dim'])
    return df_sorted

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Run Syntax: python persistence.py <path to filteration data>")
        sys.exit(0)

    filtration = read_filtration(sys.argv[1])
    for simplex in filtration:
        print(simplex)
