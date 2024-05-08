import pytest
import os
from FinderZV2 import fileOperands

#Finding Files
@pytest.fixture
def setup_test_dir(tmp_path):
    # Create a temporary directory
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()

    # Create some test files
    file1 = test_dir / "testfile1.txt"
    file1.write_text("This is a test file.")

    file2 = test_dir / "testfile2.txt"
    file2.write_text("This is another test file.")

    yield test_dir


def test_findFiles_exact_search(setup_test_dir):
    # Test exact search
    results = fileOperands.findFiles("testfile1.txt", str(setup_test_dir), exactSearch=True)
    expected = [str(setup_test_dir / "testfile1.txt")]
    assert results == expected


def test_findFiles_inexact_search(setup_test_dir):
    # Test inexact search
    results = fileOperands.findFiles("testfile", str(setup_test_dir), exactSearch=False)
    expected = [str(setup_test_dir / "testfile1.txt"), str(setup_test_dir / "testfile2.txt")]
    assert set(results) == set(expected)

# Scan Files
def test_scanFilesForContent(setup_test_dir):
    # Create a file with content
    file_with_keyword = setup_test_dir / "keywordfile.txt"
    file_with_keyword.write_text("This file contains the keyword.")

    # Test scanning for content
    results = fileOperands.scanFilesForContent("keyword", str(setup_test_dir))
    expected = [str(file_with_keyword)]
    assert results == expected
