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
# filtration = read_filtration("./tests/testcases/filtration_1.txt")
filtration = read_filtration("./tests/testcases/filtration_2.txt")


# s = filtration[0]
# df = convert_filtration_df(filtration)

# bm = get_boundary_matrix(df)
# bm_reducer = BoundaryMatrixReducer(verbose=True)
# bm_reduced = bm_reducer.reduce(bm, return_copy=False)


from persistence.reduce_boundary_matrix import SparseBoundaryMatrixReducer
df = convert_filtration_df(filtration)
sbm = get_sparse_boundary_matrix(df)


sbm_reducer = SparseBoundaryMatrixReducer(verbose=True)
sbm_reduced = sbm_reducer.reduce(sbm)


from persistence.utils.io import save_pickle
from persistence.utils.io import load_pickle

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