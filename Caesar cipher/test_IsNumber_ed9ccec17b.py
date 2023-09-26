# Test generated by RoostGPT for test awesome-python-ceaser-cipher using AI Type Open AI and AI Model gpt-4

import unittest

def isNumber(element):
    for i in range(0,10):
        if(int(element) == i):
            return True
    return False

class TestIsNumber(unittest.TestCase):
    def TestIsNumber_ed9ccec17b(self):
        # Test case 1: Check with a number
        self.assertTrue(isNumber(5))
        
        # Test case 2: Check with a string
        self.assertFalse(isNumber('abc'))

        # Test case 3: Check with a number in string format
        self.assertTrue(isNumber('9'))

        # Test case 4: Check with a number out of range
        self.assertFalse(isNumber(11))

        # Test case 5: Check with a negative number
        self.assertFalse(isNumber(-1))

if __name__ == '__main__':
    unittest.main()
