import numpy as np
import matplotlib.pyplot as plt

# Function to plot the barcode diagram
def plot_barcode(data, max_death=10):
    # Convert the input list to a NumPy array for easier slicing
    data = np.array(data)
    
    # Separate data by homology dimensions
    H0 = data[data[:, 0] == 0]  # 0D homology (connected components)
    H1 = data[data[:, 0] == 1]  # 1D homology (loops)
    H2 = data[data[:, 0] == 2]  # 2D homology (voids), if any

    # Create a plot for each homology dimension
    fig, ax = plt.subplots(figsize=(10, 6))  # Adjust size for better clarity
    
    # Set a different color for each homology group (H0, H1, etc.)
    colors = ['b', 'r', 'g']  # blue for H0, red for H1, green for H2, etc.
    labels = ['H0: Connected Components', 'H1: Loops', 'H2: Voids']
    
    # Define a vertical range for each homology group
    spacing = 5  # Amount of vertical space between groups
    h0_offset = 0
    h1_offset = len(H0) + spacing  # Start H1 after H0 with some spacing
    h2_offset = h1_offset + len(H1) + spacing  # Start H2 after H1

    # Plot each homology dimension separately, ensuring distinct vertical regions
    for i, (homology_group, offset) in enumerate(zip([H0, H1, H2], [h0_offset, h1_offset, h2_offset])):
        if len(homology_group) == 0:
            continue  # Skip if no data for that dimension
        for j, (dim, birth, death) in enumerate(homology_group):
            if death == np.inf:
                death = max_death  # Cap infinite death times at max_death
                ax.plot([np.log(birth), np.log(death)], [j + offset] * 2, lw=2, color=colors[i], linestyle='dashed')  # Dashed line for infinite persistence
            else:
                ax.plot([np.log(birth), np.log(death)], [j + offset] * 2, lw=2, color=colors[i])  # Solid line for finite persistence
    
    # Set the labels and title
    ax.set_yticks([])  # Hide y-axis labels as they're just indices
    ax.set_xlabel('Filtration Value')
    ax.set_title('Barcode Plot for Persistent Homology')

    # Create a legend
    handles = [
        plt.Line2D([0], [0], color='b', lw=2, label=labels[0]),
        plt.Line2D([0], [0], color='r', lw=2, label=labels[1]),
        plt.Line2D([0], [0], color='g', lw=2, label=labels[2]),
        plt.Line2D([0], [0], color='black', lw=2, label='Finite Persistence'),
        plt.Line2D([0], [0], color='black', lw=2, linestyle='dashed', label='Infinite Persistence'),
    ]
    ax.legend(handles=handles, loc='upper right')

    # Display the plot
    # plt.show()
    plt.savefig("./outputs/fig.png")



# Test data (list of tuples)
# test_data = [
#     (0, 0.1, 0.3), (0, 0.2, 0.5), (0, 0.15, 0.35), (0, 0.05, 0.25), (0, 0.4, 0.6),
#     (0, 0.3, np.inf), (0, 0.05, 0.2), (0, 0.25, 0.55), (0, 0.6, 0.8), (0, 0.35, 0.45),
#     (1, 0.1, 0.4), (1, 0.2, np.inf), (1, 0.3, 0.5), (1, 0.15, 0.35), (1, 0.05, 0.25),
#     (1, 0.4, np.inf), (1, 0.2, 0.45), (1, 0.05, 0.3), (1, 0.5, np.inf), (1, 0.25, 0.55),
#     (2, 0.1, np.inf), (2, 0.3, 0.6), (2, 0.2, np.inf), (2, 0.4, 0.8), (2, 0.25, np.inf),
#     (2, 0.15, 0.35), (2, 0.05, 0.2), (2, 0.5, 0.9), (2, 0.7, np.inf), (2, 0.1, 0.4),
#     (0, 0.6, 0.75), (0, 0.55, 0.7), (0, 0.4, np.inf), (0, 0.35, 0.5), (0, 0.15, 0.3),
#     (0, 0.05, 0.15), (0, 0.25, 0.6), (0, 0.05, 0.4), (0, 0.2, 0.45), (0, 0.3, 0.5),
#     (1, 0.35, 0.7), (1, 0.05, 0.15), (1, 0.2, 0.6), (1, 0.3, np.inf), (1, 0.55, 0.75),
#     (1, 0.4, np.inf), (1, 0.1, 0.5), (1, 0.15, 0.35), (1, 0.45, 0.65), (1, 0.25, 0.55)
# ]


from persistence.persistence import read_filtration
from persistence.boundary_matrix import get_sparse_boundary_matrix
from persistence.reduce_boundary_matrix import SparseBoundaryMatrixReducer

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
# sbm_col2row_reduced = sbm_reducer.reduce1(sbm_col2row)

from persistence.compute_barcode import compute_barcode
barcode_list = compute_barcode(filtration, sbm_col2row_reduced)


# Plot the barcode with the test data
plot_barcode(barcode_list, max_death=10)  # Adjust max_death if needed
