from persistence import read_filtration
from persistence import convert_filtration_df
from persistence import get_boundary_matrix



# filtration = read_filtration("./filtrations/filtration_D.txt")
filtration = read_filtration("./tests/testcases/filtration_1.txt")

s = filtration[0]

import pandas as pd
df = convert_filtration_df(filtration)
bm = get_boundary_matrix(df)