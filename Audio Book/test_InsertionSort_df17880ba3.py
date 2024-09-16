import unittest
from insertion_sort import insertionSort

class TestInsertionSort(unittest.TestCase):

    def test_InsertionSort_df17880ba3(self):
        # Test case 1: Normal scenario
        arr1 = [12, 11, 13, 5, 6]
        insertionSort(arr1)
        self.assertEqual(arr1, [5, 6, 11, 12, 13], "Should sort the array in ascending order")

        # Test case 2: Array with duplicate elements
        arr2 = [12, 11, 13, 5, 6, 12]
        insertionSort(arr2)
        self.assertEqual(arr2, [5, 6, 11, 12, 12, 13], "Should handle duplicate elements")

        # Test case 3: Array with negative numbers
        arr3 = [12, -11, 13, -5, 6]
        insertionSort(arr3)
        self.assertEqual(arr3, [-11, -5, 6, 12, 13], "Should handle negative numbers")

        # Test case 4: Array with one element
        arr4 = [12]
        insertionSort(arr4)
        self.assertEqual(arr4, [12], "Should handle single element array")

        # Test case 5: Empty array
        arr5 = []
        insertionSort(arr5)
        self.assertEqual(arr5, [], "Should handle empty array")

if __name__ == '__main__':
    unittest.main()
