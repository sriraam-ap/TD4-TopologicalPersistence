from itertools import combinations
import pandas as pd

def get_sparse_boundary_matrix(filtration: list) -> dict:
    """
    Parameters
    ----------
    filtration: list
    In [92]: filtration
    Out[92]:
    [<persistence.persistence.Simplex at 0x7f191d47a0d0>,
    <persistence.persistence.Simplex at 0x7f191da46d90>,
    ...]

    Returns
    -------
    sbm_col2row : dict
    key: nonzero column index of boundary matrix
    value: set of nonzero row indices of boundary matrix

    In [91]: sbm_col2row
    Out[91]:
    {10000: {4805, 9997},
    10001: {4807, 9999},
    10002: {4804, 9996},
    10003: {4806, 9998},
    ...}
    """
    print("--- get_sparse_boundary_matrix start ---")
    dim_list = [s.dim for s in filtration]
    val_list = [s.val for s in filtration]
    vert_list = [frozenset(s.vert) for s in filtration]
    df = pd.DataFrame({"val": val_list, "dim": dim_list, "vert": vert_list})
    df_sorted = df.sort_values(by=['val', 'dim'])
    vert2idx = {vert: i for i, vert in enumerate(df_sorted.vert.values)}
    sbm_col2row = {j: {vert2idx[frozenset(b)] for b in combinations(vert, len(vert)-1)} for j, vert in enumerate(df_sorted.vert.values) if len(vert) > 1}
    print("--- get_sparse_boundary_matrix finished ---")
    return sbm_col2row

def sparse2dense(sbm_col2row: dict) -> list:
    """
    Parameters
    ----------
    sbm_col2row : dict
    bm_dense : list
    In [29]: bm_dense
    [[0, 0, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 1, 0, 0],
    [0, 0, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0]]
    """
    N = max(sbm_col2row.keys()) + 1 # assume index of simplex starts from 0
    bm_dense = [[0 for _ in range(N)] for _ in range(N)]
    for col_idx, row_indices in sbm_col2row.items():
        for row_idx in row_indices:
            bm_dense[row_idx][col_idx] = 1
    return bm_dense

def sbm_col2row_to_row2col(sbm_col2row: dict) -> dict:
    """
    In [56]: sbm_col2row
    Out[56]: {3: {0, 1}, 4: {1, 2}, 5: {0, 2}, 6: {3, 4, 5}}

    In [55]: sbm_row2col
    Out[55]: {0: {3, 5}, 1: {3, 4}, 2: {4, 5}, 3: {6}, 4: {6}, 5: {6}}
    """
    sbm_row2col = {}
    for col_idx, row_indices in sbm_col2row.items():
        for row_index in row_indices:
            if row_index in sbm_row2col:
                sbm_row2col[row_index].add(col_idx)
            else:
                sbm_row2col[row_index] = {col_idx}

    return sbm_row2col

def sbm_col2row_to_sbm_list(sbm_col2row: dict) -> dict:
    """
    sbm_col2row

    In [2]: sbm_reduced
    Out[2]:
    {'row': [0, 1, 0, 2, 3, 4, 5],
    'col': [3, 3, 4, 4, 6, 6, 6],
    'val': [1, 1, 1, 1, 1, 1, 1]}
    """
    sbm_reduced = {"row": [], "col": [], "val": []}
    for col_idx, row_indices in sbm_col2row.items():
        for row_idx in row_indices:
            sbm_reduced["col"].append(col_idx)
            sbm_reduced["row"].append(row_idx)
    sbm_reduced["val"] = [1] * len(sbm_reduced["col"])
    return sbm_reduced