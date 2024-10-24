import time
from pathlib import Path

from persistence.persistence import read_filtration
from persistence.boundary_matrix import get_sparse_boundary_matrix
from persistence.reduce_boundary_matrix import SparseBoundaryMatrixReducer
from persistence.compute_barcode import compute_barcode, save_barcode

filenames = ["./filtrations/filtration_A.txt", "./filtrations/filtration_B.txt", "./filtrations/filtration_C.txt"]
timing_output_filename = "./outputs/results_of_timing.txt"
barcode_output_savedir = "./outputs/barcodes"

p = Path(barcode_output_savedir)
p.mkdir(exist_ok=True)

for filename in filenames:
    print(f"--- {filename} ---")
    start = time.time()

    # read data
    filtration = read_filtration(filename)

    # make boundary matrix
    sbm_col2row = get_sparse_boundary_matrix(filtration)
    sbm_reducer = SparseBoundaryMatrixReducer()

    # reduce boundary matrix
    sbm_col2row_reduced = sbm_reducer.reduce1(sbm_col2row)
    # sbm_col2row_reduced = sbm_reducer.reduce2(sbm_col2row)

    # compute barcode
    barcode_list = compute_barcode(filtration, sbm_col2row_reduced)
    barcode_output_filename = str(p.joinpath(f"barcode_{Path(filename).name.split('.')[0]}.txt"))
    save_barcode(barcode_list, barcode_output_filename)

    # save time
    t = time.time() - start

    output_str = f"filename: {filename}, elapsed time: {t} sec\n"
    with open(timing_output_filename, mode='a') as f:
        f.write(output_str)