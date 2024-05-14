import os
import unittest
from FinderZV2 import Backup
from FinderZV2 import GatherInfo

class TestBackup(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_dir = 'Testing-FinderZ'
        os.makedirs(cls.test_dir, exist_ok=True)

        # Create main directory and files
        cls.main_dir = os.path.join(cls.test_dir, 'New-test-dir')
        os.makedirs(cls.main_dir, exist_ok=True)
        with open(os.path.join(cls.main_dir, 'file1.txt'), 'w') as f:
            f.write('Content of file1.')
        with open(os.path.join(cls.main_dir, 'file2.txt'), 'w') as f:
            f.write('Content of file2.')

        # Create backup directory
        cls.backup_dir = os.path.join(cls.test_dir, 'backup_dir')
        os.makedirs(cls.backup_dir, exist_ok=True)

    def testBackup(self):
        backup_dirs = [self.backup_dir]

        Backup.backup(self.main_dir, backup_dirs)

        main_dir_files = GatherInfo.getAllFileNamesinDir(self.main_dir)
        backup_dir_files = GatherInfo.getAllFileNamesinDir(self.backup_dir)

        main_dir_files.sort()
        backup_dir_files.sort()

        self.assertEqual(main_dir_files, backup_dir_files)

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
