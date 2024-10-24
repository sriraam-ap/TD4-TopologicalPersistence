

def compute_barcode(filtration, sbm_col2row_reduced: dict, verbose: bool=False) -> list:
    """
    Parameters
    ----------
    filtration : list
    In [7]: filtration
    Out[7]:
    [<persistence.persistence.Simplex at 0x7fc13c329a50>,
    <persistence.persistence.Simplex at 0x7fc144ec4910>,
    ...

    sbm_col2row_reduced : dict
    In [5]: sbm_col2row_reduced
    Out[5]: {3: {0, 1}, 4: {1, 2}, 6: {2, 5}, 9: {6, 7, 8}}

    Returns
    -------
    barcode_list : list
    In [6]: barcode_list
    Out[6]:
    [(0, 0.0, inf),
    (0, 0.0, 1.0),
    (0, 0.0, 1.0),
    (0, 2.0, 3.0),
    (1, 3.0, inf),
    (1, 4.0, 5.0)]
    """
    # preparetion
    pivot_row2col = {}
    pivots_set = set()
    for col_idx in sbm_col2row_reduced.keys():
        lowest_row_idx = max(sbm_col2row_reduced[col_idx])
        pivot_row2col[lowest_row_idx] = col_idx
        pivots_set |= set([lowest_row_idx, col_idx])

    barcode_list = []
    simplex_indices = set(range(len(filtration)))

    # compute barcode
    _counter = 0
    while simplex_indices:
        if verbose:
            print(f"{_counter}: simplex_indices {simplex_indices}")

        s_idx = simplex_indices.pop()
        birth = filtration[s_idx].val
        dim = filtration[s_idx].dim

        if verbose:
            print(f"s_idx: {s_idx}")

        if s_idx in pivots_set:
            if not s_idx in pivot_row2col :
                breakpoint()

            death = filtration[pivot_row2col[s_idx]].val

            if verbose:
                print("pivot_row2col[s_idx]: ", pivot_row2col[s_idx])

            simplex_indices.remove(pivot_row2col[s_idx])
        else:
            death = float('inf')

        barcode_list.append((dim, birth, death))

        if verbose:
            print(f"barcode: {(dim, birth, death)}")
            print(f"simplex_indices at the end: {simplex_indices}")

        _counter += 1

    return barcode_list

def save_barcode(barcode_list, output_filename) -> None:
    """
    Parameters
    ----------
    In [12]: barcode_list
    Out[12]:
    [(0, 0.0, inf),
    (0, 0.0, 1.0),
    (0, 0.0, 1.0),
    (0, 2.0, 3.0),
    (1, 3.0, inf),
    (1, 4.0, 5.0)]

    In [13]: output_filename
    Out[13]: './outputs/barcode.txt'
    """
    barcode_str_list = [f"{b[0]} {b[1]} {b[2]}\n" for b in barcode_list]
    with open(output_filename, mode='w', encoding='utf-8') as f:
        f.writelines(barcode_str_list)