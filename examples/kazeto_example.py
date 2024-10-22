import pandas as pd

from persistence.persistence import read_filtration
from persistence.persistence import convert_filtration_df
from persistence.boundary_matrix import get_boundary_matrix
from persistence.boundary_matrix import get_sparse_boundary_matrix
from persistence.reduce_boundary_matrix import BoundaryMatrixReducer

# filtration = read_filtration("./filtrations/filtration_A.txt")
# filtration = read_filtration("./filtrations/filtration_B.txt")
# filtration = read_filtration("./filtrations/filtration_C.txt")
# filtration = read_filtration("./filtrations/filtration_D.txt")
filtration = read_filtration("./tests/testcases/filtration_1.txt")
# filtration = read_filtration("./tests/testcases/filtration_2.txt")


# s = filtration[0]
# df = convert_filtration_df(filtration)

# bm = get_boundary_matrix(df)
# bm_reducer = BoundaryMatrixReducer(verbose=True)
# bm_reduced = bm_reducer.reduce(bm, return_copy=False)


from persistence.reduce_boundary_matrix import SparseBoundaryMatrixReducer
df = convert_filtration_df(filtration)
sbm = get_sparse_boundary_matrix(df)
sbm_reducer = SparseBoundaryMatrixReducer()
sbm_reduced = sbm_reducer.reduce(sbm)



sbm_df = sbm_reducer._sbm_dict_to_sbm_df(sbm)
lowest_row_idx_dict = sbm_reducer._get_lowest_row_idx_dict(sbm_df)
freq_of_low_dict, lowest_row_idx_more_than_one = sbm_reducer._get_freq_of_low_dict(lowest_row_idx_dict)





j = lowest_row_idx_more_than_one[0]


sbm_df.loc[:, 3]

lowest_row_idx_dict
freq_of_low_dict
sbm_df


sbm2 = {col_idx: [] for col_idx in set(sbm["col"])}
for i, col_idx in enumerate(sbm["col"]):
    sbm2[col_idx].append(sbm["row"][i])

j = 6
L = sbm2[j]
i = max(L)
is_occupied = i in sbm2 # No len=0 list in sbm2, so just checking existence of i is OK
R = []

L
sbm2[i]

while len(L) > 0 and is_occupied:

from persistence.reduce_boundary_matrix import SparseBoundaryMatrixReducer
from persistence.utils.io import load_pickle
# filename = "./filtrations/filtration_D_sbm_not_reduced.pickle"
filename = "./filtrations/filtration_B_sbm_not_reduced.pickle" # reduce 12:52 - # 21:24 - 

sbm = load_pickle(filename)

sbm_reducer = SparseBoundaryMatrixReducer(verbose=True)
sbm_reduced = sbm_reducer.reduce(sbm)



from persistence.utils.io import save_pickle

# filename = "./filtrations/filtration_A_sbm.pickle"
# filename = "./filtrations/filtration_B_sbm.pickle"
filename = "./filtrations/filtration_C_sbm.pickle"
# filename = "./filtrations/filtration_D_sbm.pickle"

save_pickle(filename, sbm)

# filename = "./filtrations/filtration_A_df.pickle"
# filename = "./filtrations/filtration_B_df.pickle"
filename = "./filtrations/filtration_C_df.pickle"
# filename = "./filtrations/filtration_D_df.pickle"
save_pickle(filename, df)

# lowest_row_idx_dict = sbm_reducer._get_lowest_row_idx_dict(pd.DataFrame(sbm))
# freq_of_low_dict = sbm_reducer._get_freq_of_low_dict(lowest_row_idx_dict)
sbm_reduced = sbm_reducer.reduce(sbm)


# filtration_D, sbm took 30m