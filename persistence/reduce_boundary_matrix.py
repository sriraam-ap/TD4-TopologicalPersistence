import copy

import pandas as pd


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

            for _counter, (key, val) in enumerate(freq_of_low_dict.items()):
                print(f"{_counter}/{len(freq_of_low_dict)}")
                if len(val) > 1:
                    for j in val[1:]: # iterating on column indices where val[0] < j
                        for i in range(0, j): # Since boundary matrix is upper triangular matrix, rows after j are 0.
                            print(f"i={i}/{j}, j={j}/{val[1:]}")
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