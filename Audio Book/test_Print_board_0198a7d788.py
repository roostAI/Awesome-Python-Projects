import unittest
from sudoku import print_board

class TestPrintBoard(unittest.TestCase):

    def test_Print_board_0198a7d788(self):
        # Test case 1: Check if function handles empty board correctly
        empty_board = [[0]*9]*9
        try:
            print_board(empty_board)
            print("Test case 1 passed")
        except Exception as e:
            self.fail(f"Test case 1 failed: {e}")

        # Test case 2: Check if function handles filled board correctly
        filled_board = [[1, 2, 3, 4, 5, 6, 7, 8, 9] for _ in range(9)]
        try:
            print_board(filled_board)
            print("Test case 2 passed")
        except Exception as e:
            self.fail(f"Test case 2 failed: {e}")

        # Test case 3: Check if function handles invalid board correctly
        invalid_board = [[1, 2, 3, 4, 5, 6, 7, 8] for _ in range(9)]  # one column missing
        try:
            print_board(invalid_board)
            self.fail("Test case 3 failed: No exception raised for invalid board")
        except Exception as e:
            print("Test case 3 passed")

if __name__ == '__main__':
    unittest.main()
