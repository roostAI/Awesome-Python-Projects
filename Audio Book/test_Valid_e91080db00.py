import unittest
from sudoku import valid

class TestValid(unittest.TestCase):

    def test_Valid_e91080db00(self):
        bo = [[5,3,0,0,7,0,0,0,0],
              [6,0,0,1,9,5,0,0,0],
              [0,9,8,0,0,0,0,6,0],
              [8,0,0,0,6,0,0,0,3],
              [4,0,0,8,0,3,0,0,1],
              [7,0,0,0,2,0,0,0,6],
              [0,6,0,0,0,0,2,8,0],
              [0,0,0,4,1,9,0,0,5],
              [0,0,0,0,8,0,0,7,9]]
        self.assertTrue(valid(bo, 5, (0, 0)))
        self.assertFalse(valid(bo, 5, (1, 0)))
        self.assertRaises(IndexError, valid, bo, 5, (9, 9))
        self.assertRaises(IndexError, valid, bo, 10, (9, 9))

if __name__ == '__main__':
    unittest.main()
