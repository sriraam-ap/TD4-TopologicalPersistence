import pandas as pd
from persistence import read_filtration
from persistence import convert_filtration_df
from persistence import get_boundary_matrix
from persistence import get_sparse_boundary_matrix
from persistence import BoundaryMatrixReducer

filtration = read_filtration("./filtrations/filtration_A.txt")
# filtration = read_filtration("./filtrations/filtration_D.txt")
# filtration = read_filtration("./tests/testcases/filtration_1.txt")
# filtration = read_filtration("./tests/testcases/filtration_2.txt")


# s = filtration[0]
# df = convert_filtration_df(filtration)

# bm = get_boundary_matrix(df)
# bm_reducer = BoundaryMatrixReducer(verbose=True)
# bm_reduced = bm_reducer.reduce(bm, return_copy=False)


from persistence import SparseBoundaryMatrixReducer
df = convert_filtration_df(filtration)
sbm = get_sparse_boundary_matrix(df)
sbm_reducer = SparseBoundaryMatrixReducer(verbose=True)
# lowest_row_idx_dict = sbm_reducer._get_lowest_row_idx_dict(pd.DataFrame(sbm))
# freq_of_low_dict = sbm_reducer._get_freq_of_low_dict(lowest_row_idx_dict)
sbm_reduced = sbm_reducer.reduce(sbm)


import pandas as pd
sbm_df = pd.DataFrame(sbm)
sbm_df = sbm_df.set_index(keys=["row", "col"])
sbm_df.reset_index().to_dict()

_sbm_df = sbm_df.reset_index()
sbm = {col: _sbm_df[col].to_list() for col in _sbm_df.columns}

sbm_df.loc[0, 3]
sbm_df.loc[1, 4]
sbm_df.loc[1, 5]

(1, 5) in sbm_df.index
(0, 3) in sbm_df.index

i = 0
j = 3
sbm_df.loc[i, j] = 0
sbm_df = sbm_df.drop((i, j))