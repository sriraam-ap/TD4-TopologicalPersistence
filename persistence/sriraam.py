from collections import defaultdict
import sys
from tqdm import tqdm

class Simplex:
    """Simplex representation with filtration value, dimension, and vertices."""
    def __init__(self, val, dim, vert):
        self.val = val
        self.dim = dim
        self.vert = set(vert)
        self.cached_boundary = None  # Cache for simplex boundaries

    def boundary(self):
        """Generates the boundary simplices of the current simplex (cached)."""
        if self.cached_boundary is not None:
            return self.cached_boundary
        
        boundary_simplices = []
        vert_list = list(self.vert)
        
        for i in range(len(vert_list)):
            boundary_simplex = set(vert_list[:i] + vert_list[i+1:])
            boundary_simplices.append(Simplex(self.val, self.dim - 1, boundary_simplex))
        
        self.cached_boundary = boundary_simplices  # Cache the boundary
        return boundary_simplices

    def __eq__(self, other):
        """Check equality based on vertices and dimension."""
        return self.dim == other.dim and self.vert == other.vert

    def __hash__(self):
        """Hash function based on vertices and dimension for set operations."""
        return hash((self.dim, frozenset(self.vert)))

    def __repr__(self):
        return f"Simplex(val={self.val}, dim={self.dim}, vert={sorted(self.vert)})"


def read_filtration(filename):
    """Reads the filtration from a file."""
    print(f"Reading filtration from {filename}...")
    filtration = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in tqdm(lines, desc="Loading Filtration"):
            parts = line.split()
            val = float(parts[0])
            dim = int(parts[1])
            vert = list(map(int, parts[2:]))
            filtration.append(Simplex(val, dim, vert))
    return filtration


def sort_filtration(filtration):
    """Sorts the filtration by filtration value."""
    print("Sorting the filtration based on filtration values...")
    return sorted(filtration, key=lambda s: s.val)


def boundary_matrix_sparse(filtration, dim):
    """Constructs the sparse boundary matrix for simplices of dimension 'dim'."""
    print(f"Constructing the boundary matrix for dimension {dim}...")
    simplices_dim = [s for s in filtration if s.dim == dim]
    simplices_dim_minus_1 = [s for s in filtration if s.dim == dim - 1]
    
    simplex_to_col = {simplex: i for i, simplex in enumerate(simplices_dim)}
    simplex_to_row = {simplex: i for i, simplex in enumerate(simplices_dim_minus_1)}

    # Debug: Print filtration at this dimension
    print(f"Filtration (dim {dim}):")
    #for simplex in simplices_dim:
        # print(simplex)
    
    # Sparse matrix represented as a list of non-zero entries
    sparse_matrix = defaultdict(list)

    for j, simplex in tqdm(enumerate(simplices_dim), total=len(simplices_dim), desc="Building Matrix"):
        print(f"\nProcessing Simplex: {simplex}")
        for boundary_simplex in simplex.boundary():
            #print(f"Generated boundary simplex: {boundary_simplex}")  # Debugging output
            
            # Create a Simplex object to check against simplex_to_row
            # Need to make sure to check using the same representation
            if boundary_simplex in simplex_to_row:
                row_index = simplex_to_row[boundary_simplex]
                sparse_matrix[j].append(row_index)
                #print(f"Adding boundary simplex: {boundary_simplex} to column {j}")
            #else:
                #print(f"Boundary simplex {boundary_simplex} not found in simplex_to_row.")  # Debugging output

    # Debug: Print sparse boundary matrix
    # print(f"Sparse Matrix (dim {dim}): {dict(sparse_matrix)}")
    
    return sparse_matrix, len(simplices_dim_minus_1), len(simplices_dim)


def reduce_matrix_sparse(matrix, num_rows, num_cols):
    """Reduces the sparse boundary matrix using column operations over Z2."""
    print("Reducing the boundary matrix...")
    low = [-1] * num_rows  # Track the lowest 1 in each row
    
    # Store non-zero entries of each column in a dictionary
    column_data = defaultdict(list)

    # Build the column data from the sparse matrix
    for j, rows in matrix.items():
        for row in rows:
            column_data[j].append(row)
    
    for j in tqdm(range(num_cols), desc="Performing Matrix Reduction"):  # For each column
        while True:
            pivot_row = -1
            if j in column_data and column_data[j]:
                pivot_row = column_data[j][0]  # Get the lowest row with a 1

            if pivot_row == -1:
                break

            if pivot_row < num_rows:  # Ensure we don't go out of bounds
                if low[pivot_row] != -1:
                    # Reduce column j by column low[pivot_row]
                    col_to_reduce = column_data[low[pivot_row]]
                    col_j = column_data[j]

                    # XOR the columns (Z2 addition is XOR)
                    new_col = sorted(set(col_j) ^ set(col_to_reduce))  # Symmetric difference
                    column_data[j] = new_col  # Update column j with the reduced column
                else:
                    low[pivot_row] = j
                    break
            else:
                print(f"Warning: pivot_row {pivot_row} exceeds num_rows {num_rows}.")
                break
    
    # Debug: Print low array
    print(f"Low array after reduction: {low}")

    return low


def compute_persistence_sparse(filtration):
    """Compute persistence intervals for the given filtration using sparse matrix representation."""
    max_dim = max(s.dim for s in filtration)
    persistence_pairs = []
    
    # Track simplices that correspond to features that are born but never die (infinite death time)
    inf_features = set(s for s in filtration if s.dim == 0)
    
    for dim in range(1, max_dim + 1):
        matrix, num_rows, num_cols = boundary_matrix_sparse(filtration, dim)
        low = reduce_matrix_sparse(matrix, num_rows, num_cols)
        
        for j in range(len(low)):
            if low[j] != -1:
                birth_simplex = filtration[low[j]]
                death_simplex = filtration[j]
                persistence_pairs.append((birth_simplex.val, death_simplex.val, dim))
                if birth_simplex in inf_features:
                    inf_features.remove(birth_simplex)
    
    # Add the infinite persistence for the remaining 0-dimensional features
    for simplex in inf_features:
        persistence_pairs.append((simplex.val, float('inf'), 0))
    
    # Debug: Print persistence pairs
    # print(f"Persistence pairs: {persistence_pairs}")
    
    return persistence_pairs


def write_barcode_to_file(persistence_pairs, filename):
    """Writes the persistence pairs to a file in the required format."""
    print(f"Writing persistence barcode to {filename}...")
    with open(filename, 'w') as f:
        for birth, death, dim in sorted(persistence_pairs):
            death_str = f"{death}" if death != float('inf') else "inf"
            f.write(f"{dim} {birth} {death_str}\n")


def main():
    if len(sys.argv) != 2:
        print("Usage: python sriraam.py <filtration_file>")
        sys.exit(1)

    filename = sys.argv[1]
    
    # Reading filtration
    filtration = read_filtration(filename)
    
    # Sorting filtration
    sorted_filtration = sort_filtration(filtration)
    
    # Computing persistence
    persistence_pairs = compute_persistence_sparse(sorted_filtration)
    
    # Writing the barcode
    write_barcode_to_file(persistence_pairs, 'barcode_output.txt')

    print("Persistence barcode written to 'barcode_output.txt'.")


if __name__ == "__main__":
    main()
