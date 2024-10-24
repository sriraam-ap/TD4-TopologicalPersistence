import matplotlib.pyplot as plt
import numpy as np

# Sample input data: [(dimension, birth, death)]
# input_data = [
#     (0, 0.0, float('inf')),
#     (1, 0.0, 1.2),
#     (1, 0.5, 1.8),
#     (1, 0.0, 1.5),
#     (2, 0.0, 0.9),
#     (2, 0.2, 1.2),
#     (2, 0.1, float('inf')),
# ]

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
input_data = compute_barcode(filtration, sbm_col2row_reduced)


# Function to plot barcode
def plot_barcode(input_data):
    # Sort input data by dimension (for plotting H0 at the top)
    input_data.sort(key=lambda x: x[0])

    # Extract unique dimensions from input data
    dimensions = sorted(set([dim for dim, birth, death in input_data]), reverse=True)
    
    # Set up figure and axis
    fig, ax = plt.subplots()
    
    # Colors for different dimensions
    colors = ['blue', 'green', 'red']
    
    # For each dimension, plot the corresponding bars
    for dim in dimensions:
        dim_data = [(birth, death) for d, birth, death in input_data if d == dim]
        y_base = dimensions.index(dim)  # Position based on the dimension (higher dimensions go lower on the plot)
        
        # Each homology class in this dimension gets its own y-position
        for i, (birth, death) in enumerate(dim_data):
            y = y_base - 0.1 * i  # Slightly offset each line within the dimension
            
            if death == float('inf'):
                # Represent infinite death with an arrow
                ax.plot([birth, 1], [y, y], lw=2)
                ax.arrow(1, y, 0.1, 0, head_width=0.05, head_length=0.05, color=colors[dim])
            else:
                ax.plot([birth, death], [y, y], lw=2)

    # Add labels and formatting
    ax.set_xlabel('Filtration value')
    ax.set_ylabel('Homology dimension')
    ax.set_yticks(range(len(dimensions)))
    ax.set_yticklabels([f'H{dim}' for dim in dimensions])

    # Ensure H0 is on the top and the dimensions go down from there
    ax.invert_yaxis()
    
    plt.title('Barcode Plot for Persistence Homology')
    plt.grid(True, axis='x')
    plt.show()

# Call the function to plot barcode
plot_barcode(input_data)
