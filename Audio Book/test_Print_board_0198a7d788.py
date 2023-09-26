import unittest
from io import StringIO
import sys
from sudoku import print_board

class TestPrintBoard(unittest.TestCase):

    def test_Print_board_0198a7d788(self):
        # Test case 1: Testing with a 3x3 board
        board1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        expected_output1 = '1 2 3\n- - - - - - - - - - - - -\n4 5 6\n- - - - - - - - - - - - -\n7 8 9\n'
        
        # Redirect stdout to a buffer
        stdout = sys.stdout
        sys.stdout = StringIO()

        # Call function and get its output
        print_board(board1)
        output1 = sys.stdout.getvalue()

        # Test if the function output is as expected
        self.assertEqual(output1, expected_output1)

        # Restore stdout
        sys.stdout = stdout

        # Test case 2: Testing with an empty board
        board2 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        expected_output2 = '0 0 0\n- - - - - - - - - - - - -\n0 0 0\n- - - - - - - - - - - - -\n0 0 0\n'

        # Redirect stdout to a buffer
        stdout = sys.stdout
        sys.stdout = StringIO()

        # Call function and get its output
        print_board(board2)
        output2 = sys.stdout.getvalue()

        # Test if the function output is as expected
        self.assertEqual(output2, expected_output2)

        # Restore stdout
        sys.stdout = stdout

if __name__ == '__main__':
    unittest.main()
