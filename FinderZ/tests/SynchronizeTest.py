import os
import pytest
from unittest.mock import patch, MagicMock

from FinderZV2 import Synchronize, GatherInfo, \
    fileOperands  # Make sure to import the module where your Synchronize class is defined


@pytest.fixture
def backup_setup():
    return {
        "file_path": "/path/to/source/file.txt",
        "directory_path": "/path/to/source/dir",
        "sync_backup_folder_name": "backup",
        "main_dir": "/path/to/main",
        "sync_dir": "/path/to/sync",
        "sync_backup_folder_path_main": os.path.join("/path/to/main", "backup"),
        "sync_backup_folder_path_sync": os.path.join("/path/to/sync", "backup"),
        "expected_main_backup_path_file": os.path.join("/path/to/main/backup", "file.txt"),
        "expected_sync_backup_path_file": os.path.join("/path/to/sync/backup", "file.txt"),
        "expected_main_backup_path_dir": os.path.join("/path/to/main/backup", "dir"),
        "expected_sync_backup_path_dir": os.path.join("/path/to/sync/backup", "dir"),
        "file1": "hash1",
        "file2": "hash2",
        "file3": "hash3"
    }

@pytest.fixture
def file_hashes():
    return {
        "file1": "hash1",
        "file2": "hash2",
        "file3": "hash3"
    }


def test_backUpToSyncFolder_file_exists():
    # Setup
    file_path = "/path/to/source/file.txt"
    sync_backup_folder_name = "backup"
    main_dir = "/path/to/main"
    sync_dir = "/path/to/sync"

    sync_backup_folder_path_main = os.path.join(main_dir, sync_backup_folder_name)
    sync_backup_folder_path_sync = os.path.join(sync_dir, sync_backup_folder_name)
    expected_main_backup_path = os.path.join(sync_backup_folder_path_main, "file.txt")
    expected_sync_backup_path = os.path.join(sync_backup_folder_path_sync, "file.txt")

    # Mocks
    with patch('os.path.join', side_effect=os.path.join), \
            patch('os.path.isfile', return_value=True), \
            patch('os.path.isdir', return_value=False), \
            patch('os.path.exists', return_value=True), \
            patch('os.remove') as mock_remove, \
            patch('shutil.rmtree') as mock_rmtree, \
            patch.object(fileOperands, 'copyFile') as mock_copy_file:
        # Test
        Synchronize.backUpToSyncFolder(file_path, sync_backup_folder_name, main_dir, sync_dir)

        # Asserts
        mock_remove.assert_any_call(expected_main_backup_path)
        mock_remove.assert_any_call(expected_sync_backup_path)
        mock_copy_file.assert_any_call(file_path, sync_backup_folder_path_main)
        mock_copy_file.assert_any_call(file_path, sync_backup_folder_path_sync)
        assert mock_rmtree.call_count == 0  # Ensure rmtree is not called since we're testing with files, not directories


def test_backUpToSyncFolder_directory_exists():
    # Similar setup to the file exists test, but adjust return values and assertions for directory handling
    directory_path = "/path/to/source/dir"
    sync_backup_folder_name = "backup"
    main_dir = "/path/to/main"
    sync_dir = "/path/to/sync"

    sync_backup_folder_path_main = os.path.join(main_dir, sync_backup_folder_name)
    sync_backup_folder_path_sync = os.path.join(sync_dir, sync_backup_folder_name)
    expected_main_backup_path = os.path.join(sync_backup_folder_path_main, "dir")
    expected_sync_backup_path = os.path.join(sync_backup_folder_path_sync, "dir")

    # Mocks
    with patch('os.path.join', side_effect=os.path.join), \
            patch('os.path.isfile', return_value=False), \
            patch('os.path.isdir', return_value=True), \
            patch('os.path.exists', return_value=True), \
            patch('os.remove') as mock_remove, \
            patch('shutil.rmtree') as mock_rmtree, \
            patch.object(fileOperands, 'copyDir') as mock_copy_dir:
        # Test
        Synchronize.backUpToSyncFolder(directory_path, sync_backup_folder_name, main_dir, sync_dir)

        # Asserts
        mock_rmtree.assert_any_call(expected_main_backup_path)
        mock_rmtree.assert_any_call(expected_sync_backup_path)
        mock_copy_dir.assert_any_call(directory_path, sync_backup_folder_path_main)
        mock_copy_dir.assert_any_call(directory_path, sync_backup_folder_path_sync)
        assert mock_remove.call_count == 0  # Ensure remove is not called since we're testing with directories, not files


# This setup assumes that you have the `fileOperands` class correctly defined and that its methods do what they are
# supposed to do as per the provided code.
def test_backUpToSyncFolder_non_existent_source(backup_setup):
    with patch('os.path.isfile', return_value=False), \
            patch('os.path.isdir', return_value=False), \
            patch('os.path.exists', return_value=False):
        # This test assumes function should return False or None when the source does not exist
        result = Synchronize.backUpToSyncFolder(backup_setup['file_path'], backup_setup['sync_backup_folder_name'],
                                                backup_setup['main_dir'], backup_setup['sync_dir'])
        assert result is None  # or assert result is False, depending on your implementation


def test_backUpToSyncFolder_permission_error(backup_setup):
    with patch('os.path.isfile', return_value=True), \
            patch('os.path.isdir', return_value=False), \
            patch('os.path.exists', return_value=True), \
            patch('os.remove', side_effect=PermissionError("Permission denied")), \
            patch('shutil.rmtree'), \
            patch.object(fileOperands, 'copyFile') as mock_copy_file:
        with pytest.raises(PermissionError):
            Synchronize.backUpToSyncFolder(backup_setup['file_path'], backup_setup['sync_backup_folder_name'],
                                           backup_setup['main_dir'], backup_setup['sync_dir'])
        mock_copy_file.assert_not_called()  # Ensure no copy operation if removal fails
