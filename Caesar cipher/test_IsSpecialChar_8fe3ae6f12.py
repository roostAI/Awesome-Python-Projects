# Test generated by RoostGPT for test awesome-python-ceaser-cipher using AI Type Open AI and AI Model gpt-4

import unittest
from cipher import isSpecialChar

class TestSpecialChar(unittest.TestCase):

    def test_isSpecialChar_True(self):
        self.assertEqual(isSpecialChar('!'), True)

    def test_isSpecialChar_False(self):
        self.assertEqual(isSpecialChar('a'), False)

    def test_isSpecialChar_Empty(self):
        self.assertEqual(isSpecialChar(''), False)

if __name__ == '__main__':
    unittest.main()
