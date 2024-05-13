import unittest
from FinderZV2 import GatherInfo

class GatherInfoTest(unittest.TestCase):
    def test_get_amount_of_components(self):
        directory_path = r'Testing-FinderZ'
        expected_amount = (2, 4)
        actual_amount = GatherInfo.getAmountofComponentsinDir(directory_path)

        self.assertEqual(expected_amount, actual_amount)

    def test_getFileNamesinDir(self):
        directory_path = r'Testing-FinderZ'
        expected_filenames = ['backup_dir', 'empty.txt', 'helloworld.bat', 'New-test-dir', 'Now.txt', 'tp.txt']
        actual_filenames = GatherInfo.getAllFileNamesinDir(directory_path)

        self.assertEqual(expected_filenames, actual_filenames)

    def test_getFileLineContents(self):
        directory_path = r'Testing-FinderZ/tp.txt'
        expected_output = ['1\n', '2\n', '3']
        actual_output = GatherInfo.getFileLineContents(directory_path)

        self.assertEqual(expected_output, actual_output)

    def test_getFileLineAmount(self):
        directory_path = r'Testing-FinderZ/tp.txt'
        expected_output = 3
        actual_output = GatherInfo.getFileLineAmount(directory_path)

        self.assertEqual(expected_output, actual_output)

    def test_isEmptyDir(self):
        directory_path = r'Testing-FinderZ'
        actual_output = GatherInfo.isEmptyDir(directory_path)
        print(actual_output)

    def test_computeHash(self):
        directory_path = r'Testing-FinderZ/Now.txt'
        actual_output = GatherInfo.computeHash(directory_path)
        print(actual_output)

    def test_isOneInCommon(self):
        list1 = 'tp.txt'
        list2 = 'Now.txt'
        actual_output = GatherInfo.isOneInCommon(list1, list2)
        print(actual_output)

    def test_readDir(self):
        directory_path = r'Testing-FinderZ'
        directories, files = GatherInfo.readDir(directory_path)
        print(files, directories)

    def test_getTotalInfo(self):
        directory_path = r'Testing-FinderZ/tp.txt'
        actual_file = GatherInfo.getTotalInfo(directory_path, 'int', recursive=True)
        print(actual_file)

    def test_compareFiles(self):
        file1 = r'Testing-FinderZ/Now.txt'
        file2 = r'Testing-FinderZ/tp.txt'
        diff_lines = GatherInfo.compareFiles(file1, file2)
        print(diff_lines)


if __name__ == '__main__':
    unittest.main()