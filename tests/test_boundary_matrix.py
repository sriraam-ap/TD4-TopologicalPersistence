import pytest
from pathlib import Path

from persistence.persistence import read_filtration
from persistence.boundary_matrix import get_sparse_boundary_matrix


testcases_path = Path(__file__).parent / "testcases"

@pytest.fixture
def sparse_boundary_matrix_cases():
    filename = testcases_path / "filtration_1.txt"
    filtration_1 = read_filtration(str(filename))
    expected_case_1 = {3: {0, 1}, 4: {1, 2}, 5: {0, 2}, 6: {3, 4, 5}}

    filename = testcases_path / "filtration_2.txt"
    filtration_2 = read_filtration(str(filename))
    expected_case_2 = {3: {0, 1}, 4: {1, 2}, 6: {2, 5}, 7: {0, 5}, 8: {0, 2}, 9: {6, 7, 8}}
    
    testcases = [
                    (filtration_1, expected_case_1),
                    (filtration_2, expected_case_2)
                ]
    
    return testcases

def test_get_sparse_boundary_matrix(sparse_boundary_matrix_cases):
    for filtration, expected_case in sparse_boundary_matrix_cases:
        sbm_col2row = get_sparse_boundary_matrix(filtration)
        print(sbm_col2row)
        print(expected_case)

        for key in sbm_col2row.keys():
            assert sbm_col2row[key] == expected_case[key]