import sys
import copy
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

    print("--- convert_filtration_df: collecting data ---")
    for i, s in enumerate(filtration):
        print(f"{i}/{len(filtration)}")
        val_list.append(s.val)
        dim_list.append(s.dim)
        vert_list.append(s.vert)

    print("--- convert_filtration_df: creating data frame ---")
    df = pd.DataFrame({"val": val_list, "dim": dim_list, "vert": vert_list})

    print("--- convert_filtration_df: sorting ---")
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
    print("--- get_boundary_matrix: creating initial boundary matrix ---")
    N = len(filtration_df)
    print(f"boundary matrix size: {N}x{N}")
    boundary_matrix = [[0 for i in range(N)] for j in range(N)]

    print("--- get_boundary_matrix: updating boundary matrix ---")
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

def get_sparse_boundary_matrix(filtration_df: pd.DataFrame) -> list:
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
    sbm : dict
    In [5]: sbm
    Out[5]:
    {'row': [0, 1, 1, 2, 0, 2, 3, 4, 5],
    'col': [3, 3, 4, 4, 5, 5, 6, 6, 6],
    'val': [1, 1, 1, 1, 1, 1, 1, 1, 1]}
    """
    print("--- get_boundary_matrix: creating initial boundary matrix ---")
    N = len(filtration_df)
    sbm = {"row": [], "col": [], "val": []}
    # row: index(int), col: index(int), val: 0 or 1

    print("--- get_boundary_matrix: updating boundary matrix ---")
    for i, row in filtration_df.iterrows(): # i is index of column
        print(f"{i}/{len(filtration_df)}")
        if row.dim == 0:
            continue
        else:
            print(f"--- get_boundary_matrix: taking subset of filtration_df")
            vert = row.vert
            print(f"vertices : {vert}")
            df_subset = filtration_df[filtration_df["dim"] == row.dim - 1]
            print(f"len(filtration_df): {len(filtration_df)} -> {len(df_subset)}")
            df_subset = df_subset[df_subset.apply(lambda one_row: one_row["vert"].issubset(vert), axis=1)]
            print(f"len(filtration_df): {len(filtration_df)} -> {len(df_subset)}")

            print(f"--- get_boundary_matrix: adding to sbm")
            for idx in df_subset.index:
                sbm["row"].append(idx)
                sbm["col"].append(i)
                sbm["val"].append(1)

    return sbm

class SparseBoundaryMatrixReducer(object):
    def __init__(self, verbose: bool=True):
        self._verbose = verbose # for debug

    def _sbm_df_to_sbm_dict(self, sbm_df: pd.DataFrame) -> dict:
        _sbm_df = sbm_df.reset_index()
        sbm_dict = {col: _sbm_df[col].to_list() for col in _sbm_df.columns}
        return sbm_dict
    
    def _sbm_dict_to_sbm_df(self, sbm_dict: dict) -> pd.DataFrame:
        sbm_df = pd.DataFrame(sbm_dict)
        sbm_df = sbm_df.set_index(keys=["row", "col"])
        return sbm_df

    def _get_lowest_row_idx_dict(self, sbm_df: pd.DataFrame) -> int:
        """
        Parameters
        ----------

        Returns
        -------
        lowest_row_idx_dict : dict
            key: column idx
            val: lowest row idx
            No column index in this dict means zero column

            In [12]: lowest_row_idx_dict
            Out[12]: {3: 1, 4: 2, 5: 2, 6: 5}
        """
        lowest_row_idx_dict = {}
        sbm = self._sbm_df_to_sbm_dict(sbm_df)

        N = len(sbm["col"])

        for i in range(N):
            print(f"{i}/{N}")
            lowest_row_idx_dict[sbm["col"][i]] = sbm["row"][i] # assuming sorted

        return lowest_row_idx_dict

    def _get_freq_of_low_dict(self, lowest_row_idx_dict: dict) -> dict:
        """
        Parameters
        ----------

        Returns
        -------
        freq_of_low_dict : dict
        key : lowest row index
        value : list of column indices of boundary matrix whose lowest row index is key

        In [2]: freq_of_low_dict
        Out[2]: {1: [3], 2: [4, 5], 5: [6]}
        """
        if self._verbose:
            print("--- BoundaryMatrixReducer._get_freq_of_low_dict ---")

        freq_of_low_dict = {}
        for col_idx, lowest_row_idx in lowest_row_idx_dict.items():
            if not lowest_row_idx in freq_of_low_dict:
                freq_of_low_dict[lowest_row_idx] = [col_idx]
            else:
                freq_of_low_dict[lowest_row_idx].append(col_idx)

        return freq_of_low_dict
    
    def reduce(self, sbm: list) -> list:
        """
        from persistence import read_filtration
        from persistence import SparseBoundaryMatrixReducer
        filtration = read_filtration("./tests/testcases/filtration_1.txt")
        df = convert_filtration_df(filtration)
        sbm = get_sparse_boundary_matrix(df)
        sbm_reducer = SparseBoundaryMatrixReducer(verbose=True)
        sbm_reduced = sbm_reducer.reduce(sbm)
        """
        sbm_df = self._sbm_dict_to_sbm_df(sbm)
        lowest_row_idx_dict = self._get_lowest_row_idx_dict(sbm_df)
        freq_of_low_dict = self._get_freq_of_low_dict(lowest_row_idx_dict)

        _counter = 0
        while max(list(map(len, freq_of_low_dict.values()))) > 1:
            if self._verbose:
                print(f"---{_counter}---")
                print(freq_of_low_dict)

            for key, val in freq_of_low_dict.items():
                if len(val) > 1:
                    for j in val[1:]: # iterating on column indices where val[0] < j
                        for i in range(len(sbm_df)):
                            if (i, val[0]) in sbm_df.index and (i, j) in sbm_df.index:
                                # 1 + 1 case
                                sbm_df = sbm_df.drop((i, j))
                            elif (i, val[0]) in sbm_df.index and not (i, j) in sbm_df.index:
                                # 1 + 0 case
                                # adding new row in this case
                                _sbm_df = sbm_df.reset_index()
                                _sbm_df.loc[len(sbm_df)] = [i, j, 1] # [row idx, col idx, val] 
                                sbm_df = _sbm_df.set_index(["row", "col"])
                            elif not (i, val[0]) in sbm_df.index and (i, j) in sbm_df.index:
                                # 0 + 1 case
                                sbm_df.loc[i, j] = 1 
                            else:
                                # 0 + 0 case
                                pass

            lowest_row_idx_dict = self._get_lowest_row_idx_dict(sbm_df)
            freq_of_low_dict = self._get_freq_of_low_dict(lowest_row_idx_dict)
            _counter += 1

        sbm_reduced = self._sbm_df_to_sbm_dict(sbm_df)
        return sbm_reduced

class BoundaryMatrixReducer(object):
    def __init__(self, verbose: bool=True):
        self._verbose = verbose # for debug

    def _get_lowest_row_idx(self, bm: list, column_idx: int) -> int:
        """
        Returns
        -------
        lowest_row_idx : int or None
            None if the column has only 0 
        """
        N = len(bm)
        lowest_row_idx = None
        for i in range(1, N):
            if bm[N-i][column_idx] == 0:
                continue
            else:
                lowest_row_idx = N - i
                break

        return lowest_row_idx

    def _get_freq_of_low_dict(self, boundary_matrix: list) -> dict:
        """
        Parameters
        ----------
        boundary_matrix : list
        In [3]: boundary_matrix
        Out[3]:
        [[0, 0, 0, 1, 0, 1, 0],
        [0, 0, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0]]

        Returns
        -------
        freq_of_low_dict : dict
        key : lowest row index
        value : list of column indices of boundary matrix whose lowest row index is key

        In [2]: freq_of_low_dict
        Out[2]: {1: [3], 2: [4, 5], 5: [6]}
        """
        if self._verbose:
            print("--- BoundaryMatrixReducer._get_freq_of_low_dict ---")

        lowest_row_list = [self._get_lowest_row_idx(boundary_matrix, column_idx) for column_idx in range(len(boundary_matrix))]
        freq_of_low_dict = {}

        for i, val in enumerate(lowest_row_list):
            if val is not None:
                if val in freq_of_low_dict:
                    freq_of_low_dict[val].append(i)
                else:
                    freq_of_low_dict[val] = [i]
        return freq_of_low_dict
    
    def reduce(self, boundary_matrix: list, return_copy: bool=False) -> list:
        if return_copy: # for debug
            _bm = copy.deepcopy(boundary_matrix)
        else:
            _bm = boundary_matrix

        freq_of_low_dict = self._get_freq_of_low_dict(_bm)

        _counter = 0
        while max(list(map(len, freq_of_low_dict.values()))) > 1:
            if self._verbose:
                print(f"---{_counter}---")
                print(freq_of_low_dict)

            for key, val in freq_of_low_dict.items():
                if len(val) > 1:
                    for j in val[1:]:
                        for i in range(len(_bm)):
                            _bm[i][j] = _bm[i][val[0]] + _bm[i][j] # _bm[row idx][column idx]
                            if _bm[i][j] > 1:
                                _bm[i][j] = 0

            freq_of_low_dict = self._get_freq_of_low_dict(_bm)
            _counter += 1
        
        return _bm


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Run Syntax: python persistence.py <path to filteration data>")
        sys.exit(0)

    filtration = read_filtration(sys.argv[1])
    for simplex in filtration:
        print(simplex)
