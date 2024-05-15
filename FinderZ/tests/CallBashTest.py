import os
import unittest
from FinderZV2 import Callbash

class TestCallBash(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_dir = 'Testing-FinderZ'
        os.makedirs(cls.test_dir, exist_ok=True)

        # Create test batch file
        with open(os.path.join(cls.test_dir, 'helloworld.bat'), 'w') as f:
            f.write('@echo off\n')
            f.write('echo Hello World!\n')

    def test_callBash(self):
        directory_path = os.path.join(self.test_dir, 'helloworld.bat')
        expected_output = None
        actual_output = Callbash.runFile(directory_path)
        self.assertEqual(expected_output, actual_output)

    @classmethod
    def tearDownClass(cls):
        # Clean up the test environment
        for root, dirs, files in os.walk(cls.test_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(cls.test_dir)

if __name__ == '__main__':
    unittest.main()
