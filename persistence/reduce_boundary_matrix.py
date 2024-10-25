import copy

from .boundary_matrix import sbm_col2row_to_row2col


class SparseBoundaryMatrixReducer(object):
    def __init__(self, verbose: bool=True):
        self._verbose = verbose # for debug

    def reduce1(self, sbm_col2row: dict, return_copy=True) -> dict:
        """Use reduce2 method.
        The reduce1 is just for comparing two slightly different reduction algorithm.

        We will change input and output format but now it's like below

        input
        In [3]: sbm_col2row
        Out[3]: {3: {0, 1}, 4: {1, 2}, 5: {0, 2}, 6: {3, 4, 5}}

        output
        In [2]: sbm_reduced
        Out[2]: [set(), set(), set(), {0, 1}, {1, 2}, {0, 2}, {3, 4, 5}]

        The reduce1 searches columns to add by row-wise
        """
        _sbm_col2row = copy.deepcopy(sbm_col2row) if return_copy else sbm_col2row

        sbm = [set() for _ in range(max(_sbm_col2row.keys())+1)]
        for j in _sbm_col2row.keys():
            sbm[j] = _sbm_col2row[j]

        n = len(sbm)
        previous_pivots_column = [None] * n

        for j in range(len(sbm)):
            print(f"--- reduce: {j}/{n} ---")
            j_col = sbm[j]
            while j_col:
                pivot_row_index = max(j_col)
                # print(f"j: {j}, pivot_row_index: {pivot_row_index}")

                if previous_pivots_column[pivot_row_index] is None:
                    previous_pivots_column[pivot_row_index] = j
                    break

                j_col ^= sbm[previous_pivots_column[pivot_row_index]]

        # convert format
        sbm_col2row_reduced = {}
        for col_idx, row_indices in enumerate(sbm):
            if len(row_indices) == 0:
                continue
            sbm_col2row_reduced[col_idx] = row_indices
        
        return sbm_col2row_reduced

    def reduce2(self, sbm_col2row: list, return_copy=True) -> dict:
        """
        Parameters
        ----------
        sbm_col2row : dict
        return_copy: bool
            It returns a different dict object if True.
            It copies input sbm, then update it if False.

        Example
        -------
        from persistence.persistence import read_filtration
        from persistence.boundary_matrix import get_sparse_boundary_matrix
        from persistence.reduce_boundary_matrix import SparseBoundaryMatrixReducer

        filename = "./filtrations/filtration_A.txt"

        filtration = read_filtration(filename)
        sbm_col2row = get_sparse_boundary_matrix(filtration)
        sbm_reducer = SparseBoundaryMatrixReducer()
        sbm_reduced_2 = sbm_reducer.reduce2(sbm_col2row_2)

        Notes
        -----
        The reduce2 searches columns to add by col-wise
        """
        _sbm_col2row = copy.deepcopy(sbm_col2row) if return_copy else sbm_col2row

        print("reduce: making row2col dict")
        row2col = sbm_col2row_to_row2col(_sbm_col2row)

        col_indices = list(_sbm_col2row.keys())
        for _counter, j in enumerate(col_indices):
            if self._verbose:
                print(f"reduce: {_counter}/{len(col_indices)}")

            if j in _sbm_col2row:
                i = max(_sbm_col2row[j])
            else:
                continue # In this case, j col became all zeros after some addition

            col_indices_to_add = sorted([_col_idx for _col_idx in row2col[i] if j < _col_idx])
            # print(f"number of col_indices_to_add: {len(col_indices_to_add)}")
            for col_idx_to_add in col_indices_to_add:
                if j == col_idx_to_add:
                    breakpoint()
                nonzero_rows_at_j_col = _sbm_col2row[j] if j in _sbm_col2row else set()
                nonzero_rows_at_col_to_add = _sbm_col2row[col_idx_to_add] if col_idx_to_add in _sbm_col2row else set()
                xor = nonzero_rows_at_j_col ^ nonzero_rows_at_col_to_add
                new_nonzero_rows = xor - nonzero_rows_at_col_to_add # the rows to be apdated from 0 to 1 at col_idx_to_add-th col
                new_zero_rows = nonzero_rows_at_j_col & nonzero_rows_at_col_to_add# the rows to be apdated from 1 to 0 at col_idx_to_add-th col

                if self._verbose:
                    print(f"j: {j}")
                    print(f"i (lowest row idx): {i}")
                    print(f"col_idx_to_add: {col_idx_to_add}")
                    print(f"nonzero_rows_at_j_col: {nonzero_rows_at_j_col}")
                    print(f"nonzero_rows_at_col_to_add: {nonzero_rows_at_col_to_add}")
                    print(f"xor: {xor}")
                    print(f"new_nonzero_rows: {new_nonzero_rows}")
                    print(f"new_zero_rows: {new_zero_rows}")
                    print(f"_sbm_col2row before update: {_sbm_col2row}")
                    print(f"row2col before update: {row2col}") 

                # update col2row
                if len(xor) == 0:
                    # became all zero column
                    if col_idx_to_add in _sbm_col2row:
                        _sbm_col2row.pop(col_idx_to_add)
                else:
                    _sbm_col2row[col_idx_to_add] = xor

                if self._verbose:
                    print(f"_sbm_col2row after update: {_sbm_col2row}")

                # update row2col
                for row_idx in new_zero_rows:
                    row2col[row_idx].remove(col_idx_to_add)

                for row_idx in new_nonzero_rows:
                    row2col[row_idx].add(col_idx_to_add)

                if self._verbose:
                    print(f"row2col after update: {row2col}")

        return _sbm_col2row