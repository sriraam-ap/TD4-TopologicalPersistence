import copy

import pandas as pd
from numba import jit


class SparseBoundaryMatrixReducer(object):
    def __init__(self, verbose: bool=True):
        self._verbose = verbose # for debug

    def _sbm_df_to_sbm_dict(self, sbm_df: pd.DataFrame) -> dict:
        _sbm_df = sbm_df.reset_index()
        sbm_dict = {col: _sbm_df[col].to_list() for col in _sbm_df.columns}
        return sbm_dict
    
    def _sbm_dict_to_sbm_df(self, sbm_dict: dict) -> pd.DataFrame:
        """
        Parameters
        ----------
        In [9]: sbm_dict
        Out[9]:
        {'row': [0, 1, 1, 2, 0, 2, 3, 4, 5],
        'col': [3, 3, 4, 4, 5, 5, 6, 6, 6],
        'val': [1, 1, 1, 1, 1, 1, 1, 1, 1]}
        """
        sbm_df = pd.DataFrame(sbm_dict)
        sbm_df = sbm_df.set_index(keys=["row", "col"])
        return sbm_df

    def _get_lowest_row_idx_dict(self, sbm_df: pd.DataFrame) -> int:
        """
        Parameters
        ----------
        sbm_df : pd.DataFrame
        In [7]: sbm_df
        Out[7]:
                val
        row col
        0   3      1
        1   3      1
            4      1
        2   4      1
        ...

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
        _sbm_df_sorted = sbm_df.sort_values(["col", "row"])
        sbm = self._sbm_df_to_sbm_dict(_sbm_df_sorted)

        N = len(sbm["col"])

        for i in range(N):
            print(f"{i}/{N}")
            lowest_row_idx_dict[sbm["col"][i]] = sbm["row"][i]
            # assuming sorted on row gived specific column
            # ex.
            # row: [6, 7, 8]
            # col: [9 ,9 ,9]
            # val: [1, 1, 1]

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

        lowest_row_idx_more_than_one: list
        In [6]: lowest_row_idx_more_than_one
        Out[6]: [2]
        """
        if self._verbose:
            print("--- BoundaryMatrixReducer._get_freq_of_low_dict ---")

        freq_of_low_dict = {}
        lowest_row_idx_more_than_one = []
        for col_idx, lowest_row_idx in lowest_row_idx_dict.items():
            if not lowest_row_idx in freq_of_low_dict:
                freq_of_low_dict[lowest_row_idx] = [col_idx]
            else:
                freq_of_low_dict[lowest_row_idx].append(col_idx)
                lowest_row_idx_more_than_one.append(lowest_row_idx)

        return freq_of_low_dict, lowest_row_idx_more_than_one
    
    def reduce(self, sbm: list) -> list:
        """
        Parameters
        ----------
        sbm : list
        In [2]: sbm
        Out[2]:
        {'row': [0, 1, 1, 2, 0, 2, 3, 4, 5],
        'col': [3, 3, 4, 4, 5, 5, 6, 6, 6],
        'val': [1, 1, 1, 1, 1, 1, 1, 1, 1]}

        Example
        -------
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

        print("reduce: making col2row dict")
        col2row = {col_idx: [] for col_idx in set(sbm["col"])}
        for i, col_idx in enumerate(sbm["col"]):
            col2row[col_idx].append(sbm["row"][i])

        print("reduce: making row2col dict")
        row2col = {row_idx: [] for row_idx in set(sbm["row"])}
        for i, row_idx in enumerate(sbm["row"]):
            row2col[row_idx].append(sbm["col"][i])

        col_indices = list(col2row.keys())
        for _counter, j in enumerate(col_indices):
            print(f"reduce: {_counter}/{len(col_indices)}")

            i = lowest_row_idx_dict[j] # lowest row index doesn't change after adding j col to j+t col since it's upper triangular matrix
            col_indices_to_add = row2col[i][1:]
            print(f"number of col_indices_to_add: {len(col_indices_to_add)}")
            for col_idx_to_add in col_indices_to_add:
                nonzero_rows_at_j_col = set(col2row[j]) if j in col2row else set()
                nonzero_rows_at_col_to_add = set(col2row[col_idx_to_add]) if col_idx_to_add in col2row else set()
                xor = nonzero_rows_at_j_col ^ nonzero_rows_at_col_to_add
                new_nonzero_rows = xor - nonzero_rows_at_col_to_add

                # update col2row
                if len(xor) == 0:
                    if col_idx_to_add in col2row:
                        col2row.pop(col_idx_to_add)
                else:
                    col2row[col_idx_to_add] = list(xor)

                # update row2col
                for row_idx in new_nonzero_rows:
                    row2col[row_idx].append(col_idx_to_add)
                    row2col[row_idx] = sorted(row2col[row_idx])

        sbm_reduced = {"row": [], "col": [], "val": []}
        for col_idx, row_indices in col2row.items():
            for row_idx in row_indices:
                sbm_reduced["col"].append(col_idx)
                sbm_reduced["row"].append(row_idx)
        sbm_reduced["val"] = [1] * len(sbm_reduced["col"])

        return sbm_reduced

class BoundaryMatrixReducer(object):
    """This class is for dense format boundary matrix.
    """
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