import copy

import pandas as pd

from .boundary_matrix import sbm_col2row_to_row2col


class SparseBoundaryMatrixReducer(object):
    def __init__(self, verbose: bool=True):
        self._verbose = verbose # for debug
    
    def reduce(self, sbm_col2row: list, return_copy=True) -> dict:
        """
        Parameters
        ----------
        sbm_col2row : dict
        return_copy: bool
            It returns a different dict object if True.
            It copies input sbm, then update it if False.

        Example
        -------

        """
        _sbm_col2row = sbm_col2row.copy() if return_copy else sbm_col2row

        print("reduce: making row2col dict")
        row2col = sbm_col2row_to_row2col(_sbm_col2row)

        col_indices = list(_sbm_col2row.keys())
        for _counter, j in enumerate(col_indices):
            print(f"reduce: {_counter}/{len(col_indices)}")

            if j in _sbm_col2row:
                i = max(_sbm_col2row[j])
            else:
                continue # In this case, j col became all zeros after some addition

            col_indices_to_add = [_col_idx for _col_idx in row2col[i] if j < _col_idx]
            col_indices_to_add = list(row2col[i])[1:]
            print(f"number of col_indices_to_add: {len(col_indices_to_add)}")
            for col_idx_to_add in col_indices_to_add:
                nonzero_rows_at_j_col = _sbm_col2row[j] if j in _sbm_col2row else set()
                nonzero_rows_at_col_to_add = _sbm_col2row[col_idx_to_add] if col_idx_to_add in _sbm_col2row else set()
                xor = nonzero_rows_at_j_col ^ nonzero_rows_at_col_to_add
                new_nonzero_rows = xor - nonzero_rows_at_col_to_add

                # update col2row
                if len(xor) == 0:
                    if col_idx_to_add in _sbm_col2row:
                        _sbm_col2row.pop(col_idx_to_add)
                else:
                    _sbm_col2row[col_idx_to_add] = xor

                # update row2col
                for row_idx in new_nonzero_rows:
                    if col_idx_to_add in row2col[row_idx]:
                        row2col[row_idx].remove(col_idx_to_add)
                    else:
                        row2col[row_idx].add(col_idx_to_add)

        return _sbm_col2row