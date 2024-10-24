from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from persistence.persistence import read_filtration
from persistence.boundary_matrix import get_sparse_boundary_matrix
from persistence.reduce_boundary_matrix import SparseBoundaryMatrixReducer
from persistence.compute_barcode import compute_barcode


def plot_barcode_for_one_homology(ax, df_subset, title: str, is_logscale: bool):
    for i, row in df_subset.iterrows():
        if is_logscale:
            ax.vlines(i, np.log(row.birth), np.log(row.death))
        else:
            ax.vlines(i, row.birth, row.death)
    ax.set_title(title)

    return ax

def plot_barcode(df, savename: str, suptitle: str="", thre_to_plot: float=0.05, is_logscale: bool=False):

    n = len(df.dim.unique())
    fig = plt.figure()

    for i, dim in enumerate(df.dim.unique(), 1):
        ax = fig.add_subplot(1, n, i)
        df_subset = df.query(f"dim == {dim} and (death - birth) > {thre_to_plot}")
        df_subset = df_subset.reset_index(drop=True)
        df_non_inf_subset = df_subset[df_subset["death"] != float("inf")]

        if len(df_non_inf_subset) == 0:
            # This case, df_subset contains only inf
            val_for_inf = 10000
        else:
            val_for_inf = df_subset[df_subset["death"] != float("inf")].max() * 3

        df_subset = df_subset.replace(float("inf"), val_for_inf)
        name = f"dim{dim}.png"
        # savename = str(p.joinpath(name))
        title = f"dim: {dim}"
        ax = plot_barcode_for_one_homology(ax, df_subset, title, is_logscale)

    fig.suptitle(suptitle)
    fig.savefig(savename)
    plt.close(fig)

def sort_filtration(filtration):
    dim_list = [s.dim for s in filtration]
    val_list = [s.val for s in filtration]
    vert_list = [frozenset(s.vert) for s in filtration]
    df = pd.DataFrame({"val": val_list, "dim": dim_list, "vert": vert_list})
    df = df.sort_values(["val", "dim"])
    filtration_sorted = [ filtration[idx] for idx in df.index ]
    return filtration_sorted

# filename = "./tests/testcases/filtration_1.txt"
# filename = "./tests/testcases/filtration_2.txt"
# filename = "./filtrations/filtration_A.txt"
# filename = "./filtrations/filtration_B.txt"
# filename = "./filtrations/filtration_C.txt"
# filename = "./filtrations/filtration_D.txt"
# filename = "./filtrations/moebius.txt"
# filename = "./filtrations/torus.txt"
# filename = "./filtrations/klein_bottle.txt"
# filename = "./filtrations/projective_plane.txt"
# filenames = ["./filtrations/moebius.txt", "./filtrations/torus.txt", "./filtrations/klein_bottle.txt", "./filtrations/projective_plane.txt"]

savedir = "./outputs/barcode_Q6"
filtrations_path = "./filtrations/filtrations2"
filtrations_p = Path(filtrations_path)

for filename_p in filtrations_p.iterdir():
    filename = str(filename_p)
    print(f"filename: {filename}")
    filtration = read_filtration(filename)
    filtration = sort_filtration(filtration)

    sbm_col2row = get_sparse_boundary_matrix(filtration)
    sbm_reducer = SparseBoundaryMatrixReducer(verbose=False)
    sbm_col2row_reduced = sbm_reducer.reduce2(sbm_col2row)

    barcode_list = compute_barcode(filtration, sbm_col2row_reduced)
    df = pd.DataFrame(barcode_list, columns=["dim", "birth", "death"])

    thre_to_plot = 0.0
    is_logscale = False
    savedir_p = Path(savedir)
    savedir_p.mkdir(exist_ok=True)
    name = Path(filename).name.split(".")[0]
    savename = str(savedir_p.joinpath(f"{name}.png"))
    suptitle = name
    plot_barcode(df, savename, suptitle, thre_to_plot, is_logscale)