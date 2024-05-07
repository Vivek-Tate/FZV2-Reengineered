import unittest
from FinderZV2 import GatherInfo

class GatherInfoTest(unittest.TestCase):
    def test_get_amount_of_components(self):
        directory_path = r'D:\Sem2\SR-Test\Testing-FinderZ'
        expected_amount = (2, 3)
        actual_amount = GatherInfo.getAmountofComponentsinDir(directory_path)

        self.assertEqual(actual_amount, expected_amount, f"Test case passed")

    def test_getFileNamesinDir(self):
        directory_path = r'D:\Sem2\SR-Test\Testing-FinderZ'
        expected_filenames = ['empty.txt', 'New-test-dir', 'Now.txt', 'test dir', 'tp.txt']
        actual_filenames = GatherInfo.getAllFileNamesinDir(directory_path)

        self.assertEqual(actual_filenames, expected_filenames, f"Test case passed")

    def test_getFileLineContents(self):
        directory_path = r'D:\Sem2\SR-Test\Testing-FinderZ/tp.txt'
        expected_output = ['1\n', '2\n', '3']
        actual_output = GatherInfo.getFileLineContents(directory_path)

        self.assertEqual(actual_output, expected_output, f"Test case passed")

    def test_getFileLineAmount(self):
        directory_path = r'D:\Sem2\SR-Test\Testing-FinderZ/tp.txt'
        expected_output = 3
        actual_output = GatherInfo.getFileLineAmount(directory_path)

        self.assertEqual(actual_output, expected_output, f"Test case passed")


if __name__ == '__main__':
    unittest.main()