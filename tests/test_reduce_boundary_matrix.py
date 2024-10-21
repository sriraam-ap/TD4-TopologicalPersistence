import pytest

from persistence.reduce_boundary_matrix import SparseBoundaryMatrixReducer

@pytest.fixture
def reducer_testcases():
    sbm_filtration_1 = {'row': [0, 1, 1, 2, 0, 2, 3, 4, 5], 'col': [3, 3, 4, 4, 5, 5, 6, 6, 6], 'val': [1, 1, 1, 1, 1, 1, 1, 1, 1]}
    expected_case_1 = {'row': [0, 1, 1, 2, 3, 4, 5], 'col': [3, 3, 4, 4, 6, 6, 6], 'val': [1, 1, 1, 1, 1, 1, 1]}

    sbm_filtration_2 = {'row': [0, 1, 1, 2, 0, 5, 2, 5, 0, 2, 8, 7, 6], 'col': [3, 3, 4, 4, 6, 6, 7, 7, 8, 8, 9, 9, 9], 'val': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}
    expected_case_2 = {'row': [0, 1, 1, 2, 0, 5, 8, 7, 6], 'col': [3, 3, 4, 4, 6, 6, 9, 9, 9], 'val': [1, 1, 1, 1, 1, 1, 1, 1, 1]}

    testcases = [
                    (sbm_filtration_1, expected_case_1),
                    (sbm_filtration_2, expected_case_2)
                ]
    
    return testcases

class TestSparseBoundaryMatrixReducer():
    def test_reduce(self, reducer_testcases):
        for sbm, expected_case in reducer_testcases:
            sbm_reducer = SparseBoundaryMatrixReducer(verbose=True)
            sbm_reduced = sbm_reducer.reduce(sbm)
            print("sbm: ", sbm)
            print("sbm_reduced: ", sbm_reduced)

            for key in expected_case.keys():
                assert sbm_reduced[key] == expected_case[key]