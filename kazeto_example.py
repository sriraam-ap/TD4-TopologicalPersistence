from persistence import read_filtration
from persistence import convert_filtration_df


filtration = read_filtration("./filtrations/filtration_D.txt")
s = filtration[0]

import pandas as pd
df = convert_filtration_df(filtration)

