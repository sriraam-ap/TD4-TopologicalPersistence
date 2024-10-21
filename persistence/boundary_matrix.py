import pandas as pd
import swifter


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

def _make_vert_row_df(filtration_df: pd.DataFrame, dim: int) -> pd.DataFrame:
    """The output (vert_row_df) is used for get_sparse_boundary_matrix function to look up row index from vertex index.
    "row" column inthe vert_row_df is the row index of boundary matrix for the object with vertices in its index.

    In [46]: vert_row_df_dim1 = _make_vert_row_df(df, dim=1)
    In [47]: vert_row_df_dim1
    Out[47]:
                    row
    vert0 vert1
    13793 13795   14754
    13794 13795   14755
    ...
    
    In [50]: vert_row_df_dim3 = _make_vert_row_df(df, dim=3)
    In [51]: vert_row_df_dim3
    Out[51]:
                                row
    vert0 vert1 vert2 vert3
    11247 13087 14084 14087   14902
    4475  13053 13055 13079   15411
    ...
    """
    df_subset = filtration_df[filtration_df["dim"] == dim]
    df_subset = df_subset.vert.map(sorted)
    num_verts = dim + 1

    data_dict = {}
    for i in range(num_verts):
        data_dict[f"vert{i}"] = [vert[i] for _, vert in df_subset.items()]
    data_dict["row"] = df_subset.index

    vert_row_df = pd.DataFrame(data_dict)
    vert_row_df = vert_row_df.set_index(keys=list(vert_row_df.columns[:-1]))
    return vert_row_df

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

    vert_row_df_dim_0 = _make_vert_row_df(filtration_df, dim=0)
    vert_row_df_dim_1 = _make_vert_row_df(filtration_df, dim=1)
    vert_row_df_dim_2 = _make_vert_row_df(filtration_df, dim=2)
    vert_row_df_dim_3 = _make_vert_row_df(filtration_df, dim=3)

    print("--- get_boundary_matrix: updating boundary matrix ---")
    for col_idx, row in filtration_df.iterrows():
        print(f"{col_idx}/{len(filtration_df)}: get_boundary_matrix: updating boundary matrix")
        if row.dim == 0:
            continue
        elif row.dim == 1:
            for vert in row.vert:
                row_idx = int(vert_row_df_dim_0.loc[vert].row) # boundary is dim - 1, so it uses vert_row_df_dim_0 for dim=1 case.
                sbm["row"].append(row_idx)
                sbm["col"].append(col_idx)
                sbm["val"].append(1)
        elif row.dim == 2:
            vert1, vert2, vert3 = row.vert
            for (vertA, vertB) in [(vert1, vert2), (vert2, vert3), (vert1, vert3)]:
                if (vertA, vertB) in vert_row_df_dim_1.index:
                    row_idx = int(vert_row_df_dim_1.loc[vertA, vertB].row)
                    sbm["row"].append(row_idx)
                    sbm["col"].append(col_idx)
                    sbm["val"].append(1)
        elif row.dim == 3:
            vert1, vert2, vert3, vert4 = row.vert
            for (vertA, vertB, vertC) in [(vert1, vert2, vert3), (vert1, vert3, vert4), (vert2, vert3, vert4), (vert1, vert2, vert4)]:
                if (vertA, vertB, vertC) in vert_row_df_dim_2.index:
                    row_idx = int(vert_row_df_dim_2.loc[vertA, vertB, vertC].row)
                    sbm["row"].append(row_idx)
                    sbm["col"].append(col_idx)
                    sbm["val"].append(1)
        else:
            print(f"--- get_boundary_matrix: taking subset of filtration_df ---")
            vert = row.vert
            print(f"vertices : {vert}")
            df_subset = filtration_df[filtration_df["dim"] == row.dim - 1]
            print(f"len(filtration_df): {len(filtration_df)} -> {len(df_subset)}")
            df_subset = df_subset[df_subset.swifter.apply(lambda one_row: one_row["vert"].issubset(vert), axis=1)]
            print(f"len(filtration_df): {len(filtration_df)} -> {len(df_subset)}")

            print(f"--- get_boundary_matrix: adding to sbm")
            for idx in df_subset.index:
                sbm["row"].append(idx)
                sbm["col"].append(col_idx)
                sbm["val"].append(1)

    return sbm