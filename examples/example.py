from persistence.persistence import read_filtration
from persistence.boundary_matrix import get_sparse_boundary_matrix
from persistence.reduce_boundary_matrix import SparseBoundaryMatrixReducer

# filename = "./tests/testcases/filtration_1.txt"
filename = "./filtrations/filtration_A.txt"
# filename = "./filtrations/filtration_B.txt"
# filename = "./filtrations/filtration_C.txt"
# filename = "./filtrations/filtration_D.txt"

filtration = read_filtration(filename)
sbm_col2row = get_sparse_boundary_matrix(filtration)
sbm_reducer = SparseBoundaryMatrixReducer()
sbm_col2row_1 = sbm_col2row.copy()
sbm_col2row_2 = sbm_col2row.copy()


import time

start1 = time.time()
sbm_reduced_1 = sbm_reducer.reduce1(sbm_col2row_1)
t1 = time.time() - start1
print(f"reduce1: {t1} sec")

start2 = time.time()
sbm_reduced_2 = sbm_reducer.reduce2(sbm_col2row_2)
t2 = time.time() - start2



print(f"filename: {filename}")
print(f"reduce1: {t1} sec")
print(f"reduce2: {t2} sec")

sbm_col2row_2 == sbm_col2row_1
for key in sbm_col2row_2.keys():
    assert(sbm_col2row_2[key] == sbm_col2row_1[key])


filtration = read_filtration(filename)
sbm_col2row = get_sparse_boundary_matrix(filtration)
sbm_col2row_2 == sbm_col2row
for key in sbm_col2row_2.keys():
    assert(sbm_col2row_2[key] == sbm_col2row[key])

# filtration B reduce1 reduction 1m16s
# filtration B reduce2 kazeto reduction 15s
