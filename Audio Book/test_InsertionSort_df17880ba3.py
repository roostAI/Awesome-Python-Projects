import unittest
from insertion_sort import insertionSort

class TestInsertionSort(unittest.TestCase):

    def test_InsertionSort_df17880ba3(self):
        # Test case 1: Normal scenario
        arr = [12, 11, 13, 5, 6]
        insertionSort(arr)
        self.assertEqual(arr, [5, 6, 11, 12, 13])

        # Test case 2: Array already sorted
        arr = [1, 2, 3, 4, 5]
        insertionSort(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5])

        # Test case 3: Array sorted in reverse order
        arr = [5, 4, 3, 2, 1]
        insertionSort(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5])

        # Test case 4: Array with duplicate elements
        arr = [5, 5, 3, 2, 1]
        insertionSort(arr)
        self.assertEqual(arr, [1, 2, 3, 5, 5])

        # Test case 5: Array with one element
        arr = [1]
        insertionSort(arr)
        self.assertEqual(arr, [1])

        # Test case 6: Empty array
        arr = []
        insertionSort(arr)
        self.assertEqual(arr, [])

if __name__ == '__main__':
    unittest.main()
