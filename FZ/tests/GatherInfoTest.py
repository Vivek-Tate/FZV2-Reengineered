import unittest
import os
from FinderZV2 import GatherInfo

class GatherInfoTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_dir = 'Testing-FinderZ'
        os.makedirs(cls.test_dir, exist_ok=True)

        # Create test files and directories
        with open(os.path.join(cls.test_dir, 'empty.txt'), 'w') as f:
            pass
        os.makedirs(os.path.join(cls.test_dir, 'New-test-dir'), exist_ok=True)
        with open(os.path.join(cls.test_dir, 'tp.txt'), 'w') as f:
            f.write('1\n2\n3')
        os.makedirs(os.path.join(cls.test_dir, 'backup_dir'), exist_ok=True)
        with open(os.path.join(cls.test_dir, 'Now.txt'), 'w') as f:
            f.write('This is Now.txt file.')
        with open(os.path.join(cls.test_dir, 'helloworld.bat'), 'w') as f:
            f.write('echo Hello World!')

    def test_get_amount_of_components(self):
        expected_amount = (2, 4)
        actual_amount = GatherInfo.getAmountofComponentsinDir(self.test_dir)
        self.assertEqual(expected_amount, actual_amount)

    def test_getFileNamesinDir(self):
        expected_filenames = ['backup_dir', 'empty.txt', 'helloworld.bat', 'New-test-dir', 'Now.txt', 'tp.txt']
        actual_filenames = GatherInfo.getAllFileNamesinDir(self.test_dir)
        expected_filenames.sort()
        actual_filenames.sort()
        self.assertEqual(expected_filenames, actual_filenames)

    def test_getFileLineContents(self):
        file_path = os.path.join(self.test_dir, 'tp.txt')
        expected_output = ['1\n', '2\n', '3']
        actual_output = GatherInfo.getFileLineContents(file_path)
        self.assertEqual(expected_output, actual_output)

    def test_getFileLineAmount(self):
        file_path = os.path.join(self.test_dir, 'tp.txt')
        expected_output = 3
        actual_output = GatherInfo.getFileLineAmount(file_path)
        self.assertEqual(expected_output, actual_output)

    def test_isEmptyDir(self):
        directory_path = self.test_dir
        actual_output = GatherInfo.isEmptyDir(directory_path)
        print(actual_output)

    def test_computeHash(self):
        file_path = os.path.join(self.test_dir, 'Now.txt')
        actual_output = GatherInfo.computeHash(file_path)
        print(actual_output)

    def test_isOneInCommon(self):
        list1 = ['tp.txt']
        list2 = ['Now.txt']
        actual_output = GatherInfo.isOneInCommon(list1, list2)
        print(actual_output)

    def test_readDir(self):
        directories, files = GatherInfo.readDir(self.test_dir)
        print(files, directories)

    def test_getTotalInfo(self):
        file_path = os.path.join(self.test_dir, 'tp.txt')
        actual_file = GatherInfo.getTotalInfo(file_path, 'int', recursive=True)
        print(actual_file)

    def test_compareFiles(self):
        file1 = os.path.join(self.test_dir, 'Now.txt')
        file2 = os.path.join(self.test_dir, 'tp.txt')
        diff_lines = GatherInfo.compareFiles(file1, file2)
        print(diff_lines)

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
