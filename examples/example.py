from persistence.persistence import read_filtration
from persistence.boundary_matrix import get_sparse_boundary_matrix
from persistence.reduce_boundary_matrix import SparseBoundaryMatrixReducer
# filtration = read_filtration("./tests/testcases/filtration_1.txt")
filtration = read_filtration("./filtrations/filtration_D.txt")
sbm_col2row = get_sparse_boundary_matrix(filtration)
sbm_reducer = SparseBoundaryMatrixReducer()
sbm_reduced = sbm_reducer.reduce(sbm_col2row)