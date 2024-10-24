import time
from persistence.persistence import read_filtration
from persistence.boundary_matrix import get_sparse_boundary_matrix
from persistence.reduce_boundary_matrix import SparseBoundaryMatrixReducer

filenames = ["./filtrations/filtration_A.txt", "./filtrations/filtration_B.txt", "./filtrations/filtration_C.txt"]
timing_output_filename = "./outputs/results_of_timing.txt"

for filename in filenames:
    filtration = read_filtration(filename)
    sbm_col2row = get_sparse_boundary_matrix(filtration)
    sbm_reducer = SparseBoundaryMatrixReducer()

    start = time.time()
    sbm_reduced_2 = sbm_reducer.reduce2(sbm_col2row)
    t = time.time() - start

    output_str = f"filename: {filename}, elapsed time: {t} sec\n"

    with open(timing_output_filename, mode='a') as f:
        f.write(output_str)