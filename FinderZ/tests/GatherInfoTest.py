import unittest
from FinderZV2 import GatherInfo

class GatherInfoTest(unittest.TestCase):
    def test_get_amount_of_components(self):
        directory_path = r'D:\Sem2\SR-Test\Testing-FinderZ'
        expected_amount = (2, 4)
        actual_amount = GatherInfo.getAmountofComponentsinDir(directory_path)

        self.assertEqual(expected_amount, actual_amount, f"Test case passed")

    def test_getFileNamesinDir(self):
        directory_path = r'D:\Sem2\SR-Test\Testing-FinderZ'
        expected_filenames = ['backup_dir', 'empty.txt', 'helloworld.bat', 'New-test-dir', 'Now.txt', 'tp.txt']
        actual_filenames = GatherInfo.getAllFileNamesinDir(directory_path)

        self.assertEqual(expected_filenames, actual_filenames, f"Test case passed")

    def test_getFileLineContents(self):
        directory_path = r'D:\Sem2\SR-Test\Testing-FinderZ/tp.txt'
        expected_output = ['1\n', '2\n', '3']
        actual_output = GatherInfo.getFileLineContents(directory_path)

        self.assertEqual(expected_output, actual_output, f"Test case passed")

    def test_getFileLineAmount(self):
        directory_path = r'D:\Sem2\SR-Test\Testing-FinderZ/tp.txt'
        expected_output = 3
        actual_output = GatherInfo.getFileLineAmount(directory_path)

        self.assertEqual(expected_output, actual_output, f"Test case passed")


if __name__ == '__main__':
    unittest.main()