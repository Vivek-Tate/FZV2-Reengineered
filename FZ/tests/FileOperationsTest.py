import pytest
import os
from FinderZV2 import FileOperands

# Finding Files
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
    results = FileOperands.findFiles("testfile1.txt", str(setup_test_dir), exactSearch=True)
    expected = [str(setup_test_dir / "testfile1.txt")]
    assert results == expected


def test_findFiles_inexact_search(setup_test_dir):
    # Test inexact search
    results = FileOperands.findFiles("testfile", str(setup_test_dir), exactSearch=False)
    expected = [str(setup_test_dir / "testfile1.txt"), str(setup_test_dir / "testfile2.txt")]
    assert set(results) == set(expected)

# Scan Files
def test_scanFilesForContent(setup_test_dir):
    # Create a file with content
    file_with_keyword = setup_test_dir / "keywordfile.txt"
    file_with_keyword.write_text("This file contains the keyword.")

    # Test scanning for content
    results = FileOperands.scanFilesForContent("keyword", str(setup_test_dir))
    expected = [str(file_with_keyword)]
    assert results == expected

# Create Files
def test_createFiles(setup_test_dir):
    # Create files
    FileOperands.createFiles(3, "testcreatefile", ".txt", str(setup_test_dir))

    # Verify that the files were created
    created_files = [f for f in os.listdir(setup_test_dir) if f.startswith("testcreatefile") and f.endswith(".txt")]
    assert len(created_files) == 3

# Find and Replace Files
def test_findAndReplaceInFiles(setup_test_dir):
    # Create a file with content
    file_path = setup_test_dir / "replacefile.txt"
    file_path.write_text("This line contains a keyword.")

    # Perform the find and replace
    FileOperands.findAndReplaceInFiles("keyword", "replacement", str(setup_test_dir))

    # Check that the replacement was made
    content = file_path.read_text()
    assert "replacement" in content
    assert "keyword" not in content

# Merge Class Folders
def test_mergeClassFolders(setup_test_dir, tmp_path):
    # Create class folders with files
    class1 = setup_test_dir / "class1"
    class1.mkdir()
    (class1 / "file1.txt").write_text("Class 1 File 1")

    class2 = setup_test_dir / "class2"
    class2.mkdir()
    (class2 / "file2.txt").write_text("Class 2 File 2")

    merge_destination = tmp_path / "merged"
    merge_destination.mkdir()

    # Merge the folders
    FileOperands.mergeClassFolders(str(setup_test_dir), str(merge_destination))

    # Verify the merge
    assert (merge_destination / "file1.txt").exists()
    assert (merge_destination / "file2.txt").exists()

# XOR Encryption and Decryption
def test_xor_encrypt_decrypt_file(setup_test_dir):
    # Create a file to encrypt
    file_path = setup_test_dir / "encryptfile.txt"
    file_path.write_text("This is a secret message.")

    # Encrypt the file
    FileOperands.xor_encrypt_file(str(file_path), "key")

    # Verify encryption
    encrypted_path = str(file_path) + ".enc"
    assert os.path.exists(encrypted_path)

    # Decrypt the file
    FileOperands.xor_decrypt_file(encrypted_path, "key")

    # Verify decryption
    decrypted_path = setup_test_dir / "encryptfile.txt"
    content = decrypted_path.read_text()
    assert content == "This is a secret message."

# Calculate File and Directory Size
def test_calculateFileSize(setup_test_dir):
    # Create a file
    file_path = setup_test_dir / "sizefile.txt"
    file_path.write_text("This is a test file with some content.")

    # Calculate file size
    size = FileOperands.calculateFileSize(str(file_path))

    # Verify the file size
    assert size == os.path.getsize(str(file_path))

def test_calculateDirectorySize(setup_test_dir):
    # Calculate directory size
    size = FileOperands.calculateDirectorySize(str(setup_test_dir))

    # Verify the directory size
    expected_size = sum(os.path.getsize(str(f)) for f in setup_test_dir.rglob('*') if f.is_file())
    assert size == expected_size


# Compress and Decompress Files
def test_compress_decompress_files(setup_test_dir, tmp_path):
    # Create some test files
    file1 = setup_test_dir / "file1.txt"
    file1.write_text("File 1 content.")

    file2 = setup_test_dir / "file2.txt"
    file2.write_text("File 2 content.")

    # Compress the files
    zip_path = tmp_path / "test.zip"
    FileOperands.compressFiles([str(file1), str(file2)], str(zip_path))

    # Verify the zip file was created
    assert os.path.exists(str(zip_path))

    # Decompress the files
    extract_path = tmp_path / "extracted"
    extract_path.mkdir()
    FileOperands.decompressFiles(str(zip_path), str(extract_path))

    # Verify the files were extracted
    assert (extract_path / "file1.txt").exists()
    assert (extract_path / "file2.txt").exists()
