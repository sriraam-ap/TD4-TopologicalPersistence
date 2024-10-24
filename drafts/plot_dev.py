from persistence.persistence import read_filtration
from persistence.boundary_matrix import get_sparse_boundary_matrix
from persistence.reduce_boundary_matrix import SparseBoundaryMatrixReducer
from persistence.barcode_plotter import plot_barcode

# filename = "./tests/testcases/filtration_1.txt"
# filename = "./tests/testcases/filtration_2.txt"
# filename = "./filtrations/filtration_A.txt"
filename = "./filtrations/filtration_B.txt"
# filename = "./filtrations/filtration_C.txt"
# filename = "./filtrations/filtration_D.txt"

filtration = read_filtration(filename)
sbm_col2row = get_sparse_boundary_matrix(filtration)
sbm_reducer = SparseBoundaryMatrixReducer(verbose=False)
sbm_col2row_reduced = sbm_reducer.reduce2(sbm_col2row)

from persistence.compute_barcode import compute_barcode
barcode_list = compute_barcode(filtration, sbm_col2row_reduced)


plot_title = filename.split('/')[-1].split('.')[0]
savename = "./outputs/fig_filtration_B_2.png"
plot_barcode(barcode_list, plot_title, savename)


import pandas as pd

df = pd.DataFrame(barcode_list, columns=["dim", "birth", "death"])

df["death"] - df["birth"]

import numpy as np
import matplotlib.pyplot as plt
df_subset = df.query("dim == 0 and (death - birth) > 0.05")
plt.plot(np.log(df_subset["birth"]), np.log(df_subset["death"]))
plt.savefig("./outputs/fig_3.png")
plt.close()

import numpy as np
import matplotlib.pyplot as plt
df_subset = df.query("dim == 1 and (death - birth) >= 0.05")
plt.bar(df_subset["birth"], df_subset["death"])
plt.savefig("./outputs/fig_4.png")
plt.close()
