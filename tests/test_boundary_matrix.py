import pytest
from pathlib import Path

from persistence.persistence import read_filtration
from persistence.persistence import convert_filtration_df
from persistence.boundary_matrix import get_sparse_boundary_matrix


testcases_path = Path(__file__).parent / "testcases"

@pytest.fixture
def sparse_boundary_matrix_cases():
    filename = testcases_path / "filtration_1.txt"
    filtration = read_filtration(str(filename))
    _filtration_1_df = convert_filtration_df(filtration)
    expected_case_1 = {'row': [0, 1, 1, 2, 0, 2, 3, 4, 5], 'col': [3, 3, 4, 4, 5, 5, 6, 6, 6], 'val': [1, 1, 1, 1, 1, 1, 1, 1, 1]}

    filename = testcases_path / "filtration_2.txt"
    filtration = read_filtration(str(filename))
    _filtration_2_df = convert_filtration_df(filtration)
    expected_case_2 = {'row': [0, 1, 1, 2, 0, 5, 2, 5, 0, 2, 8, 7, 6], 'col': [3, 3, 4, 4, 6, 6, 7, 7, 8, 8, 9, 9, 9], 'val': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}
    
    testcases = [
                    (_filtration_1_df, expected_case_1),
                    (_filtration_2_df, expected_case_2)
                ]
    
    return testcases

def test_get_sparse_boundary_matrix(sparse_boundary_matrix_cases):
    for filtration_df, expected_case in sparse_boundary_matrix_cases:
        sbm = get_sparse_boundary_matrix(filtration_df)
        print(filtration_df)
        print(sbm)
        print(expected_case)

        for key in expected_case.keys():
            assert sbm[key] == expected_case[key]