import pytest

from persistence.reduce_boundary_matrix import SparseBoundaryMatrixReducer

@pytest.fixture
def reducer_testcases():
    sbm_col2row_1 =  {3: {0, 1}, 4: {1, 2}, 5: {0, 2}, 6: {3, 4, 5}}
    expected_case_1 = {3: {0, 1}, 4: {0, 2}, 6: {3, 4, 5}}

    sbm_col2row_2 = {3: {0, 1}, 4: {1, 2}, 6: {2, 5}, 7: {0, 5}, 8: {0, 2}, 9: {6, 7, 8}}
    expected_case_2 =  {3: {0, 1}, 4: {0, 2}, 6: {0, 5}, 9: {6, 7, 8}}

    testcases = [
                    (sbm_col2row_1, expected_case_1),
                    (sbm_col2row_2, expected_case_2)
                ]
    
    return testcases

class TestSparseBoundaryMatrixReducer():
    def test_reduce(self, reducer_testcases):
        for sbm_col2row, expected_case in reducer_testcases:
            sbm_reducer = SparseBoundaryMatrixReducer(verbose=False)
            sbm_col2row_reduced = sbm_reducer.reduce2(sbm_col2row)
            print("sbm_col2row: ", sbm_col2row)
            print("sbm_reduced: ", sbm_col2row_reduced)
            print("expected_case: ", expected_case)

            assert sbm_col2row_reduced == expected_case