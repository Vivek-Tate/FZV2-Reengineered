import os
import unittest
from FinderZV2 import callBash

class TestCallBash(unittest.TestCase):
    def test_callBash(self):
        directory_path = r"Testing-FinderZ\helloworld.bat"
        expected_output = None
        actual_output = callBash.runFile(directory_path)

        self.assertEqual(expected_output, actual_output, f"Test case passed")