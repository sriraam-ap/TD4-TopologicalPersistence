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

def get_boundary_matrix(filtration_df: pd.DataFrame) -> list:
    """
    Parameters
    ----------
    filtration_df : pd.DataFrame
    In [4]: filtration_df
    Out[4]:
    val  dim       vert
    0  0.0    0        {0}
    1  0.0    0        {1}
    2  0.0    0        {2}
    3  1.0    1     {0, 1}
    4  1.0    1     {1, 2}
    5  1.0    1     {0, 2}
    6  2.0    2  {0, 1, 2}

    Returns
    -------
    boundary_matrix : list
    In [2]: boundary_matrix
    Out[2]: 
    [[0, 0, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 1, 0, 0],
    [0, 0, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0]]
    """
    N = len(filtration_df)
    boundary_matrix = [[0 for i in range(N)] for j in range(N)]

    for i, row in filtration_df.iterrows():
        print(f"{i}/{len(filtration_df)}")
        if row.dim == 0:
            continue
        else:
            vert = row.vert
            df_subset = filtration_df[filtration_df["dim"] == row.dim - 1]
            df_subset = df_subset[df_subset.apply(lambda row: row["vert"].issubset(vert), axis=1)]
            for idx in df_subset.index:
                boundary_matrix[idx][i] = 1

    return boundary_matrix


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Run Syntax: python persistence.py <path to filteration data>")
        sys.exit(0)

    filtration = read_filtration(sys.argv[1])
    for simplex in filtration:
        print(simplex)
