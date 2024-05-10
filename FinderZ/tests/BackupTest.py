import unittest
from FinderZV2 import Backup
from FinderZV2 import GatherInfo

class TestBackup(unittest.TestCase):
    def testBackup(self):
        main_dir = r"Testing-FinderZ\New-test-dir"
        backup_dir = [r"Testing-FinderZ\backup_dir"]
        backup_dir_test = r"Testing-FinderZ\backup_dir"

        Backup.backup(main_dir, backup_dir)

        main_dir_files = GatherInfo.getAllFileNamesinDir(main_dir)
        backup_dir_files = GatherInfo.getAllFileNamesinDir(backup_dir_test)

        self.assertEqual(main_dir_files, backup_dir_files, f"Test case passed")