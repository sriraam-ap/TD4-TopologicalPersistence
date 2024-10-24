from persistence.persistence import read_filtration
from persistence.boundary_matrix import get_sparse_boundary_matrix
from persistence.reduce_boundary_matrix import SparseBoundaryMatrixReducer
# filtration = read_filtration("./tests/testcases/filtration_1.txt")
# filtration = read_filtration("./filtrations/filtration_D.txt")
filtration = read_filtration("./filtrations/filtration_B.txt")
# filtration = read_filtration("./filtrations/filtration_A.txt")

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

print(f"reduce1: {t1} sec")
print(f"reduce2: {t2} sec")

# filtration B reduce1 reduction 1m16s
# filtration B reduce2 kazeto reduction 15s
