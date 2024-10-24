from persistence.persistence import read_filtration
from persistence.boundary_matrix import get_sparse_boundary_matrix
from persistence.reduce_boundary_matrix import SparseBoundaryMatrixReducer

# filename = "./tests/testcases/filtration_1.txt"
filename = "./tests/testcases/filtration_2.txt"
# filename = "./filtrations/filtration_A.txt"
# filename = "./filtrations/filtration_B.txt"
# filename = "./filtrations/filtration_C.txt"
# filename = "./filtrations/filtration_D.txt"

filtration = read_filtration(filename)
sbm_col2row = get_sparse_boundary_matrix(filtration)
sbm_reducer = SparseBoundaryMatrixReducer(verbose=True)
sbm_col2row_reduced = sbm_reducer.reduce2(sbm_col2row)
# sbm_col2row_reduced = sbm_reducer.reduce1(sbm_col2row)





from persistence.boundary_matrix import sparse2dense
sparse2dense(sbm_col2row)

sparse2dense(sbm_col2row_reduced)


from persistence.compute_barcode import compute_barcode
barcode_list = compute_barcode(filtration, sbm_col2row_reduced)

output_filename = "./outputs/barcode.txt"

from pathlib import Path

barcode_output_savedir = "./outputs/barcodes"







####

import pandas as pd

from persistence.persistence import read_filtration
from persistence.boundary_matrix import get_sparse_boundary_matrix


# filtration = read_filtration("./filtrations/filtration_A.txt")
filtration = read_filtration("./filtrations/filtration_B.txt")
# filtration = read_filtration("./filtrations/filtration_C.txt")
# filtration = read_filtration("./filtrations/filtration_D.txt")
# filtration = read_filtration("./tests/testcases/filtration_1.txt")
# filtration = read_filtration("./tests/testcases/filtration_2.txt")
# filtration = read_filtration("./filtrations/filtration_on_TD4_homepage.txt")

# s = filtration[0]
df = convert_filtration_df(filtration)


# bm = get_boundary_matrix(df)
# _bm = bm.copy()
# bm_reducer = BoundaryMatrixReducer(verbose=True)
# bm_reduced = bm_reducer.reduce(bm, return_copy=False)


from persistence.persistence import read_filtration
from persistence.boundary_matrix import get_sparse_boundary_matrix
from persistence.boundary_matrix import sbm_col2row_to_row2col, sbm_col2row_to_sbm_list
from persistence.reduce_boundary_matrix import SparseBoundaryMatrixReducer
filtration = read_filtration("./filtrations/filtration_D.txt")
# filtration = read_filtration("./tests/testcases/filtration_1.txt")
sbm_col2row = get_sparse_boundary_matrix(filtration)
# row2col = sbm_col2row_to_row2col(sbm_col2row)
# sbm_reducer = SparseBoundaryMatrixReducer()
# sbm_col2row_reduced = sbm_reducer.reduce(sbm_col2row)
# sbm_reduced = sbm_col2row_to_sbm_list(sbm_col2row_reduced)

# D: get bm 36s, 33s

sbm = [set() for _ in range(len(filtration))]
for j in sbm_col2row.keys():
    sbm[j] = sbm_col2row[j]
del sbm_col2row


sbm_col2row[10994]
sbm[10994]

# 
# list ver
# filtration_D.txt
# 1800000/2716431 8m31s
# 2158038/2716431 15m00s
# 2159882/2716431 18m00s
# 2161271/2716431 21m00s
# 2164428/2716431 28m00

n = len(sbm)
previous_pivots_column = [None] * n

for j in range(len(sbm)):
    print(f"{j}/{n}")
    j_col = sbm[j]
    while j_col:
        pivot_row_index = max(j_col)
        # print(f"j: {j}, pivot_row_index: {pivot_row_index}")

        if previous_pivots_column[pivot_row_index] is None:
            previous_pivots_column[pivot_row_index] = j
            break

        j_col = j_col ^ sbm[previous_pivots_column[pivot_row_index]]
        



        

{{row_idx:  for row_idx in row_indices} for col_idx, row_indices in sbm_col2row.items()}




filtration



sbm_df = sbm_reducer._sbm_dict_to_sbm_df(sbm)
lowest_row_idx_dict = sbm_reducer._get_lowest_row_idx_dict(sbm_df)

print("reduce: making col2row dict")
col2row = {col_idx: [] for col_idx in set(sbm["col"])}
for i, col_idx in enumerate(sbm["col"]):
    col2row[col_idx].append(sbm["row"][i])

print("reduce: making row2col dict")
row2col = {row_idx: [] for row_idx in set(sbm["row"])}
for i, row_idx in enumerate(sbm["row"]):
    row2col[row_idx].append(sbm["col"][i])

# check row2col
for key, val in row2col.items():
    if len(val) != len(set(val)):
        print(f"{key} is wrong")

# check sbm
for row, col in zip(sbm["row"], sbm["col"]):
    if row > col:
        print(f"row, col: {row}, {col}")

col_indices = list(col2row.keys())
# max(col_indices) # 108160

_counter = 0
j = 3727
print(f"reduce: {_counter}/{len(col_indices)}")

i = lowest_row_idx_dict[j] # lowest row index doesn't change after adding j col to j+t col since it's upper triangular matrix
col_indices_to_add = row2col[i][1:]
print(f"number of col_indices_to_add: {len(col_indices_to_add)}")
col_idx_to_add = col_indices_to_add[0]

nonzero_rows_at_j_col = set(col2row[j]) if j in col2row else set()
nonzero_rows_at_col_to_add = set(col2row[col_idx_to_add]) if col_idx_to_add in col2row else set()
xor = nonzero_rows_at_j_col ^ nonzero_rows_at_col_to_add
new_nonzero_rows = xor - nonzero_rows_at_col_to_add

# update col2row
if len(xor) == 0:
    if col_idx_to_add in col2row:
        col2row.pop(col_idx_to_add)
else:
    col2row[col_idx_to_add] = sorted(list(xor))

# update row2col
for row_idx in new_nonzero_rows:
    row2col[row_idx].append(col_idx_to_add)
    row2col[row_idx] = sorted(row2col[row_idx])



# number of non-zero value
len(sbm["col"]) # 158148
# reduce: 73441/85060
# number of col_indices_to_add: 123189
# reduce: 74159/85060
# number of col_indices_to_add: 277006

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


sbm2[i]

while len(L) > 0 and is_occupied:

from persistence.reduce_boundary_matrix import SparseBoundaryMatrixReducer
from persistence.utils.io import load_pickle
# filename = "./filtrations/filtration_D_sbm_not_reduced.pickle"
filename = "./filtrations/filtration_B_sbm_not_reduced.pickle" # reduce 12:52 - # 21:24 - 

sbm = load_pickle(filename)

sbm_reducer = SparseBoundaryMatrixReducer(verbose=True)
sbm_reduced = sbm_reducer.reduce(sbm)

# reduce: 65294/85060
# number of col_indices_to_add: 58488


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